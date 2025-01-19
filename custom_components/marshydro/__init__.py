from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers import device_registry as dr
from .const import DOMAIN
import logging
from .api import MarsHydroAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor", "light", "switch", "fan"]  # Sensor hinzugefügt


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Setup für die Mars Hydro-Integration."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Mars Hydro integration from a config entry."""
    email = entry.data["email"]
    password = entry.data["password"]

    api = MarsHydroAPI(email, password)
    await api.login()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {"api": api}

    # Gerät registrieren
    device_registry = dr.async_get(hass)

    # Light-Gerät registrieren
    light_data = await api.get_lightdata()
    if light_data:
        device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            identifiers={(DOMAIN, light_data["id"])},
            manufacturer="Mars Hydro",
            name=light_data["deviceName"],
            model="Mars Hydro Light",
        )
        _LOGGER.info(
            f"Light Device {light_data['deviceName']} wurde erfolgreich registriert."
        )
    else:
        _LOGGER.warning("Kein Light-Gerät gefunden, Registrierung übersprungen.")

    # Fan-Gerät registrieren
    fan_data = await api.get_fandata()
    if fan_data:
        device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            identifiers={(DOMAIN, fan_data["id"])},
            manufacturer="Mars Hydro",
            name=fan_data["deviceName"],
            model="Mars Hydro Fan",
        )
        _LOGGER.info(
            f"Fan Device {fan_data['deviceName']} wurde erfolgreich registriert."
        )
    else:
        _LOGGER.warning("Kein Fan-Gerät gefunden, Registrierung übersprungen.")

    # Plattformen laden
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Entferne eine Konfigurationsinstanz."""
    _LOGGER.debug("Mars Hydro async_unload_entry wird aufgerufen")

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def create_api_instance(hass: HomeAssistant, email: str, password: str):
    """Erstelle eine API-Instanz und führe den Login durch."""
    try:
        api_instance = MarsHydroAPI(email, password)
        await api_instance.login()
        return api_instance
    except Exception as e:
        _LOGGER.error(f"Fehler beim Erstellen der API-Instanz: {e}")
        return None
