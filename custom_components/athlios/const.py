"""Constants for the AthliOS integration."""
from __future__ import annotations

from typing import Final, TypedDict

from homeassistant.components.sensor import (
    ATTR_STATE_CLASS,
    SensorStateClass
)

from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    ATTR_ICON,
    UnitOfSpeed,
    ATTR_SECONDS,
)

API_IMPERIAL: Final = "Imperial"
API_METRIC: Final = "Metric"
ATTR_ENABLED: Final = "enabled"
ATTR_LABEL: Final = "label"
ATTR_UNIT_IMPERIAL: Final = "unit_imperial"
ATTR_UNIT_METRIC: Final = "unit_metric"
MANUFACTURER: Final = "AthliOS, Inc."
NAME: Final = "AthliOS"
ATTRIBUTION: Final = "Data from AthliOS"
DOMAIN: Final = "athlios"
MODEL: Final = "Model"
ATTR_ICON_ALT: Final = "icon_alt"


API = {
    "protocol": "http",
    "Device": "/api/v1/device",
    "HA": "/api/v1/ha",
    "Server": "/api/v1/server",
}


BINARY_SENSOR_TYPES: Final[dict[str, SensorDescription]] = {
    "Status": {
        ATTR_DEVICE_CLASS: "athlios__occupancy",
        ATTR_ICON: "mdi:run-fast",
        ATTR_ICON_ALT: "mdi:pause-octagon",
        ATTR_LABEL: "Treadmill Status",
        ATTR_UNIT_METRIC: None,
        ATTR_UNIT_IMPERIAL: None,
        ATTR_ENABLED: True,
        ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT,
    },
    "Screensaver": {
        ATTR_DEVICE_CLASS: "athlios__screensaver",
        ATTR_ICON: "mdi:sleep",
        ATTR_ICON_ALT: "mdi:sleep-off",
        ATTR_LABEL: "Screensaver",
        ATTR_UNIT_METRIC: None,
        ATTR_UNIT_IMPERIAL: None,
        ATTR_ENABLED: True,
        ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT,
    },

}
SENSOR_TYPES: Final[dict[str, SensorDescription]] = {
    "InactiveTime": {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:information-variant",
        ATTR_LABEL: "Inactive Time",
        ATTR_UNIT_METRIC: ATTR_SECONDS,
        ATTR_UNIT_IMPERIAL: ATTR_SECONDS,
        ATTR_ENABLED: True,
        ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT,
    },
    "CurrentProfile": {
        ATTR_DEVICE_CLASS: "athlios__profile",
        ATTR_ICON: "mdi:account",
        ATTR_LABEL: "Current Profile",
        ATTR_UNIT_METRIC: None,
        ATTR_UNIT_IMPERIAL: None,
        ATTR_ENABLED: True,
        ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT,
    },
    "Workout": {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:information-variant",
        ATTR_LABEL: "Workout",
        ATTR_UNIT_METRIC: None,
        ATTR_UNIT_IMPERIAL: None,
        ATTR_ENABLED: True,
        ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT,
    },
    "Phase": {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:information-variant",
        ATTR_LABEL: "Phase",
        ATTR_UNIT_METRIC: None,
        ATTR_UNIT_IMPERIAL: None,
        ATTR_ENABLED: True,
        ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT,
    },
    "Heartrate": {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:heart-pulse",
        ATTR_LABEL: "Heart rate",
        ATTR_UNIT_METRIC: "bpm",
        ATTR_UNIT_IMPERIAL: "bpm",
        ATTR_ENABLED: True,
        ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT,
    },
    "Duration": {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:clock-start",
        ATTR_LABEL: "Duration",
        ATTR_UNIT_METRIC: None,
        ATTR_UNIT_IMPERIAL: None,
        ATTR_ENABLED: True,
        ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT,
    },
    "Speed": {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:speedometer",
        ATTR_LABEL: "Speed",
        ATTR_UNIT_METRIC: UnitOfSpeed.KILOMETERS_PER_HOUR,
        ATTR_UNIT_IMPERIAL: UnitOfSpeed.MILES_PER_HOUR,
        ATTR_ENABLED: True,
        ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT,
    },
    "Grade": {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:angle-acute",
        ATTR_LABEL: "Grade",
        ATTR_UNIT_METRIC: "%",
        ATTR_UNIT_IMPERIAL: "%",
        ATTR_ENABLED: True,
        ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT,
    },
}

class SensorDescription(TypedDict, total=False):
    """Sensor description class."""

    device_class: str | None
    icon: str | None
    icon_alt: str | None
    label: str
    unit_metric: str | None
    unit_imperial: str | None
    enabled: bool
    state_class: str | None