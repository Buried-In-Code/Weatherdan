__all__ = ["Settings"]

import tomllib as tomlreader
from datetime import datetime, timedelta
from pathlib import Path
from typing import ClassVar

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
    last_updated: datetime = datetime.now() - timedelta(days=365)

    @field_validator("last_updated")
    def validate_last_updated(cls, v: datetime) -> datetime:
        year_ago = datetime.now() - timedelta(days=365)
        return year_ago if v < year_ago else v


class _Settings(SettingsModel):
    _filepath: ClassVar[Path] = get_config_root() / "settings.toml"
    _instance: ClassVar["_Settings"] = None
    ecowitt: EcowittSettings = EcowittSettings()
    website: WebsiteSettings = WebsiteSettings()

    @classmethod
    def load(cls) -> "_Settings":
        if not cls._filepath.exists():
            _Settings().save()
        with cls._filepath.open("rb") as stream:
            content = tomlreader.load(stream)
        return _Settings(**content)

    def save(self) -> "_Settings":
        with self._filepath.open("wb") as stream:
            content = self.model_dump(by_alias=False)
            tomlwriter.dump(content, stream)
        return self


def Settings() -> _Settings:  # noqa: N802
    if _Settings._instance is None:
        _Settings._instance = _Settings.load()
    return _Settings._instance
