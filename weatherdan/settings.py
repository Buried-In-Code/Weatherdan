__all__ = ["Settings"]

import tomllib as tomlreader
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import ClassVar, Self

import tomli_w as tomlwriter
from pydantic import BaseModel, field_validator

from weatherdan import get_config_root


class SettingsModel(
    BaseModel,
    populate_by_name=True,
    str_strip_whitespace=True,
    validate_assignment=True,
    revalidate_instances="always",
    extra="ignore",
):
    pass


class WebsiteSettings(SettingsModel):
    host: str = "localhost"
    port: int = 3326
    reload: bool = False


class EcowittSettings(SettingsModel):
    application_key: str = ""
    api_key: str = ""
    last_updated: datetime = datetime.now(tz=UTC).astimezone() - timedelta(days=365)

    @field_validator("last_updated")
    def validate_last_updated(cls: Self, v: datetime) -> datetime:
        year_ago = datetime.now(tz=UTC).astimezone() - timedelta(days=365)
        return year_ago if v < year_ago else v


class Settings(SettingsModel):
    _filepath: ClassVar[Path] = get_config_root() / "settings.toml"
    ecowitt: EcowittSettings = EcowittSettings()
    website: WebsiteSettings = WebsiteSettings()

    @classmethod
    def load(cls: Self) -> Self:
        if not cls._filepath.exists():
            Settings().save()
        with cls._filepath.open("rb") as stream:
            content = tomlreader.load(stream)
        return Settings(**content)

    def save(self: Self) -> Self:
        with self._filepath.open("wb") as stream:
            content = self.model_dump(by_alias=False)
            tomlwriter.dump(content, stream)
        return self
