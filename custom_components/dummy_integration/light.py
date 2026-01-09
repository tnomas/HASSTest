"""Light platform for Dummy Integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ColorMode,
    LightEntity,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN, DEFAULT_BRIGHTNESS

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Dummy light platform from YAML."""
    data = hass.data.get(DOMAIN)
    if data is None:
        _LOGGER.error("Dummy integration data not found")
        return

    light = DummyLight(data)
    async_add_entities([light], True)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Dummy light platform from config entry."""
    data = hass.data.get(DOMAIN)
    if data is None:
        _LOGGER.error("Dummy integration data not found")
        return

    light = DummyLight(data)
    async_add_entities([light], True)


class DummyLight(LightEntity):
    """Representation of a Dummy Light."""

    _attr_has_entity_name = True
    _attr_name = "Dummy Light"
    _attr_unique_id = "dummy_integration_light"
    _attr_color_mode = ColorMode.BRIGHTNESS
    _attr_supported_color_modes = {ColorMode.BRIGHTNESS}

    def __init__(self, data) -> None:
        """Initialize the light."""
        self._data = data
        self._attr_is_on = data.light_is_on
        self._attr_brightness = data.light_brightness

    async def async_added_to_hass(self) -> None:
        """Register callbacks when entity is added."""
        self._data.add_listener(self._handle_state_change)

    async def async_will_remove_from_hass(self) -> None:
        """Clean up when entity is removed."""
        self._data.remove_listener(self._handle_state_change)

    @callback
    def _handle_state_change(self) -> None:
        """Handle state change from shared data."""
        self._attr_is_on = self._data.light_is_on
        self._attr_brightness = self._data.light_brightness
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the light on."""
        self._data.light_is_on = True

        if ATTR_BRIGHTNESS in kwargs:
            self._data.light_brightness = kwargs[ATTR_BRIGHTNESS]

        self._attr_is_on = True
        self._attr_brightness = self._data.light_brightness

        self._data.notify_listeners()
        _LOGGER.debug("Dummy light turned on with brightness %s", self._attr_brightness)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the light off."""
        self._data.light_is_on = False
        self._attr_is_on = False

        self._data.notify_listeners()
        _LOGGER.debug("Dummy light turned off")

    async def async_update(self) -> None:
        """Fetch new state data for the light."""
        self._attr_is_on = self._data.light_is_on
        self._attr_brightness = self._data.light_brightness
