"""
Utility functions for interacting with the WattTime API.
"""

import time
from typing import Any, cast

import httpx

from src.config import settings

# Cache for the authentication token
_token_cache: dict[str, Any] = {"token": None, "expiry": 0}

# Token cache duration in seconds (30 minutes)
TOKEN_CACHE_DURATION = 30 * 60


async def _get_auth_token() -> str:
    """
    Get an authentication token from the WattTime API using credentials from settings.

    Returns:
        Authentication token

    Raises:
        Exception: If authentication fails
    """
    current_time = time.time()

    # Return cached token if it's still valid
    if _token_cache["token"] and current_time < _token_cache["expiry"]:
        return cast(str, _token_cache["token"])

    # Fetch new token
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.watttime.org/login",
            auth=(settings.watttime.username, settings.watttime.password),
        )

        if response.status_code != httpx.codes.OK:
            raise Exception(f"Authentication failed: {response.status_code} {response.text}")

        data = response.json()
        token = data.get("token")

        if not token:
            raise Exception("No token received in authentication response")

        # Cache the token
        _token_cache["token"] = token
        _token_cache["expiry"] = current_time + TOKEN_CACHE_DURATION

        return cast(str, token)


async def get_forecast(region: str, horizon_hours: int) -> dict[str, Any]:
    """
    Fetch forecast data from the WattTime API using credentials from settings.

    Args:
        region: The region code to get forecast for
        horizon_hours: Number of hours to forecast

    Returns:
        Forecast data as a dictionary

    Raises:
        Exception: If the API request fails
    """
    # Get authentication token
    token = await _get_auth_token()

    # Fetch forecast data
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.watttime.org/v3/forecast",
            params={"signal_type": "co2_moer", "region": region, "horizonHours": horizon_hours},
            headers={"Authorization": f"Bearer {token}"},
        )

        if response.status_code != httpx.codes.OK:
            raise Exception(f"Failed to fetch forecast: {response.status_code} {response.text}")

        return cast(dict[str, Any], response.json())
