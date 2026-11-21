"""Plateforme Binary Sensor pour poêle 4Fire."""
import logging

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import PoeleDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configuration via Config Entry UI."""
    coordinator: PoeleDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([PoeleAlarmeSensor(coordinator)])


class PoeleAlarmeSensor(CoordinatorEntity[PoeleDataUpdateCoordinator], BinarySensorEntity):
    """Capteur binaire d'alarme / sécurité du poêle."""

    _attr_has_entity_name = True
    _attr_name = "Alarme"
    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_icon = "mdi:alert"

    def __init__(self, coordinator: PoeleDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._client = coordinator.client
        self._attr_unique_id = f"{DOMAIN}_{self._client.host}_alarme"
        self._attr_device_info = coordinator.device_info

    @property
    def is_on(self) -> bool:
        """Retourne True si le poêle est en état d'alarme ou de sécurité."""
        return self._client.data.get("code_etat", 0) in (8, 9)

    @property
    def extra_state_attributes(self) -> dict:
        err = self._client.historique_erreurs
        if not err:
            return {}
        return {
            "derniere_erreur": err[0].get("libelle"),
            "date_heure": err[0].get("timestamp"),
            "solution": err[0].get("solution"),
        }
