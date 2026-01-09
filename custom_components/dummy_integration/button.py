"""Button platform for Dummy Integration."""
from __future__ import annotations

import logging

from homeassistant.components.button import ButtonEntity, ButtonDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Dummy Integration button platform."""
    async_add_entities([DummyRestartButton(hass)], True)


class DummyRestartButton(ButtonEntity):
    """Button to restart Home Assistant."""

    _attr_has_entity_name = True
    _attr_name = "Restart Home Assistant"
    _attr_unique_id = f"{DOMAIN}_restart_button"
    _attr_device_class = ButtonDeviceClass.RESTART
    _attr_icon = "mdi:restart"

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the restart button."""
        self._hass = hass

    async def async_press(self) -> None:
        """Handle the button press - restart Home Assistant."""
        _LOGGER.info("Restart button pressed - restarting Home Assistant")
        await self._hass.services.async_call("homeassistant", "restart")
