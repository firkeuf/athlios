"""The AthliOS integration."""
from __future__ import annotations

from typing import Any, Dict
from datetime import timedelta
from asyncio import gather

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.const import CONF_HOST, CONF_PORT

from .const import DOMAIN, API
from .athlios import async_get

import logging


_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["binary_sensor", "sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AthliOS from a config entry."""
    coordinator = AthliOSDataUpdateCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()
    entry.async_on_unload(entry.add_update_listener(update_listener))
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update listener."""
    await hass.config_entries.async_reload(entry.entry_id)


class AthliOSDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from AthliOS API."""
    def __init__(self, hass: HomeAssistant, ) -> None:
        """Initialize."""
        update_interval = timedelta(seconds=2)
        self.is_metric = hass.config.units.is_metric
        _LOGGER.debug("Data will be update every %s", update_interval)
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=update_interval)

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        host = self.config_entry.data.get(CONF_HOST)
        port = self.config_entry.data.get(CONF_PORT)
        task_ha = async_get(self.hass, f'{host}:{port}', API['HA'], API['protocol'])
        task_s = async_get(self.hass, f'{host}:{port}', API['Server'], API['protocol'])
        response_ha, response_s = await gather(task_ha, task_s)

        result = {}

        result.update({"CurrentProfile": "empty" if not response_ha.get('current_profile') else "%(first_name)s %(last_name)s" % response_ha.get('current_profile')})
        result.update({"Status": True if response_ha.get('workout') else False})
        result.update({"Screensaver": True if response_ha.get('screensaver') else False})
        result.update({"Workout": response_ha.get('workout').get('current_preset_name') if type(response_ha.get('workout')) == dict else None})
        result.update({"Phase": response_ha.get('workout').get('current_phase_name') if type(response_ha.get('workout')) == dict else None})
        if result.get("Workout") == "Manual":
            result["Phase"] = None

        result.update({"Heartrate": response_ha.get('workout').get('heart_rate') if type(response_ha.get('workout')) == dict else None})
        result.update({"Duration": timedelta(seconds=round(response_ha.get('workout').get('duration'))) if type(response_ha.get('workout')) == dict else None})
        result.update({"Speed": response_ha.get('workout').get('speed') if type(response_ha.get('workout')) == dict else 0})
        result.update({"Grade": response_ha.get('workout').get('grade') if type(response_ha.get('workout')) == dict else 0})
        result.update({"InactiveTime": response_s.get('inactive_time')})
        return result
