"""Plateforme Sensors pour poêle 4Fire."""
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
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
    async_add_entities([
        PoeleFumeesSensor(coordinator),
        PoelePuissanceSensor(coordinator),
        PoeleEtatSensor(coordinator),
        PoeleHeureSensor(coordinator),
        PoeleDerniereErreurSensor(coordinator),
    ])


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Configuration via YAML (rétrocompatibilité)."""
    coordinator: PoeleDataUpdateCoordinator = hass.data[DOMAIN].get("coordinator")
    if coordinator:
        async_add_entities([
            PoeleFumeesSensor(coordinator),
            PoelePuissanceSensor(coordinator),
            PoeleEtatSensor(coordinator),
            PoeleHeureSensor(coordinator),
            PoeleDerniereErreurSensor(coordinator),
        ])


class PoeleSensorBase(CoordinatorEntity[PoeleDataUpdateCoordinator], SensorEntity):
    """Classe de base pour les capteurs du poêle."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: PoeleDataUpdateCoordinator, key: str):
        super().__init__(coordinator)
        self._key = key
        self._client = coordinator.client
        self._attr_unique_id = f"{DOMAIN}_{self._client.host}_{key}"
        self._attr_device_info = coordinator.device_info


class PoeleFumeesSensor(PoeleSensorBase):
    """Capteur de température des fumées."""

    _attr_translation_key = "temp_fumees"
    _attr_name = "Température des fumées"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: PoeleDataUpdateCoordinator):
        super().__init__(coordinator, "temp_fumees")

    @property
    def native_value(self) -> int | None:
        return self._client.data.get("temp_fumees")


class PoelePuissanceSensor(PoeleSensorBase):
    """Capteur de puissance active."""

    _attr_translation_key = "puissance"
    _attr_name = "Puissance"
    _attr_icon = "mdi:fire"

    def __init__(self, coordinator: PoeleDataUpdateCoordinator):
        super().__init__(coordinator, "puissance")

    @property
    def native_value(self) -> str | None:
        return self._client.data.get("puissance")


class PoeleEtatSensor(PoeleSensorBase):
    """Capteur d'état précis."""

    _attr_translation_key = "etat"
    _attr_name = "État détaillé"
    _attr_icon = "mdi:information-outline"

    def __init__(self, coordinator: PoeleDataUpdateCoordinator):
        super().__init__(coordinator, "etat")

    @property
    def native_value(self) -> str | None:
        return self._client.data.get("etat")


class PoeleHeureSensor(PoeleSensorBase):
    """Capteur de l'horloge interne du poêle."""

    _attr_translation_key = "heure_poele"
    _attr_name = "Horloge poêle"
    _attr_icon = "mdi:clock-outline"

    def __init__(self, coordinator: PoeleDataUpdateCoordinator):
        super().__init__(coordinator, "heure_poele")

    @property
    def native_value(self) -> str | None:
        return self._client.data.get("heure_poele")


class PoeleDerniereErreurSensor(PoeleSensorBase):
    """Capteur de la dernière erreur détectée sur le poêle."""

    _attr_translation_key = "derniere_erreur"
    _attr_name = "Dernière erreur"
    _attr_icon = "mdi:alert-circle-outline"

    def __init__(self, coordinator: PoeleDataUpdateCoordinator):
        super().__init__(coordinator, "derniere_erreur")

    @property
    def native_value(self) -> str:
        err = self._client.historique_erreurs
        if not err:
            return "Aucune erreur"
        return err[0].get("libelle", "Erreur inconnue")

    @property
    def extra_state_attributes(self) -> dict:
        err = self._client.historique_erreurs
        if not err:
            return {"historique": []}
        return {
            "date_heure": err[0].get("timestamp"),
            "code_etat": err[0].get("code_etat"),
            "description": err[0].get("description"),
            "solution": err[0].get("solution"),
            "historique": err,
        }
