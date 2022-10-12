__all__ = ["Settings"]

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, ClassVar

from common import get_config_root

try:
    import tomlreader  # Python >= 3.11
except ModuleNotFoundError:
    import tomli as tomlreader  # Python < 3.11

import tomli_w as tomlwriter


@dataclass
class Display:
    show_rainfall: bool = True
    show_temperature: bool = False

    @staticmethod
    def parse(content: dict[str, bool]) -> "Display":
        return Display(
            show_rainfall=content["show_rainfall"],
            show_temperature=content["show_temperature"],
        )

    def unparse(self) -> dict[str, bool]:
        return {
            "show_rainfall": self.show_rainfall,
            "show_temperature": self.show_temperature,
        }


@dataclass
class Ecowitt:
    application_key: str = ""
    api_key: str = ""
    last_updated: datetime = datetime.now() - timedelta(days=365)

    def __post_init__(self):
        year_ago = datetime.now() - timedelta(days=365)
        if self.last_updated < year_ago:
            self.last_updated = year_ago

    @staticmethod
    def parse(content: dict[str, str]) -> "Ecowitt":
        return Ecowitt(
            application_key=content["application_key"],
            api_key=content["api_key"],
            last_updated=datetime.fromisoformat(content["last_updated"]),
        )

    def unparse(self) -> dict[str, str]:
        return {
            "application_key": self.application_key,
            "api_key": self.api_key,
            "last_updated": self.last_updated.isoformat(),
        }


@dataclass
class Settings:
    FILENAME: ClassVar = get_config_root() / "settings.toml"
    display: Display = Display()
    ecowitt: Ecowitt = Ecowitt()

    @staticmethod
    def parse(content: dict[str, Any]) -> "Settings":
        return Settings(
            display=Display.parse(content["display"]),
            ecowitt=Ecowitt.parse(content["ecowitt"]),
        )

    def unparse(self) -> dict[str, Any]:
        return {"display": self.display.unparse(), "ecowitt": self.ecowitt.unparse()}

    @classmethod
    def load(cls) -> "Settings":
        if not cls.FILENAME.exists():
            Settings().save()
        with cls.FILENAME.open("rb") as stream:
            content = tomlreader.load(stream)
        return Settings.parse(content)

    def save(self):
        with self.FILENAME.open("wb") as stream:
            content = self.unparse()
            tomlwriter.dump(content, stream)
