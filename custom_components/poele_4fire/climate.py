"""Plateforme Climate pour poêle 4Fire."""
import logging
from typing import Any

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PRECISION_TENTHS, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DEFAULT_NAME, DOMAIN
from .coordinator import PoeleDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configuration via l'interface UI (Config Entry)."""
    coordinator: PoeleDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([Poele4FireClimate(coordinator)])


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Configuration via YAML (rétrocompatibilité)."""
    coordinator: PoeleDataUpdateCoordinator = hass.data[DOMAIN].get("coordinator")
    if coordinator:
        async_add_entities([Poele4FireClimate(coordinator)])


class Poele4FireClimate(CoordinatorEntity[PoeleDataUpdateCoordinator], ClimateEntity):
    """Entité Climate pour le poêle 4Fire."""

    _attr_has_entity_name = True
    _attr_name = None  # Utilise le nom de l'appareil
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_precision = PRECISION_TENTHS
    _attr_target_temperature_step = 0.1
    _attr_min_temp = 10.0
    _attr_max_temp = 40.0
    _attr_hvac_modes = [HVACMode.OFF, HVACMode.HEAT]
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.TURN_ON
        | ClimateEntityFeature.TURN_OFF
    )

    def __init__(self, coordinator: PoeleDataUpdateCoordinator):
        super().__init__(coordinator)
        self._client = coordinator.client
        self._attr_unique_id = f"{DOMAIN}_{self._client.host}_climate"
        self._attr_device_info = coordinator.device_info

    @property
    def current_temperature(self) -> float | None:
        return self._client.data.get("temp_amb")

    @property
    def target_temperature(self) -> float | None:
        return self._client.data.get("consigne_temp")

    @property
    def hvac_mode(self) -> HVACMode:
        code = self._client.data.get("code_etat", 0)
        # 0 = Éteint, 5 = Extinction, 7 = Veille, 8 = Alarme
        if code in (0, 5, 7, 8):
            return HVACMode.OFF
        return HVACMode.HEAT

    @property
    def hvac_action(self) -> HVACAction:
        code = self._client.data.get("code_etat", 0)
        if code in (4, 6):
            return HVACAction.HEATING
        if code in (1, 2, 3):
            return HVACAction.PREHEATING
        if code in (0, 5, 7, 8):
            return HVACAction.OFF
        return HVACAction.IDLE

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {
            "etat_detaille": self._client.data.get("etat"),
            "code_etat": self._client.data.get("code_etat"),
            "puissance": self._client.data.get("puissance"),
            "temp_fumees": self._client.data.get("temp_fumees"),
            "heure_poele": self._client.data.get("heure_poele"),
        }

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Définit la température de consigne (et allume si demandé)."""
        temp = kwargs.get("temperature")
        hvac_mode = kwargs.get("hvac_mode")

        if hvac_mode == HVACMode.HEAT:
            await self._client.async_turn_on()
        elif hvac_mode == HVACMode.OFF:
            await self._client.async_turn_off()

        if temp is not None:
            await self._client.async_set_temperature(float(temp))

        await self.coordinator.async_request_refresh()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Change le mode HVAC (ON / OFF)."""
        if hvac_mode == HVACMode.HEAT:
            await self._client.async_turn_on()
        elif hvac_mode == HVACMode.OFF:
            await self._client.async_turn_off()

        await self.coordinator.async_request_refresh()

    async def async_turn_on(self) -> None:
        """Allume le poêle."""
        await self._client.async_turn_on()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        """Éteint le poêle."""
        await self._client.async_turn_off()
        await self.coordinator.async_request_refresh()
