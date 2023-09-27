__all__ = ["Settings"]

import tomllib as tomlreader
from datetime import datetime, timedelta
from pathlib import Path
from typing import ClassVar, Self

import tomli_w as tomlwriter
from pydantic import BaseModel

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
    host: str = "127.0.0.1"
    port: int = 25710
    reload: bool = False


class EcowittSettings(SettingsModel):
    application_key: str = ""
    api_key: str = ""


class UpdateSettings(SettingsModel):
    pressure: datetime = datetime.now() - timedelta(days=365)  # noqa: DTZ005
    rainfall: datetime = datetime.now() - timedelta(days=365)  # noqa: DTZ005
    solar: datetime = datetime.now() - timedelta(days=365)  # noqa: DTZ005
    uv_index: datetime = datetime.now() - timedelta(days=365)  # noqa: DTZ005
    wind: datetime = datetime.now() - timedelta(days=365)  # noqa: DTZ005


class Settings(SettingsModel):
    _filepath: ClassVar[Path] = get_config_root() / "settings.toml"
    ecowitt: EcowittSettings = EcowittSettings()
    last_updated: UpdateSettings = UpdateSettings()
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
