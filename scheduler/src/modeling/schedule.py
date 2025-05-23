import logging
from datetime import timedelta

import pandas as pd

from src.forecasting.conversion import PowerZone, convert_power_zone_to_cloud_zones
from src.forecasting.fetch import fetch_forecast
from src.types.schedule import (
    CarbonSavings,
    ScheduleOption,
    ScheduleRequest,
    ScheduleResponse,
    TimeRange,
)

logger = logging.getLogger(__name__)


async def compute_schedule(request: ScheduleRequest) -> ScheduleResponse:
    """Computes the best schedule for the given request."""
    # fetch forecast
    forecast_df = await fetch_forecast(request.zones, request.windows)

    # trim forecast to windows
    trimmed_forecast_df = _trim_forecast_to_windows(forecast_df, request.windows, request.duration)

    # rollup forecast to windows (rolling average of duration)
    rolled_forecast_df = _rollup_forecast_to_job_duration(trimmed_forecast_df, request.duration)

    # If we don't have any forecast data, return an error
    if rolled_forecast_df.empty:
        raise ValueError(
            "No valid forecast data available for the requested time windows and zones"
        )

    # Map power zones back to cloud zones
    # This requires exploding the dataframe since one power zone can map to multiple cloud zones
    result_rows = []
    for _, row in rolled_forecast_df.iterrows():
        power_zone = PowerZone(row["power_zone"])
        cloud_zones = convert_power_zone_to_cloud_zones(power_zone)

        for cloud_zone in cloud_zones:
            result_rows.append(
                {
                    "time": row["time"],
                    "zone": cloud_zone,
                    "co2_intensity": row["c02_moer"],
                    "window_id": row["window_id"],
                }
            )

    # Create a new dataframe with the cloud zones
    options_df = pd.DataFrame(result_rows)

    # Sort by carbon intensity (lower is better)
    options_df = options_df.sort_values("co2_intensity")

    # Get the best (lowest) carbon intensity option
    best_option = options_df.iloc[0]
    ideal = ScheduleOption(
        time=best_option["time"],
        zone=best_option["zone"],
        co2_intensity=best_option["co2_intensity"],
    )

    # Get the worst (highest) carbon intensity option
    worst_option = options_df.iloc[-1]
    worst_case = ScheduleOption(
        time=worst_option["time"],
        zone=worst_option["zone"],
        co2_intensity=worst_option["co2_intensity"],
    )

    # Get the median option
    median_idx = len(options_df) // 2
    median_option = options_df.iloc[median_idx]
    median_case = ScheduleOption(
        time=median_option["time"],
        zone=median_option["zone"],
        co2_intensity=median_option["co2_intensity"],
    )

    # For naive case, we'll use the first time slot of the first window with the first zone
    # This simulates what would happen if no carbon-aware scheduling was used
    first_window_mask = options_df["window_id"] == options_df["window_id"].min()
    first_time_in_window = options_df[first_window_mask]["time"].min()
    naive_options = options_df[
        (options_df["window_id"] == options_df["window_id"].min())
        & (options_df["time"] == first_time_in_window)
    ]
    naive_option = naive_options.iloc[0]
    naive_case = ScheduleOption(
        time=naive_option["time"],
        zone=naive_option["zone"],
        co2_intensity=naive_option["co2_intensity"],
    )

    # Get the top N options based on the request num_options parameter
    num_options = request.num_options if request.num_options is not None else 3
    top_n_options = []
    for i in range(min(num_options, len(options_df))):
        option = options_df.iloc[i]
        top_n_options.append(
            ScheduleOption(
                time=option["time"], zone=option["zone"], co2_intensity=option["co2_intensity"]
            )
        )

    # Calculate carbon savings
    carbon_savings = CarbonSavings(
        vs_worst_case=float(
            (worst_case.co2_intensity - ideal.co2_intensity) / worst_case.co2_intensity * 100
        ),
        vs_naive_case=float(
            (naive_case.co2_intensity - ideal.co2_intensity) / naive_case.co2_intensity * 100
        ),
        vs_median_case=float(
            (median_case.co2_intensity - ideal.co2_intensity) / median_case.co2_intensity * 100
        ),
    )

    # Construct and return the full schedule response
    return ScheduleResponse(
        ideal=ideal,
        options=top_n_options,
        worst_case=worst_case,
        naive_case=naive_case,
        median_case=median_case,
        carbon_savings=carbon_savings,
    )


