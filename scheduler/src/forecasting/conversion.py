import enum
import logging

from src.types.schedule import AwsRegion, CloudProvider, CloudZone

logger = logging.getLogger(__name__)


class PowerZone(enum.Enum):
    PJM_DC = "PJM_DC"
    CAISO_NORTH = "CAISO_NORTH"
    DE = "DE"
    NEM_NSW = "NEM_NSW"


_power_zone_map: dict[CloudZone, PowerZone] = {
    CloudZone(provider=CloudProvider.AWS, region=AwsRegion("us-east-1")): PowerZone.PJM_DC,
    CloudZone(provider=CloudProvider.AWS, region=AwsRegion("us-west-1")): PowerZone.CAISO_NORTH,
    CloudZone(provider=CloudProvider.AWS, region=AwsRegion("eu-central-1")): PowerZone.DE,
    CloudZone(provider=CloudProvider.AWS, region=AwsRegion("ap-southeast-2")): PowerZone.NEM_NSW,
}


def convert_cloud_zone_to_power_zone(cloud_zone: CloudZone) -> PowerZone:
    return _power_zone_map[cloud_zone]


def convert_power_zone_to_cloud_zones(power_zone: PowerZone) -> list[CloudZone]:
    ret = [cloud for cloud, power in _power_zone_map.items() if power == power_zone]
    logger.warning(f"{ret=}")
    return ret
