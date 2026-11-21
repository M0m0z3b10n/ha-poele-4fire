"""Coordinateur de données pour le Poêle 4Fire / TiEmme."""
import asyncio
import json
import logging
import socket
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, ETATS_POELE, MAX_TEMP, MIN_TEMP, SCAN_INTERVAL_SECONDS

_LOGGER = logging.getLogger(__name__)


class PoeleClient:
    """Client de communication TCP local avec le poêle (port 80)."""

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self._lock = asyncio.Lock()
        self.data = {
            "code_etat": 0,
            "etat": "Éteint",
            "temp_amb": 20.0,
            "consigne_temp": 20.0,
            "consigne_min": 10.0,
            "consigne_max": 40.0,
            "temp_fumees": 0,
            "puissance": "P5",
            "heure_poele": "--:--",
        }

    def _sync_send(self, trame: bytes, wait_resp=True) -> str:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(4.0)
            s.connect((self.host, self.port))
            s.sendall(trame)
            if wait_resp:
                return s.recv(4096).decode("utf-8", errors="ignore")
            return ""

    async def async_send(self, trame: bytes, wait_resp=True) -> str:
        async with self._lock:
            loop = asyncio.get_running_loop()
            resp = await loop.run_in_executor(None, self._sync_send, trame, wait_resp)
            await asyncio.sleep(0.4)
            return resp

    async def async_update(self) -> dict:
        """Lit la télémétrie complète du poêle."""
        raw = await self.async_send(b'["2WL","0"]')
        data = json.loads(raw)
        trames = data[2:]

        for trame in trames:
            # Trame principale de fonctionnement (#01)
            if trame.startswith("10") and len(trame) >= 24:
                code_etat = int(trame[10:12], 16)
                self.data["code_etat"] = code_etat
                self.data["etat"] = ETATS_POELE.get(code_etat, f"Code {code_etat}")
                self.data["temp_fumees"] = int(trame[8:10], 16)
                self.data["puissance"] = f"P{int(trame[14:16], 16)}"
                self.data["heure_poele"] = f"{trame[16:18]}:{trame[18:20]}"
                self.data["temp_amb"] = int(trame[20:24], 16) / 10.0
            # Sonde fumées précise
            elif trame.startswith("12ffff") and len(trame) >= 10:
                self.data["temp_fumees"] = int(trame[6:10], 16)
            # Sonde température ambiante précise
            elif trame.startswith("12fff7") and len(trame) >= 10:
                self.data["temp_amb"] = int(trame[6:10], 16) / 10.0
            # Consigne de température (registre 005a)
            elif trame.startswith("12005a") and len(trame) >= 18:
                self.data["consigne_temp"] = int(trame[6:10], 16) / 10.0
                self.data["consigne_min"] = int(trame[10:14], 16) / 10.0
                self.data["consigne_max"] = int(trame[14:18], 16) / 10.0

        return self.data

    async def async_set_temperature(self, temp: float):
        """Définit la température de consigne au dixième de degré (bridée à MAX_TEMP pour sécurité)."""
        val = max(MIN_TEMP, min(MAX_TEMP, temp))
        val_hex = f"{int(round(val * 10)):04x}"
        trame = f'["2WC","1","0512005a{val_hex}006401900001000100"]'.encode("utf-8")
        _LOGGER.debug("Envoi consigne au poêle: %.1f °C (%s)", val, trame)
        await self.async_send(trame)
        self.data["consigne_temp"] = val

    async def async_turn_on(self):
        """Allume le poêle."""
        _LOGGER.debug("Envoi ordre Allumage (05040000)")
        await self.async_send(b'["2WC","1","05040000"]')

    async def async_turn_off(self):
        """Éteint le poêle."""
        _LOGGER.debug("Envoi ordre Extinction (05050000)")
        await self.async_send(b'["2WC","1","05050000"]')


class PoeleDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinateur gérant les mises à jour périodiques."""

    def __init__(self, hass: HomeAssistant, client: PoeleClient, name: str, entry: ConfigEntry | None = None):
        super().__init__(
            hass,
            _LOGGER,
            name=name,
            update_interval=timedelta(seconds=SCAN_INTERVAL_SECONDS),
            config_entry=entry,
        )
        self.client = client
        self.device_name = name

    async def _async_update_data(self) -> dict:
        try:
            return await self.client.async_update()
        except Exception as err:
            raise UpdateFailed(f"Erreur de communication avec le poêle: {err}") from err

    @property
    def device_info(self) -> DeviceInfo:
        """Informations de l'appareil pour Home Assistant."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.client.host)},
            name=self.device_name,
            manufacturer="4Fire / TiEmme",
            model="WiFire / SY250 (Protocole 2WL/2WC)",
        )
