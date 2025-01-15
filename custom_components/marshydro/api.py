import aiohttp
import json
import time
import logging
import asyncio

_LOGGER = logging.getLogger(__name__)


class MarsHydroAPI:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.token = None
        self.base_url = "https://api.lgledsolutions.com/api/android"
        self.api_lock = asyncio.Lock()
        self.last_login_time = 0
        self.login_interval = 300  # Minimum interval between logins in seconds
        self.device_id = None  # Added device_id attribute to store dynamically

    async def login(self):
        """Authenticate and retrieve the token."""
        async with self.api_lock:
            now = time.time()
            if self.token and (now - self.last_login_time < self.login_interval):
                _LOGGER.info("Token still valid, skipping login.")
                return

            system_data = self._generate_system_data()
            headers = {"systemData": system_data, "Content-Type": "application/json"}
            payload = {
                "email": self.email,
                "password": self.password,
                "loginMethod": "1",
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/ulogin/mailLogin/v1",
                    headers=headers,
                    json=payload,
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    _LOGGER.info("API Login Response: %s", json.dumps(data, indent=2))
                    self.token = data["data"]["token"]
                    self.last_login_time = now
                    _LOGGER.info("Login erfolgreich, Token erhalten.")

    async def safe_api_call(self, func, *args, **kwargs):
        """Ensure thread-safe API calls."""
        async with self.api_lock:
            return await func(*args, **kwargs)

    async def _ensure_token(self):
        """Ensure that the token is valid."""
        if not self.token:
            await self.login()

    async def toggle_switch(self, is_close: bool):
        """Toggle the light switch (on/off)."""
        await self._ensure_token()

        # Retrieve the dynamic device_id if not set
        if not self.device_id:
            device_data = await self.get_lightdata()
            if device_data:
                self.device_id = device_data.get("id")

        system_data = self._generate_system_data()
        headers = {
            "systemData": system_data,
            "Content-Type": "application/json",
        }
        payload = {
            "isClose": is_close,
            "deviceId": self.device_id,  # Use dynamic device_id
            "groupId": None,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/udm/lampSwitch/v1", headers=headers, json=payload
            ) as response:
                response_json = await response.json()
                _LOGGER.info(
                    "API Toggle Switch Response: %s",
                    json.dumps(response_json, indent=2),
                )
                if response_json.get("code") == "102":  # Handle token expiration
                    _LOGGER.warning("Token expired, re-authenticating...")
                    await self.login()
                    return await self.toggle_switch(is_close)
                return response_json

    async def get_lightdata(self):
        """Retrieve light data from the Mars Hydro API."""
        await self._ensure_token()
        system_data = self._generate_system_data()
        headers = {
            "Accept-Encoding": "gzip",
            "Content-Type": "application/json",
            "Host": "api.lgledsolutions.com",
            "User-Agent": "Python/3.x",
            "systemData": system_data,
        }
        payload = {"currentPage": 0, "type": None, "productType": "LIGHT"}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/udm/getDeviceList/v1", headers=headers, json=payload
            ) as response:
                response_json = await response.json()
                _LOGGER.info(
                    "API Get Light Data Response: %s",
                    json.dumps(response_json, indent=2),
                )

                if response_json.get("code") == "000":
                    device_list = response_json.get("data", {}).get("list", [])
                    if device_list:
                        device_data = device_list[0]
                        self.device_id = device_data.get(
                            "id"
                        )  # Store dynamic device_id
                        return {
                            "deviceName": device_data.get("deviceName"),
                            "deviceLightRate": device_data.get("deviceLightRate"),
                            "isClose": device_data.get("isClose"),
                            "id": self.device_id,
                        }
                    else:
                        _LOGGER.warning("No devices found.")
                        return None
                else:
                    _LOGGER.error("Error in API response: %s", response_json.get("msg"))
                    return None

    async def set_brightness(self, brightness):
        """Set the brightness of the Mars Hydro light."""
        await self._ensure_token()

        # Retrieve the dynamic device_id if not set
        if not self.device_id:
            device_data = await self.get_lightdata()
            if device_data:
                self.device_id = device_data.get("id")

        system_data = self._generate_system_data()
        headers = {
            "Accept-Encoding": "gzip",
            "Content-Type": "application/json",
            "Host": "api.lgledsolutions.com",
            "systemData": system_data,
            "User-Agent": "Python/3.x",
        }
        payload = {
            "light": brightness,
            "deviceId": self.device_id,  # Use dynamic device_id
            "groupId": None,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/udm/adjustLight/v1", headers=headers, json=payload
            ) as response:
                response_json = await response.json()
                _LOGGER.info(
                    "API Set Brightness Response: %s",
                    json.dumps(response_json, indent=2),
                )
                return response_json

    def _generate_system_data(self):
        """Generate systemData payload with dynamic device_id."""
        return json.dumps(
            {
                "reqId": int(time.time() * 1000),
                "appVersion": "1.2.0",
                "osType": "android",
                "osVersion": "14",
                "deviceType": "SM-S928C",
                "deviceId": self.device_id,  # Use dynamic device_id here
                "netType": "wifi",
                "wifiName": "123",
                "timestamp": int(time.time()),
                "token": self.token,
                "timezone": "Europe/Berlin",
                "language": "German",
            }
        )
