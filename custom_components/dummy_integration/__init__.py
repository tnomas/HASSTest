"""The Dummy Integration component."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, ATTR_LIGHT_STATE, ATTR_LIGHT_BRIGHTNESS, DEFAULT_BRIGHTNESS

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.LIGHT, Platform.SWITCH]


class DummyIntegrationData:
    """Class to hold shared data for the dummy integration."""

    def __init__(self) -> None:
        """Initialize the shared data."""
        self.light_is_on: bool = False
        self.light_brightness: int = DEFAULT_BRIGHTNESS
        self._listeners: list[Any] = []

    def add_listener(self, listener: Any) -> None:
        """Add a listener for state changes."""
        self._listeners.append(listener)

    def remove_listener(self, listener: Any) -> None:
        """Remove a listener."""
        if listener in self._listeners:
            self._listeners.remove(listener)

    def notify_listeners(self) -> None:
        """Notify all listeners of state change."""
        for listener in self._listeners:
            listener()


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Dummy Integration component from yaml configuration."""
    hass.data.setdefault(DOMAIN, DummyIntegrationData())

    # Load platforms
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.helpers.discovery.async_load_platform(
                platform, DOMAIN, {}, config
            )
        )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Dummy Integration from a config entry."""
    hass.data.setdefault(DOMAIN, DummyIntegrationData())

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data.pop(DOMAIN, None)

    return unload_ok
