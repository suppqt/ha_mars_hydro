from homeassistant.components.sensor import SensorEntity
from . import _LOGGER, DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Mars Hydro brightness sensor."""
    api = hass.data[DOMAIN][entry.entry_id].get("api")

    if api:
        sensor = MarsHydroBrightnessSensor(api, entry.entry_id)
        async_add_entities([sensor], update_before_add=True)


class MarsHydroBrightnessSensor(SensorEntity):
    """Representation of the Mars Hydro brightness sensor."""

    def __init__(self, api, entry_id):
        self._api = api
        self._device_id = None  # To store the dynamic device_id
        self._name = "Mars Hydro Brightness"
        self._brightness = None
        self._available = True
        self._entry_id = entry_id

    @property
    def name(self):
        """Return the name of the sensor, dynamically including device_id."""
        # Include device_id in the name dynamically once available, without modifying the device name
        return f"{self._name} ({self._device_id})" if self._device_id else self._name

    @property
    def native_value(self):
        """Return the brightness value."""
        return self._brightness

    @property
    def available(self):
        """Return True if the sensor is available."""
        return self._available

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement."""
        return "%"

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return f"{self._entry_id}_brightness_sensor"

    @property
    def device_info(self):
        """Return device information for linking with the device registry."""
        # Device information does not change, only the entity name is affected
        return {
            "identifiers": {(DOMAIN, "mars_hydro_device")},
            "name": "Mars Hydro Light",  # Keeping the original device name intact
            "manufacturer": "Mars Hydro",
            "model": "Mars Hydro",
        }

    async def async_update(self):
        """Update the sensor state."""
        try:
            light_data = await self._api.safe_api_call(self._api.get_lightdata)
            if light_data:
                self._device_id = light_data[
                    "id"
                ]  # Set device_id dynamically from the API response
                self._brightness = light_data["deviceLightRate"]
                self._available = True
                _LOGGER.info(f"Brightness sensor updated: {self._brightness}%")
            else:
                self._available = False
                _LOGGER.warning("Could not update brightness sensor.")
        except Exception as e:
            self._available = False
            _LOGGER.error(f"Error updating brightness sensor: {e}")
