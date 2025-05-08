from enum import Enum
from pydantic import BaseModel, Field, model_validator
from datetime import datetime


class CloudProvider(Enum):
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"

class AwsRegion(Enum):
    us_east_1 = "us-east-1"
    us_west_1 = "us-west-1"
    eu_central_1 = "eu-central-1"
    ap_southeast_2 = "ap-southeast-2"

class GcpRegion(Enum):
    pass

class AzureRegion(Enum):
    pass

class CloudZone(BaseModel):
    provider: CloudProvider
    region: AwsRegion | GcpRegion | AzureRegion

    @model_validator(mode="after")
    def validate_region(self) -> 'CloudZone':
        try:
            if self.provider == CloudProvider.AWS:
                AwsRegion(self.region)
            elif self.provider == CloudProvider.GCP:
                GcpRegion(self.region)
            elif self.provider == CloudProvider.AZURE:
                AzureRegion(self.region)
            else:
                raise ValueError(f"Invalid provider: {self.provider}")
        except ValueError as e:
            raise ValueError(f"Invalid region '{self.region}' for provider '{self.provider}'") from e

        return self

class TimeRange(BaseModel):
    start: datetime
    end: datetime

class ScheduleRequest(BaseModel):
    windows: list[TimeRange]
    duration: str
    zones: list[CloudZone]
    num_options: int | None = Field(default=3)

class ScheduleOption(BaseModel):
    time: datetime
    zone: CloudZone
    co2_intensity: float

class CarbonSavings(BaseModel):
    vs_worst_case: float
    vs_naive_case: float
    vs_median_case: float

class ScheduleResponse(BaseModel):
    ideal: ScheduleOption
    options: list[ScheduleOption]
    worst_case: ScheduleOption
    naive_case: ScheduleOption
    median_case: ScheduleOption
    carbon_savings: CarbonSavings
