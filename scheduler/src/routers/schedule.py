from fastapi import APIRouter
from datetime import datetime

from src.types.schedule import ScheduleRequest, ScheduleResponse, ScheduleOption, CarbonSavings, CloudZone, CloudProvider, AwsRegion

router = APIRouter(
    prefix="/schedule",
    tags=["schedule"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def schedule(request: ScheduleRequest) -> ScheduleResponse:
    # TODO: implement schedule
    # Return a dummy response for now
    return ScheduleResponse(
        ideal=ScheduleOption(time=datetime.now(), zone=CloudZone(provider=CloudProvider.AWS, region=AwsRegion("us-west-1")), co2_intensity=100.5),
        options=[ScheduleOption(time=datetime.now(), zone=CloudZone(provider=CloudProvider.AWS, region=AwsRegion("us-west-1")), co2_intensity=100.5)],
        worst_case=ScheduleOption(time=datetime.now(), zone=CloudZone(provider=CloudProvider.AWS, region=AwsRegion("us-west-1")), co2_intensity=100.5),
        naive_case=ScheduleOption(time=datetime.now(), zone=CloudZone(provider=CloudProvider.AWS, region=AwsRegion("eu-central-1")), co2_intensity=100.5),
        median_case=ScheduleOption(time=datetime.now(), zone=CloudZone(provider=CloudProvider.AWS, region=AwsRegion("us-east-1")), co2_intensity=100.5),
        carbon_savings=CarbonSavings(vs_worst_case=100.5, vs_naive_case=100.5, vs_median_case=100.5)
    )
