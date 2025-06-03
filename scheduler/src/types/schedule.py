from __future__ import annotations

from datetime import UTC, datetime, timedelta

from pydantic import BaseModel, Field, model_validator

from src.regions.aws import AwsRegion
from src.regions.azure import AzureRegion
from src.regions.gcp import GcpRegion
from src.regions.ovh import OvhRegion
from src.regions.provider import CloudProvider


class CloudZone(BaseModel):
    provider: CloudProvider
    region: AwsRegion | GcpRegion | AzureRegion | OvhRegion

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
            elif self.provider == CloudProvider.OVH:
                OvhRegion(self.region)
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
        # convert start and end to UTC if they are naive
        tz_unset = self.start.tzinfo is None or self.end.tzinfo is None
        if tz_unset:
            self.start = self.start.replace(tzinfo=UTC)
            self.end = self.end.replace(tzinfo=UTC)

        if self.start < datetime.now(UTC) - timedelta(minutes=5):
            if tz_unset:
                raise ValueError(
                    "Start time must be in the future. Note that timezone was unset and UTC was assumed."
                )
            raise ValueError("Start time must be in the future.")
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
