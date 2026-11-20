"""Intégration Home Assistant pour poêle 4Fire / HottoH (TiEmme)."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import CONF_HOST, CONF_NAME, CONF_PORT, DEFAULT_HOST, DEFAULT_NAME, DEFAULT_PORT, DOMAIN
from .coordinator import PoeleClient, PoeleDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.CLIMATE, Platform.SENSOR]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Configuration YAML (rétrocompatibilité)."""
    hass.data.setdefault(DOMAIN, {})

    if DOMAIN in config:
        conf = config[DOMAIN]
        host = conf.get(CONF_HOST, DEFAULT_HOST)
        port = conf.get(CONF_PORT, DEFAULT_PORT)
        name = conf.get(CONF_NAME, DEFAULT_NAME)

        client = PoeleClient(host, port)
        coordinator = PoeleDataUpdateCoordinator(hass, client, name)
        await coordinator.async_config_entry_first_refresh()

        hass.data[DOMAIN]["coordinator"] = coordinator
        hass.data[DOMAIN]["client"] = client

        for platform in PLATFORMS:
            hass.async_create_task(
                hass.helpers.discovery.async_load_platform(platform, DOMAIN, {}, config)
            )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configuration via Config Flow UI."""
    hass.data.setdefault(DOMAIN, {})

    host = entry.data.get(CONF_HOST, DEFAULT_HOST)
    port = entry.data.get(CONF_PORT, DEFAULT_PORT)
    name = entry.data.get(CONF_NAME, DEFAULT_NAME)

    client = PoeleClient(host, port)
    coordinator = PoeleDataUpdateCoordinator(hass, client, name)

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Déchargement d'une entrée de configuration."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok
