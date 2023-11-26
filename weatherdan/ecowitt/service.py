__all__ = ["Ecowitt"]

import logging
import platform
import re
import sys
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from functools import cached_property
from typing import Any, Self
from urllib.parse import urlencode

from pydantic import TypeAdapter, ValidationError
from ratelimit import limits, sleep_and_retry
from requests import get
from requests.exceptions import ConnectionError, HTTPError, JSONDecodeError, ReadTimeout

from weatherdan import __version__, elapsed_timer
from weatherdan.ecowitt.category import Category
from weatherdan.ecowitt.exceptions import AuthenticationError, ServiceError
from weatherdan.ecowitt.schemas import Device, LiveReading

MINUTE = 60
LOGGER = logging.getLogger(__name__)


class Ecowitt:
    API_URL = "https://api.ecowitt.net/api/v3"

    def __init__(self: Self, application_key: str, api_key: str, timeout: float = 30.0):
        self.headers = {
            "Accept": "application/json",
            "User-Agent": f"Weatherdan/{__version__}/{platform.system()}: {platform.release()}",
        }
        self.timeout = timeout
        self.application_key = application_key
        self.api_key = api_key

    @cached_property
    def device(self: Self) -> Device:
        if devices := self.list_devices():
            return devices[0]
        sys.exit("No Ecowitt device")

    @sleep_and_retry
    @limits(calls=10, period=MINUTE)
    def _perform_get_request(self: Self, url: str, params: dict[str, str]) -> dict[str, Any]:
        try:
            with elapsed_timer() as elapsed:
                response = get(url, params=params, headers=self.headers, timeout=self.timeout)

            cache_params = f"?{urlencode({k: params[k] for k in sorted(params)})}"
            for x in ["application_key=", "api_key=", "mac="]:
                if x in cache_params:
                    cache_params = re.sub(rf"(.+{x})(.+?)(&.+)", r"\1***\3", cache_params)

            msg = f"{'GET':<7} {url}{cache_params} - {response.status_code} => {elapsed():.2f}s"
            LOGGER.info(msg)

            response.raise_for_status()
            return response.json()
        except ConnectionError as err:
            msg = f"Unable to connect to '{url}'"
            raise ServiceError(msg) from err
        except HTTPError as err:
            raise ServiceError(err.response.text) from err
        except JSONDecodeError as err:
            msg = f"Unable to parse response from '{url}' as Json"
            raise ServiceError(msg) from err
        except ReadTimeout as err:
            msg = "Server took too long to respond"
            raise ServiceError(msg) from err

    def _get_request(
        self: Self,
        endpoint: str,
        params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        if params is None:
            params = {}
        params["application_key"] = self.application_key
        params["api_key"] = self.api_key

        url = self.API_URL + endpoint

        response = self._perform_get_request(url=url, params=params)
        if response["code"] != 0:
            if response["code"] == 40010:
                raise AuthenticationError(response["msg"])
            msg = f"{response['code']} | {response['msg']}"
            raise ServiceError(msg)
        return response

    def test_credentials(self: Self) -> bool:
        try:
            self.list_devices()
            return True
        except AuthenticationError:
            pass
        return False

    def list_devices(self: Self) -> list[Device]:
        try:
            results = self._retrieve_all_responses(endpoint="/device/list")
            adapter = TypeAdapter(list[Device])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def _make_history_request(
        self: Self,
        device: str,
        category: Category,
        start_date: datetime,
        end_date: datetime,
    ) -> dict[datetime, Decimal]:
        try:
            results = self._get_request(
                endpoint="/device/history",
                params={
                    "mac": device,
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "cycle_type": "30min",
                    "call_back": category.value,
                    "temp_unitid": 1,
                    "pressure_unitid": 3,
                    "wind_speed_unitid": 7,
                    "rainfall_unitid": 12,
                    "solar_irradiance_unitid": 14,
                },
            )["data"]
            if not results:
                return {}
            return {
                datetime.fromtimestamp(int(k), tz=UTC).astimezone(): Decimal(v)
                for k, v in results[category.group_1][category.group_2]["list"].items()
            }
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_history_readings(
        self: Self,
        device: str,
        category: Category,
        start_date: datetime,
    ) -> dict[datetime, Decimal]:
        all_readings = {}
        while start_date < datetime.now():
            end_date = min(start_date + timedelta(days=31), datetime.now())
            all_readings.update(
                self._make_history_request(
                    device=device,
                    category=category,
                    start_date=start_date,
                    end_date=end_date,
                ),
            )
            start_date += timedelta(days=30)
        return all_readings

    def get_live_reading(self: Self, device: str, category: Category) -> LiveReading | None:
        try:
            result = self._get_request(
                endpoint="/device/real_time",
                params={
                    "mac": device,
                    "call_back": category.value,
                    "temp_unitid": 1,
                    "pressure_unitid": 3,
                    "wind_speed_unitid": 7,
                    "rainfall_unitid": 12,
                    "solar_irradiance_unitid": 14,
                },
            )["data"]
            if not result:
                return None
            adapter = TypeAdapter(LiveReading)
            return adapter.validate_python(result[category.group_1][category.group_2])
        except ValidationError as err:
            raise ServiceError(err) from err

    def _retrieve_all_responses(
        self: Self,
        endpoint: str,
        params: dict[str, Any] | None = None,
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
