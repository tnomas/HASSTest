"""Sensor platform for Dummy Integration."""
from __future__ import annotations

import logging
import random
from datetime import timedelta

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN, DEFAULT_SENSOR_VALUE

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=30)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Dummy sensor platform."""
    async_add_entities([DummySensor()], True)


class DummySensor(SensorEntity):
    """Representation of a Dummy Sensor."""

    _attr_has_entity_name = True
    _attr_name = "Dummy Temperature"
    _attr_unique_id = "dummy_integration_sensor_temperature"
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_suggested_display_precision = 1

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._attr_native_value = DEFAULT_SENSOR_VALUE

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This simulates a temperature sensor that fluctuates randomly.
        """
        # Simulate temperature fluctuation between 18 and 28 degrees
        self._attr_native_value = round(
            DEFAULT_SENSOR_VALUE + random.uniform(-6, 6), 1
        )
        _LOGGER.debug("Dummy sensor updated: %s", self._attr_native_value)
