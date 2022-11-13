__all__ = ["Settings"]

from datetime import datetime, timedelta
from typing import ClassVar

import tomli_w as tomlwriter
import tomllib as tomlreader
from pydantic import BaseModel as PyModel
from pydantic import Extra, validator

from ecowitt import get_config_root


class BaseModel(PyModel):
    class Config:
        anystr_strip_whitespace = True
        allow_population_by_field_name = True
        extra = Extra.ignore


class Ecowitt(BaseModel):
    application_key: str = ""
    api_key: str = ""
    last_updated: datetime = datetime.now() - timedelta(days=365)

    @validator("last_updated", always=True)
    def validate_last_updated(cls, v) -> datetime:
        year_ago = datetime.now() - timedelta(days=365)
        return year_ago if v < year_ago else v


class Settings(BaseModel):
    FILENAME: ClassVar = get_config_root() / "settings.toml"
    ecowitt: Ecowitt = Ecowitt()

    @classmethod
    def load(cls) -> "Settings":
        if not cls.FILENAME.exists():
            Settings().save()
        with cls.FILENAME.open("rb") as stream:
            content = tomlreader.load(stream)
        return Settings(**content)

    def save(self):
        with self.FILENAME.open("wb") as stream:
            content = self.dict(by_alias=False)
            tomlwriter.dump(content, stream)
