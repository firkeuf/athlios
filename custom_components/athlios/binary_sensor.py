
"""Platform for sensor integration."""
from homeassistant.const import ATTR_ATTRIBUTION, ATTR_DEVICE_CLASS, ATTR_ICON, CONF_NAME, ATTR_MODEL
from homeassistant.components.sensor import ATTR_STATE_CLASS
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.device_registry import DeviceEntryType


import logging

from .const import (
    DOMAIN,
    BINARY_SENSOR_TYPES,
    ATTR_LABEL,
    ATTRIBUTION,
    MANUFACTURER,
    ATTR_ENABLED,
    ATTR_ICON_ALT,
)
from . import AthliOSDataUpdateCoordinator


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    name: str = entry.data[CONF_NAME]
    coordinator: AthliOSDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    sensors: list[AthliOSSensor] = []
    for sensor in BINARY_SENSOR_TYPES:
        sensors.append(AthliOSSensor(name, sensor, coordinator))
    async_add_entities(sensors)


class AthliOSSensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Sensor."""
    coordinator: AthliOSDataUpdateCoordinator

    def __init__( self, name: str, kind: str, coordinator: AthliOSDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_data = coordinator.data
        self._description = BINARY_SENSOR_TYPES[kind]
        self._name = name
        self.kind = kind
        self._device_class = None
        self._attrs = {ATTR_ATTRIBUTION: ATTRIBUTION}
        self._attr_state_class = self._description.get(ATTR_STATE_CLASS)
        self._attr_is_on = False

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        self._sensor_data = self.coordinator.data
        return self.coordinator.data.get(self.kind)

    @property
    def name(self) -> str:
        """Return the name."""
        name = f"{self._name} {self._description[ATTR_LABEL]}"
        return name

    @property
    def device_class(self):
        return self._description[ATTR_DEVICE_CLASS]

    @property
    def icon(self):
        """Return the icon."""
        if not self.is_on and self._description.get(ATTR_ICON_ALT):
            return self._description.get(ATTR_ICON_ALT)
        return self._description[ATTR_ICON]

    @property
    def unique_id(self) -> str:
        """Return a unique_id for this entity."""
        return f"{self.coordinator.config_entry.data.get('basis_id')}-{self.kind}".lower()

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, self.coordinator.config_entry.unique_id)},
            "name": f"{self.coordinator.config_entry.data.get(CONF_NAME)}",
            "manufacturer": MANUFACTURER,
            "model": self.coordinator.config_entry.data.get(ATTR_MODEL),
            "entry_type": DeviceEntryType.SERVICE,
        }

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if the entity should be enabled when first added to the entity registry."""
        return self._description[ATTR_ENABLED]
