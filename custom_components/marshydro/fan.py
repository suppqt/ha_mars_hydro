from homeassistant.components.fan import FanEntity, FanEntityFeature
from . import _LOGGER, DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Mars Hydro fan entity."""
    api = hass.data[DOMAIN][entry.entry_id].get("api")

    if api:
        fan_entity = MarsHydroFanEntity(api, entry.entry_id)
        async_add_entities([fan_entity], update_before_add=True)
        _LOGGER.info("Mars Hydro fan entity added successfully.")
    else:
        _LOGGER.error("API instance not found. Cannot set up fan entity.")


class MarsHydroFanEntity(FanEntity):
    """Representation of a Mars Hydro fan."""

    def __init__(self, api, entry_id):
        self._api = api
        self._device_id = None
        self._device_name = None
        self._speed_percentage = None
        self._available = True
        self._entry_id = entry_id

    @property
    def name(self):
        """Return the name of the fan."""
        if self._device_name and self._device_id:
            return f"{self._device_name} Fan ({self._device_id})"
        elif self._device_name:
            return f"{self._device_name} Fan"
        return "Mars Hydro Fan"

    @property
    def available(self):
        """Return True if the fan is available."""
        return self._available

    @property
    def percentage(self):
        """Return the current speed percentage of the fan."""
        return self._speed_percentage

    @property
    def unique_id(self):
        """Return a unique ID for the fan."""
        return (
            f"{self._entry_id}_fan_{self._device_id}"
            if self._device_id
            else f"{self._entry_id}_fan"
        )

    @property
    def device_info(self):
        """Return device information for linking with the device registry."""
        if not self._device_id or not self._device_name:
            _LOGGER.warning("Device info incomplete for fan entity.")
            return None

        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._device_name,
            "manufacturer": "Mars Hydro",
            "model": "Mars Hydro Fan",
        }

    @property
    def supported_features(self):
        """Return supported features of the fan."""
        return FanEntityFeature.SET_SPEED  # Support speed adjustment only

    async def async_set_percentage(self, percentage):
        """Set the fan speed percentage."""
        if percentage < 25:
            _LOGGER.warning("Fan speed percentage below 25% is not allowed.")
            percentage = 25

        if percentage > 100:
            _LOGGER.warning("Fan speed percentage above 100% is not allowed.")
            percentage = 100

        try:
            response = await self._api.set_fanspeed(round(percentage), self._device_id)
            if response.get("code") == "000":
                self._speed_percentage = percentage
                _LOGGER.info(f"Fan speed set to {percentage}% successfully.")
            else:
                _LOGGER.error(f"Error setting fan speed: {response.get('msg')}")
        except Exception as e:
            _LOGGER.error(f"Error in async_set_percentage: {e}")
            self._available = False

    async def async_update(self):
        """Update the fan state."""
        try:
            fan_data = await self._api.safe_api_call(self._api.get_fandata)
            if fan_data:
                self._device_id = fan_data["id"]
                self._device_name = fan_data["deviceName"]
                raw_speed = fan_data.get(
                    "deviceLightRate", 25
                )  # Use deviceLightRate as the default slider value

                try:
                    # Convert speed to integer and clamp it
                    self._speed_percentage = min(max(int(raw_speed), 25), 100)
                    self._available = True
                    _LOGGER.info(
                        f"Fan state updated: {self._speed_percentage}% for {self._device_name}"
                    )
                except ValueError:
                    _LOGGER.warning(
                        f"Invalid speed data for fan {self._device_name}: {raw_speed}"
                    )
                    self._speed_percentage = None
                    self._available = False
            else:
                self._available = False
                _LOGGER.warning("Could not update fan state.")
        except Exception as e:
            self._available = False
            _LOGGER.error(f"Error updating fan state: {e}")
