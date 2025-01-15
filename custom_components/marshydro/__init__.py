from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers import device_registry as dr
from .const import DOMAIN
import logging
from .api import MarsHydroAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["switch", "light", "sensor"]  # Sensor hinzugefügt


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
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, "mars_hydro_device")},
        manufacturer="Mars Hydro",
        name="Mars Hydro Light",
        model="Mars Hydro FC3000",
    )

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
