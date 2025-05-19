import enum
import logging

from src.types.schedule import AwsRegion, AzureRegion, CloudProvider, CloudZone, GcpRegion

logger = logging.getLogger(__name__)


class PowerZone(enum.Enum):
    PJM_DC = "PJM_DC"
    CAISO_NORTH = "CAISO_NORTH"
    DE = "DE"
    NEM_NSW = "NEM_NSW"
    SE = "SE"
    IE = "IE"
    PL = "PL"
    PJM_ROANOKE = "PJM_ROANOKE"
    UK = "UK"
    AZPS = "AZPS"
    NO = "NO"
    ERCOT_SANANTONIO = "ERCOT_SANANTONIO"
    GCPD = "GCPD"
    PJM_CHICAGO = "PJM_CHICAGO"
    PACE = "PACE"
    NL = "NL"
    IT = "IT"
    MISO_MASON_CITY = "MISO_MASON_CITY"
    FR = "FR"


_power_zone_map: dict[CloudZone, PowerZone] = {
    CloudZone(provider=CloudProvider.AWS, region=AwsRegion("us-east-1")): PowerZone.PJM_DC,
    CloudZone(provider=CloudProvider.AWS, region=AwsRegion("us-west-1")): PowerZone.CAISO_NORTH,
    CloudZone(provider=CloudProvider.AWS, region=AwsRegion("eu-central-1")): PowerZone.DE,
    CloudZone(provider=CloudProvider.AWS, region=AwsRegion("ap-southeast-2")): PowerZone.NEM_NSW,
    CloudZone(provider=CloudProvider.AZURE, region=AzureRegion("eastus")): PowerZone.PJM_ROANOKE,
    CloudZone(provider=CloudProvider.AZURE, region=AzureRegion("eastus2")): PowerZone.PJM_DC,
    CloudZone(
        provider=CloudProvider.AZURE, region=AzureRegion("southcentralus")
    ): PowerZone.ERCOT_SANANTONIO,
    CloudZone(provider=CloudProvider.AZURE, region=AzureRegion("westus2")): PowerZone.GCPD,
    CloudZone(provider=CloudProvider.AZURE, region=AzureRegion("westus3")): PowerZone.AZPS,
    CloudZone(provider=CloudProvider.AZURE, region=AzureRegion("northeurope")): PowerZone.IE,
    CloudZone(provider=CloudProvider.AZURE, region=AzureRegion("swedencentral")): PowerZone.SE,
    CloudZone(provider=CloudProvider.AZURE, region=AzureRegion("uksouth")): PowerZone.UK,
    CloudZone(provider=CloudProvider.AZURE, region=AzureRegion("westeurope")): PowerZone.NL,
    CloudZone(
        provider=CloudProvider.AZURE, region=AzureRegion("centralus")
    ): PowerZone.MISO_MASON_CITY,
    CloudZone(provider=CloudProvider.AZURE, region=AzureRegion("francecentral")): PowerZone.FR,
    CloudZone(provider=CloudProvider.AZURE, region=AzureRegion("germanywestcentral")): PowerZone.DE,
    CloudZone(provider=CloudProvider.AZURE, region=AzureRegion("italynorth")): PowerZone.IT,
    CloudZone(provider=CloudProvider.AZURE, region=AzureRegion("norwayeast")): PowerZone.NO,
    CloudZone(provider=CloudProvider.AZURE, region=AzureRegion("polandcentral")): PowerZone.PL,
    CloudZone(provider=CloudProvider.AZURE, region=AzureRegion("eastus2euap")): PowerZone.PJM_DC,
    CloudZone(provider=CloudProvider.AZURE, region=AzureRegion("eastusstg")): PowerZone.PJM_ROANOKE,
    CloudZone(
        provider=CloudProvider.AZURE, region=AzureRegion("northcentralus")
    ): PowerZone.PJM_CHICAGO,
    CloudZone(provider=CloudProvider.AZURE, region=AzureRegion("westus")): PowerZone.CAISO_NORTH,
    CloudZone(
        provider=CloudProvider.AZURE, region=AzureRegion("centraluseuap")
    ): PowerZone.MISO_MASON_CITY,
    CloudZone(provider=CloudProvider.AZURE, region=AzureRegion("westcentralus")): PowerZone.PACE,
    CloudZone(provider=CloudProvider.AZURE, region=AzureRegion("francesouth")): PowerZone.FR,
    CloudZone(provider=CloudProvider.AZURE, region=AzureRegion("germanynorth")): PowerZone.DE,
    CloudZone(provider=CloudProvider.AZURE, region=AzureRegion("norwaywest")): PowerZone.NO,
    CloudZone(provider=CloudProvider.AZURE, region=AzureRegion("ukwest")): PowerZone.UK,
    CloudZone(
        provider=CloudProvider.GCP, region=GcpRegion("us-central1")
    ): PowerZone.MISO_MASON_CITY,
}


def convert_cloud_zone_to_power_zone(cloud_zone: CloudZone) -> PowerZone:
    return _power_zone_map[cloud_zone]


def convert_power_zone_to_cloud_zones(power_zone: PowerZone) -> list[CloudZone]:
    ret = [cloud for cloud, power in _power_zone_map.items() if power == power_zone]
    logger.warning(f"{ret=}")
    return ret
