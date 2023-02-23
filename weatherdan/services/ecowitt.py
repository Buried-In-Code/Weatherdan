__all__ = ["Ecowitt", "Category"]

import logging
import platform
from datetime import datetime
from enum import Enum
from typing import Any

from ratelimit import limits, sleep_and_retry
from requests import get
from requests.exceptions import ConnectionError, HTTPError, JSONDecodeError, ReadTimeout

from weatherdan import __version__
from weatherdan.services.exceptions import AuthenticationError, ServiceError
from weatherdan.settings import Settings

MINUTE = 60
LOGGER = logging.getLogger(__name__)


class Category(Enum):
    RAINFALL = "rainfall.daily"
    TEMPERATURE = "indoor.temperature"
    HUMIDITY = "indoor.humidity"

    @property
    def group_1(self) -> str:
        return self.value.split(".")[0]

    @property
    def group_2(self) -> str:
        return self.value.split(".")[1]


class Ecowitt:
    API_URL = "https://api.ecowitt.net/api/v3"

    def __init__(self, timeout: float = 30.0):
        self.headers = {
            "Accept": "application/json",
            "User-Agent": f"Weather-Dan/{__version__}/{platform.system()}: {platform.release()}",
        }
        self.timeout = timeout

        settings = Settings()
        self.application_key = settings.ecowitt.application_key
        self.api_key = settings.ecowitt.api_key

    @sleep_and_retry
    @limits(calls=20, period=MINUTE)
    def _perform_get_request(self, url: str, params: dict[str, str]) -> dict[str, Any]:
        try:
            response = get(url, params=params, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except ConnectionError as err:
            raise ServiceError(f"Unable to connect to '{url}'") from err
        except HTTPError as err:
            raise ServiceError(err.response.text) from err
        except JSONDecodeError as err:
            raise ServiceError(f"Unable to parse response from '{url}' as Json") from err
        except ReadTimeout as err:
            raise ServiceError("Server took too long to respond") from err

    @sleep_and_retry
    @limits(calls=20, period=MINUTE)
    def _get_request(self, endpoint: str, params: dict[str, str] = None) -> dict[str, Any]:
        if params is None:
            params = {}
        params["application_key"] = self.application_key
        params["api_key"] = self.api_key

        url = self.API_URL + endpoint

        response = self._perform_get_request(url=url, params=params)
        if response["code"] != 0:
            if response["code"] == 40010:
                raise AuthenticationError(response["msg"])
            raise ServiceError(f"{response['code']} | {response['msg']}")
        return response

    def test_credentials(self) -> bool:
        try:
            self.list_devices()
            return True
        except AuthenticationError:
            pass
        return False

    def list_devices(self) -> list[tuple[str, str]]:
        results = self._retrieve_all_responses(endpoint="/device/list")
        return [(x["mac"], x["name"]) for x in results]

    def list_device_history(
        self, mac: str, last_updated: datetime, category: Category
    ) -> dict[datetime, str]:
        results = self._get_request(
            endpoint="/device/history",
            params={
                "mac": mac,
                "start_date": last_updated.isoformat(),
                "end_date": datetime.now().isoformat(),
                "call_back": category.value,
                "rainfall_unitid": 12,
                "temp_unitid": 1,
            },
        )["data"]
        if not results:
            return {}
        return {
            datetime.fromtimestamp(int(k)): v
            for k, v in results[category.group_1][category.group_2]["list"].items()
        }

    def get_device_reading(self, mac: str, category: Category) -> tuple[datetime, str]:
        results = self._get_request(
            endpoint="/device/real_time",
            params={
                "mac": mac,
                "call_back": category.value,
                "rainfall_unitid": 12,
                "temp_unitid": 1,
            },
        )["data"]
        timestamp = datetime.fromtimestamp(int(results[category.group_1][category.group_2]["time"]))
        return timestamp, results[category.group_1][category.group_2]["value"]

    def _retrieve_all_responses(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        if params is None:
            params = {}
        params["limit"] = 100
        params["page"] = 1
        response = self._get_request(endpoint=endpoint, params=params)["data"]
        results = response["list"]
        while response["list"] and len(results) < int(response["total"]):
            params["page"] += 1
            response = self._get_request(endpoint=endpoint, params=params)["data"]
            results.extend(response["list"])
        return results
