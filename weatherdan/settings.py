__all__ = ["Settings", "Source"]

import tomllib as tomlreader
from datetime import datetime, timedelta
from enum import Enum
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


class Source(str, Enum):
    POSTGRES = "POSTGRES"
    SQLITE = "SQLITE"


class DatabaseSettings(SettingsModel):
    host: str = ""
    name: str = "freyr.sqlite"
    password: str = ""
    source: Source = Source.SQLITE
    user: str = ""

    @property
    def db_url(self: Self) -> str:
        if self.source == Source.POSTGRES:
            return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}/{self.name}"
        return f"sqlite:///{self.name}"


class EcowittSettings(SettingsModel):
    application_key: str = ""
    api_key: str = ""


class UpdateSettings(SettingsModel):
    rainfall: datetime = datetime.now() - timedelta(days=365)
    solar: datetime = datetime.now() - timedelta(days=365)
    uv_index: datetime = datetime.now() - timedelta(days=365)
    wind: datetime = datetime.now() - timedelta(days=365)


class WebsiteSettings(SettingsModel):
    host: str = "127.0.0.1"
    port: int = 25710
    reload: bool = False


class Settings(SettingsModel):
    _filepath: ClassVar[Path] = get_config_root() / "settings.toml"
    database: DatabaseSettings = DatabaseSettings()
    ecowitt: EcowittSettings = EcowittSettings()
    last_updated: UpdateSettings = UpdateSettings()
    website: WebsiteSettings = WebsiteSettings()

    @classmethod
    def load(cls: type[Self]) -> Self:
        if not cls._filepath.exists():
            cls().save()
        with cls._filepath.open("rb") as stream:
            content = tomlreader.load(stream)
        return cls(**content)

    def save(self: Self) -> Self:
        with self._filepath.open("wb") as stream:
            content = self.model_dump(by_alias=False)
            tomlwriter.dump(content, stream)
        return self