def _rollup_forecast_to_job_duration(
    forecast_df: pd.DataFrame, duration: timedelta
) -> pd.DataFrame:
    """Rolls up the forecast dataframe to the job duration.

    So, if we have a duration of 1 hour, and we have a forecast every 15 minutes, we will take the average of the 4 15 minute forecasts to get a 1 hour forecast.
    The roll up cannot cross windows.

    Args:
        forecast_df: The forecast dataframe
        duration: The duration of the job

    Returns:
        A dataframe with rolled up forecasts, where each row represents a potential job start time
        with the average carbon intensity over the job duration
    """
    # Check if dataframe is empty
    if forecast_df.empty:
        return pd.DataFrame()

    # Calculate the number of 5-minute intervals that make up the job duration
    # Assuming data is at 5-minute intervals
    interval_minutes = 5
    window_size = int(duration.total_seconds() / 60 / interval_minutes)

    if window_size < 1:
        # If job duration is less than the forecast interval, use the forecast as is
        return forecast_df

    # Process each window separately
    result_dfs = []

    # Group by window_id to process each window separately
    for _, window_df in forecast_df.groupby("window_id"):
        # Skip if the window doesn't have enough data points
        if len(window_df) < window_size:
            continue

        # Sort by time to ensure correct rolling window calculation
        window_df_sorted = window_df.sort_values("point_time")

        # Create a rolling window to compute the average
        rolling = window_df_sorted["value"].rolling(window=window_size)

        # Calculate the mean for each window
        window_df_sorted["c02_moer"] = rolling.mean()

        # Drop rows with NaN (incomplete windows)
        window_df_sorted = window_df_sorted.dropna(subset=["c02_moer"])

        # Important: By default, the rolling window assigns the result to the last point in the window
        # We need to shift the timestamps back to represent the START of each window
        # The current 'point_time' is the END of each window

        # Calculate the offset duration: (window_size - 1) * 5 minutes
        offset_duration = pd.Timedelta(minutes=(window_size - 1) * 5)
        # Simply subtract the offset duration from point_time to get the start time
        window_df_sorted["start_time"] = window_df_sorted["point_time"] - offset_duration

        # Drop rows with NaN values from the rolling operation
        rolled_forecast_df = window_df_sorted.dropna(subset=["c02_moer"])

        # Keep only necessary columns and rename for clarity
        result_df = rolled_forecast_df[["start_time", "c02_moer", "window_id", "power_zone"]].copy()
        result_df = result_df.rename(
            columns={
                "start_time": "time",
            }
        )

        result_dfs.append(result_df)

    # Combine results from all windows
    if not result_dfs:
        return pd.DataFrame()  # Return empty dataframe if no valid windows

    return pd.concat(result_dfs, ignore_index=True)


def _trim_forecast_to_windows(
    forecast_df: pd.DataFrame, windows: list[TimeRange], duration: timedelta
) -> pd.DataFrame:
    """Trims the forecast dataframe to only include the windows specified in the request.

    Trimmed forecast will contain all values within the time ranges [window.start, window.end + duration], for each window.

    Args:
        forecast_df: The forecast dataframe
        windows: The windows to trim to
        duration: The duration of the forecast
    """
    forecast_df["point_time"] = pd.to_datetime(forecast_df["point_time"])

    # Create a mask for each window and combine them
    mask = pd.Series(False, index=forecast_df.index)

    for window in windows:
        # For each window, include data points from window.start to window.end + duration
        window_end_with_duration = window.end + duration
        window_mask = (forecast_df["point_time"] >= window.start) & (
            forecast_df["point_time"] <= window_end_with_duration
        )
        mask = mask | window_mask

    # Apply the combined mask to filter the dataframe
    trimmed_df = forecast_df[mask].copy()

    # Add composite window_id based on both time window and power_zone
    # This ensures that different power zones are treated as separate windows
    trimmed_df["window_id"] = None

    # Get unique power zones
    power_zones = trimmed_df["power_zone"].unique()

    # Assign unique window_id for each combination of time window and power_zone
    window_counter = 0
    for window in windows:
        window_end_with_duration = window.end + duration
        for power_zone in power_zones:
            # Create mask for this specific time window and power zone
            window_mask = (
                (trimmed_df["point_time"] >= window.start)
                & (trimmed_df["point_time"] <= window_end_with_duration)
                & (trimmed_df["power_zone"] == power_zone)
            )
            # Only create a window if there are matching data points
            if window_mask.any():
                trimmed_df.loc[window_mask, "window_id"] = window_counter
                window_counter += 1

    return trimmed_df
