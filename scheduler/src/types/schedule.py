from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum

from pydantic import BaseModel, Field, model_validator


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
    us_central1 = "us-central1"


class AzureRegion(Enum):
    eastus = "eastus"
    eastus2 = "eastus2"
    southcentralus = "southcentralus"
    westus2 = "westus2"
    westus3 = "westus3"
    northeurope = "northeurope"
    swedencentral = "swedencentral"
    uksouth = "uksouth"
    westeurope = "westeurope"
    centralus = "centralus"
    francecentral = "francecentral"
    germanywestcentral = "germanywestcentral"
    italynorth = "italynorth"
    norwayeast = "norwayeast"
    polandcentral = "polandcentral"
    eastus2euap = "eastus2euap"
    eastusstg = "eastusstg"
    northcentralus = "northcentralus"
    westus = "westus"
    centraluseuap = "centraluseuap"
    westcentralus = "westcentralus"
    francesouth = "francesouth"
    germanynorth = "germanynorth"
    norwaywest = "norwaywest"
    ukwest = "ukwest"


class CloudZone(BaseModel):
    provider: CloudProvider
    region: AwsRegion | GcpRegion | AzureRegion

    def __hash__(self) -> int:
        return hash((self.provider, self.region))

    @model_validator(mode="after")
    def validate_region(self) -> CloudZone:
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
            raise ValueError(
                f"Invalid region '{self.region}' for provider '{self.provider}'"
            ) from e

        return self


class TimeRange(BaseModel):
    start: datetime
    end: datetime

    @model_validator(mode="after")
    def validate_time_range(self) -> TimeRange:
        if self.start < datetime.now():
            raise ValueError("Start time must be in the future")
        if self.start >= self.end:
            raise ValueError("Start time must be before end time")
        return self


class ScheduleRequest(BaseModel):
    windows: list[TimeRange] = Field(
        ..., description="List of time windows to schedule (start and end must be in the future)"
    )
    duration: timedelta = Field(..., examples=["PT1H"])
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
