from homeassistant.components.switch import SwitchEntity
from . import _LOGGER, DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the switch platform."""
    api = hass.data[DOMAIN][entry.entry_id].get("api")

    if api:
        switch = MarsHydroSwitch(api, entry.entry_id)
        async_add_entities([switch], update_before_add=True)


class MarsHydroSwitch(SwitchEntity):
    """Representation of a Mars Hydro switch."""

    def __init__(self, api, entry_id):
        self._api = api
        self._name = "Mars Hydro Switch"
        self._state = None
        self._available = True
        self._entry_id = entry_id
        self._device_id = None  # To store the dynamic device_id

    @property
    def name(self):
        """Return the name of the switch, dynamically including device_id."""
        # Only change the entity name, not the device name in the registry
        return f"{self._name} ({self._device_id})" if self._device_id else self._name

    @property
    def is_on(self):
        """Return True if the switch is on."""
        return self._state

    @property
    def available(self):
        """Return True if the switch is available."""
        return self._available

    @property
    def unique_id(self):
        """Return a unique ID for the switch."""
        return f"{self._entry_id}_switch"

    @property
    def device_info(self):
        """Return device information for linking with the device registry."""
        # Keep the device name static in the registry
        return {
            "identifiers": {(DOMAIN, "mars_hydro_device")},
            "name": "Mars Hydro Light",  # Keeping the device name unchanged
            "manufacturer": "Mars Hydro",
            "model": "Mars Hydro",
        }

    async def async_turn_on(self, **kwargs):
        """Turn the device on."""
        try:
            response = await self._api.safe_api_call(self._api.toggle_switch, False)
            if response.get("code") == "000":
                self._state = True
                _LOGGER.info("Switch turned on successfully.")
            else:
                _LOGGER.error(f"Error turning on switch: {response.get('msg')}")
        except Exception as e:
            _LOGGER.error(f"Error in async_turn_on: {e}")
            self._available = False

    async def async_turn_off(self, **kwargs):
        """Turn the device off."""
        try:
            response = await self._api.safe_api_call(self._api.toggle_switch, True)
            if response.get("code") == "000":
                self._state = False
                _LOGGER.info("Switch turned off successfully.")
            else:
                _LOGGER.error(f"Error turning off switch: {response.get('msg')}")
        except Exception as e:
            _LOGGER.error(f"Error in async_turn_off: {e}")
            self._available = False

    async def async_update(self):
        """Update the state of the switch."""
        try:
            light_data = await self._api.safe_api_call(self._api.get_lightdata)
            if light_data:
                self._device_id = light_data["id"]  # Set device_id dynamically
                self._state = not light_data["isClose"]
                self._available = True
                _LOGGER.info(f"Switch state updated: {'ON' if self._state else 'OFF'}")
            else:
                _LOGGER.warning("Could not update switch state.")
                self._available = False
        except Exception as e:
            _LOGGER.error(f"Error updating switch state: {e}")
            self._available = False
