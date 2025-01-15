from homeassistant.components.light import LightEntity, ATTR_BRIGHTNESS
from . import _LOGGER, DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Mars Hydro Light entity."""
    _LOGGER.debug("Mars Hydro Light async_setup_entry called")

    api = hass.data[DOMAIN][entry.entry_id].get("api")

    if api:
        light = MarsHydroBrightnessLight(api, entry.entry_id)
        async_add_entities([light], update_before_add=True)


class MarsHydroBrightnessLight(LightEntity):
    """Representation of the Mars Hydro Light with brightness control only."""

    def __init__(self, api, entry_id):
        self._api = api
        self._name = "Mars Hydro Brightness Light"
        self._device_id = None  # To store the dynamic device_id
        self._brightness = None
        self._available = False
        self._state = None
        self._entry_id = entry_id

    @property
    def name(self):
        """Return the name of the light, dynamically including device_id."""
        # Include device_id in the name dynamically once available
        return f"{self._name} ({self._device_id})" if self._device_id else self._name

    @property
    def brightness(self):
        """Return the brightness of the light (0-255)."""
        return self._brightness

    @property
    def available(self):
        """Return True if entity is available."""
        return self._available

    @property
    def is_on(self):
        """Return True if the light is on."""
        return self._state

    @property
    def unique_id(self):
        """Return a unique ID for the light."""
        return f"{self._entry_id}_light"

    @property
    def device_info(self):
        """Return device information for linking with the device registry."""
        # Device information remains static
        return {
            "identifiers": {(DOMAIN, "mars_hydro_device")},
            "name": "Mars Hydro Light",  # Keeping the device name consistent
            "manufacturer": "Mars Hydro",
            "model": "Mars Hydro",
        }

    @property
    def supported_color_modes(self):
        """Return the list of supported color modes."""
        return {"brightness"}

    @property
    def color_mode(self):
        """Return the current color mode."""
        return "brightness"

    async def async_turn_on(self, **kwargs):
        """Turn on the light by setting the brightness."""
        brightness = kwargs.get(ATTR_BRIGHTNESS, 255)  # Default to max brightness
        await self.async_set_brightness(brightness)
        self._state = True

    async def async_turn_off(self, **kwargs):
        """Turn off the light by setting brightness to 0."""
        await self.async_set_brightness(0)
        self._state = False

    async def async_set_brightness(self, brightness: int):
        """Set the brightness of the light."""
        try:
            brightness_percentage = round((brightness / 255) * 100)
            response = await self._api.safe_api_call(
                self._api.set_brightness, brightness_percentage
            )
            if response.get("code") == "102":
                _LOGGER.warning("Token expired, re-authenticating...")
                await self._api.login()
                response = await self._api.safe_api_call(
                    self._api.set_brightness, brightness_percentage
                )

            if response.get("code") != "000":
                raise Exception(f"API Error: {response.get('msg')}")

            self._brightness = brightness
            self._state = brightness > 0
            self._available = True
            _LOGGER.info(f"Brightness set to {brightness_percentage}%")
        except Exception as e:
            self._available = False
            _LOGGER.error(f"Error setting brightness: {e}")

    async def async_update(self):
        """Update the light's state."""
        try:
            light_data = await self._api.safe_api_call(self._api.get_lightdata)
            if light_data:
                self._device_id = light_data[
                    "id"
                ]  # Set device_id dynamically from the API response
                self._brightness = int((light_data["deviceLightRate"] / 100) * 255)
                self._state = not light_data["isClose"]
                self._available = True
                _LOGGER.info(f"Updated brightness: {self._brightness}")
            else:
                self._available = False
                self._state = None
                _LOGGER.warning("Couldn't retrieve light data")
        except Exception as e:
            self._available = False
            self._state = None
            _LOGGER.error(f"Error updating light state: {e}")
