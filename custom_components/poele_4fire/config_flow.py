"""Flux de configuration (Config Flow) pour le Poêle 4Fire."""
import logging
import socket
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_HOST,
    CONF_NAME,
    CONF_PORT,
    DEFAULT_HOST,
    DEFAULT_NAME,
    DEFAULT_PORT,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


def test_connection(host: str, port: int) -> bool:
    """Tente une connexion rapide avec le poêle pour valider l'IP et le port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3.5)
            s.connect((host, port))
            s.sendall(b'["2WL","0"]')
            resp = s.recv(512)
            return b"2WL" in resp
    except Exception as err:
        _LOGGER.warning("Échec de connexion au poêle %s:%s: %s", host, port, err)
        return False


class Poele4FireConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Gestionnaire de flux de configuration pour 4Fire."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Étape initiale de saisie par l'utilisateur."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST].strip()
            port = user_input[CONF_PORT]
            name = user_input.get(CONF_NAME, DEFAULT_NAME).strip()

            # Vérifier si l'hôte est déjà configuré
            await self.async_set_unique_id(f"{DOMAIN}_{host}")
            self._abort_if_unique_id_configured()

            # Test de connexion
            can_connect = await self.hass.async_add_executor_job(
                test_connection, host, port
            )

            if can_connect:
                return self.async_create_entry(
                    title=name,
                    data={
                        CONF_HOST: host,
                        CONF_PORT: port,
                        CONF_NAME: name,
                    },
                )
            errors["base"] = "cannot_connect"

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
                vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    async def async_step_import(self, import_data: dict[str, Any]) -> FlowResult:
        """Importation automatique depuis configuration.yaml."""
        host = import_data.get(CONF_HOST, DEFAULT_HOST)
        await self.async_set_unique_id(f"{DOMAIN}_{host}")
        self._abort_if_unique_id_configured()
        return self.async_create_entry(
            title=import_data.get(CONF_NAME, DEFAULT_NAME),
            data=import_data,
        )
