import logging

from fastapi import APIRouter
from pydantic import BaseModel

from src.forecasting.conversion import PowerZone, convert_power_zone_to_cloud_zones
from src.types.schedule import CloudZone
from src.utils.wattime import get_regions

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/regions",
    tags=["regions"],
    responses={404: {"description": "Not found"}},
)


class RegionResponse(BaseModel):
    regions: list[CloudZone]


@router.get("/")  # type: ignore[misc]
async def regions() -> RegionResponse:
    """Returns list of available regions."""
    power_zones = await get_regions()
    regions = set()
    for power_zone_dict in power_zones:
        try:
            power_zone = PowerZone(power_zone_dict["region"])
        except ValueError:
            logger.info(f"Invalid power zone: {power_zone_dict}")
            continue

        regions.update(convert_power_zone_to_cloud_zones(power_zone))

    return RegionResponse(regions=list(regions))
