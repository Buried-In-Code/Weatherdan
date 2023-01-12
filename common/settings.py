__all__ = ["Settings"]

from datetime import datetime, timedelta
from typing import ClassVar

import tomli_w as tomlwriter
import tomllib as tomlreader
from pydantic import BaseModel, Extra, Field, validator

from common import get_config_root


class SettingsModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        anystr_strip_whitespace = True
        validate_assignment = True
        extra = Extra.ignore


class WebsiteSettings(SettingsModel):
    host: str = "localhost"
    port: int = 8001


class EmailSettings(SettingsModel):
    sender_email: str = ""
    sender_password: str = ""
    reciever_emails: list[str] = Field(default_factory=list)
    enable: bool = False


class EcowittSettings(SettingsModel):
    application_key: str = ""
    api_key: str = ""
    last_updated: datetime = datetime.now() - timedelta(days=365)

    @validator("last_updated", always=True)
    def validate_last_updated(cls, v) -> datetime:
        year_ago = datetime.now() - timedelta(days=365)
        return year_ago if v < year_ago else v


class Settings(SettingsModel):
    FILENAME: ClassVar = get_config_root() / "settings.toml"
    ecowitt: EcowittSettings = EcowittSettings()
    email: EmailSettings = EmailSettings()
    website: WebsiteSettings = WebsiteSettings()

    @classmethod
    def load(cls) -> "Settings":
        if not cls.FILENAME.exists():
            Settings().save()
        with cls.FILENAME.open("rb") as stream:
            content = tomlreader.load(stream)
        return Settings(**content)

    def save(self) -> "Settings":
        with self.FILENAME.open("wb") as stream:
            content = self.dict(by_alias=False)
            tomlwriter.dump(content, stream)
        return self
