"""Config flow for AthliOS integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME, ATTR_MODEL

from .const import DOMAIN, API
from .athlios import async_get, CannotConnect

_LOGGER = logging.getLogger(__name__)


class PlaceholderHub:
    """Placeholder class to make tests pass.

    TODO Remove this placeholder class and replace with things from your PyPI package.
    """

    def __init__(self, host: str) -> None:
        """Initialize."""
        self.host = host


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """

    host = data.get(CONF_HOST)
    port = data.get(CONF_PORT)
    response = await async_get(hass, f'{host}:{port}', API['Device'], API['protocol'])
    serial = response.get('serial')
    if serial is None:
        raise CannotConnect
    basis_id = response.get('basis_id')
    name = data.get(CONF_NAME)
    title = f'{data.get(CONF_NAME)} Basis ID {basis_id}'
    model = response.get(ATTR_MODEL)

    return {
        CONF_NAME: name,
        "title": title,
        CONF_HOST: data[CONF_HOST],
        CONF_PORT: data[CONF_PORT],
        'serial': serial,
        'basis_id': basis_id,
        ATTR_MODEL: model,
    }


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Sora."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=self.data_schema
            )
        errors = {}
        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except Exception:
            errors["base"] = "unknown"
        else:
            await self.async_set_unique_id(info['serial'])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=info["title"], data=info)

        return self.async_show_form(
            step_id="user", data_schema=self.data_schema, errors=errors
        )

    @property
    def data_schema(self):
        return  vol.Schema(
            {
                vol.Required(CONF_HOST, default='192.168.19.14'): str,
                vol.Required(CONF_PORT, default='5678'): str,
                vol.Optional(CONF_NAME, default=f'AthliOS {self.hass.config.location_name}'): str,
            }
        )





