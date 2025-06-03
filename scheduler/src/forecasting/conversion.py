import json
import logging
import os

from src.regions.power_zones import PowerZone
from src.types.schedule import CloudZone

logger = logging.getLogger(__name__)


def _load_power_zone_map() -> dict[CloudZone, PowerZone]:
    current_dir = os.path.dirname(__file__)
    with open(os.path.join(current_dir, "../regions/mapping.json")) as f:
        raw_map = json.load(f)

    return {
        CloudZone(provider=zone[0][0], region=zone[0][1]): PowerZone(zone[1]) for zone in raw_map
    }


_power_zone_map = _load_power_zone_map()


def convert_cloud_zone_to_power_zone(cloud_zone: CloudZone) -> PowerZone:
    return _power_zone_map[cloud_zone]


def convert_power_zone_to_cloud_zones(
    power_zone: PowerZone, allowed_zones: list[CloudZone] | None = None
) -> list[CloudZone]:
    ret = [
        cloud
        for cloud, power in _power_zone_map.items()
        if power == power_zone and (allowed_zones is None or cloud in allowed_zones)
    ]
    logger.debug(f"Conversion results: {ret}")
    return ret
