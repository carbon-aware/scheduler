import asyncio
from datetime import datetime, UTC
import logging

import pandas as pd

from src.forecasting.conversion import PowerZone, convert_cloud_zone_to_power_zone
from src.types.schedule import CloudZone, TimeRange
from src.utils.wattime import get_forecast

logger = logging.getLogger(__name__)


async def fetch_forecast(
    cloud_zones: list[CloudZone],
    windows: list[TimeRange]
) -> pd.DataFrame:
    # convert from cloud zones to power zones
    power_zones = [convert_cloud_zone_to_power_zone(cloud_zone) for cloud_zone in cloud_zones]

    # get horizon from windows
    horizon = (max([window.end for window in windows]) - datetime.now(tz=UTC)).total_seconds() // 3600
    logger.warning(f"Horizon: {horizon}")
    
    # gather forecasts for each power zone
    forecasts = await asyncio.gather(*[_fetch_zone_forecast(power_zone, horizon) for power_zone in power_zones])

    # combine forecasts into a single dataframe
    forecast_df = pd.concat(forecasts, ignore_index=True)

    return forecast_df


async def _fetch_zone_forecast(
    power_zone: PowerZone,
    horizon: int,
) -> pd.DataFrame:
    resp = await get_forecast(power_zone.value, horizon)

    # convert to dataframe
    df = pd.json_normalize(resp, record_path="data")
    df['power_zone'] = power_zone.value

    return df

