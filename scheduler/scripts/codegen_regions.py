import asyncio
import json
import logging
import pathlib
from typing import cast

import httpx
from shapely.geometry import Point, shape
from shapely.geometry.base import BaseGeometry
from src.utils.wattime import _get_auth_token

logger = logging.getLogger(__name__)


ELECTRICITY_MAPS_REGIONS_JSON = "https://raw.githubusercontent.com/electricitymaps/electricitymaps-contrib/refs/heads/master/config/data_centers/data_centers.json"


async def region_from_loc(
    latitude: float, longitude: float, name: str, polygons: dict[str, BaseGeometry]
) -> str | None:
    for region, polygon in polygons.items():
        if polygon.contains(Point(longitude, latitude)):
            return region

    logger.warning(f"No region found for {name} ({latitude}, {longitude})")
    breakpoint()
    return None


async def electricity_map_zone_to_cloud_power_zone_pair(
    region: dict, polygons: dict[str, BaseGeometry]
) -> tuple[tuple[str, str], str | None]:
    provider: str = region["provider"]
    cloud_region: str = region["region"]
    lon, lat = region["lonlat"]
    power_zone = await region_from_loc(
        latitude=lat, longitude=lon, name=f"{provider}-{cloud_region}", polygons=polygons
    )

    return (provider, cloud_region), power_zone


async def get_regions() -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(ELECTRICITY_MAPS_REGIONS_JSON)
        return cast(list[dict], response.json().values())


async def get_polygons(token: str) -> dict[str, BaseGeometry]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.watttime.org/v3/maps",
            headers={"Authorization": f"Bearer {token}"},
            params={"signal_type": "co2_moer"},
        )
        return {
            feature["properties"]["region"]: shape(feature["geometry"])
            for feature in response.json()["features"]
        }


async def write_regions(pairs: list[tuple[tuple[str, str], str]]) -> None:
    # Write power zones to file
    power_zones = {pair[1] for pair in pairs}
    with pathlib.Path("src/regions/power_zones.py").open("w") as f:
        f.write("from enum import Enum\n\n")
        f.write("class PowerZone(Enum):\n")
        # sort power zones alphabetically
        power_zones_sorted = sorted(power_zones)
        for power_zone in power_zones_sorted:
            f.write(f'    {power_zone} = "{power_zone}"\n')

    # Write cloud regions to files
    unique_providers = {pair[0][0] for pair in pairs}
    for provider in unique_providers:
        provider_regions = {pair[0][1] for pair in pairs if pair[0][0] == provider}
        with pathlib.Path(f"src/regions/{provider.lower()}.py").open("w") as f:
            f.write("from enum import Enum\n\n")
            f.write(f"class {provider.capitalize()}Region(Enum):\n")
            # sort regions alphabetically
            provider_regions_sorted = sorted(provider_regions)
            for cloud_region in provider_regions_sorted:
                cloud_region_python = cloud_region.replace("-", "_")
                f.write(f'    {cloud_region_python} = "{cloud_region}"\n')

    # Write cloud zone to power zone mapping to file
    with pathlib.Path("src/regions/mapping.json").open("w") as f:
        # sort pairs alphabetically by cloud region
        json.dump(sorted(pairs, key=lambda pair: (pair[0][0], pair[0][1])), f, indent=2)


async def main() -> None:
    # Fetch regions from the ElectricityMaps GH
    regions = await get_regions()

    # Map cloud regions to power zones
    token = await _get_auth_token()
    polygons = await get_polygons(token)
    cloud_zone_to_power_zone_pairs = await asyncio.gather(
        *[electricity_map_zone_to_cloud_power_zone_pair(region, polygons) for region in regions]
    )

    # Filter out None values
    filtered_pairs = cast(
        list[tuple[tuple[str, str], str]],
        [pair for pair in cloud_zone_to_power_zone_pairs if pair[1] is not None],
    )

    # Write to files
    await write_regions(filtered_pairs)


if __name__ == "__main__":
    asyncio.run(main())
