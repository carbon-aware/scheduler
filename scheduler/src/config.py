from pydantic import Field
from pydantic_settings import BaseSettings


class WattTimeSettings(BaseSettings):
    """
    Settings for WattTime API authentication.
    """

    username: str = Field(..., alias="WATTTIME_USERNAME")
    password: str = Field(..., alias="WATTTIME_PASSWORD")


class Settings(BaseSettings):
    """
    Application settings.
    """

    watttime: WattTimeSettings = WattTimeSettings()


# Create a global settings instance
settings = Settings()
