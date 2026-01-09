"""Switch platform for Dummy Integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant, callback
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
    """Set up the Dummy switch platform."""
    data = hass.data.get(DOMAIN)
    if data is None:
        _LOGGER.error("Dummy integration data not found")
        return

    switch = DummyLightSwitch(data)
    async_add_entities([switch], True)


class DummyLightSwitch(SwitchEntity):
    """Representation of a Dummy Switch that controls the Dummy Light."""

    _attr_has_entity_name = True
    _attr_name = "Dummy Light Switch"
    _attr_unique_id = "dummy_integration_light_switch"

    def __init__(self, data) -> None:
        """Initialize the switch."""
        self._data = data
        self._attr_is_on = data.light_is_on

    async def async_added_to_hass(self) -> None:
        """Register callbacks when entity is added."""
        self._data.add_listener(self._handle_state_change)

    async def async_will_remove_from_hass(self) -> None:
        """Clean up when entity is removed."""
        self._data.remove_listener(self._handle_state_change)

    @callback
    def _handle_state_change(self) -> None:
        """Handle state change from shared data.

        This keeps the switch in sync with the light state,
        so if the light is turned on/off directly, the switch reflects that.
        """
        self._attr_is_on = self._data.light_is_on
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch (and thus the light) on."""
        self._data.light_is_on = True
        self._attr_is_on = True

        self._data.notify_listeners()
        _LOGGER.debug("Dummy switch turned on - light is now on")

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch (and thus the light) off."""
        self._data.light_is_on = False
        self._attr_is_on = False

        self._data.notify_listeners()
        _LOGGER.debug("Dummy switch turned off - light is now off")

    async def async_update(self) -> None:
        """Fetch new state data for the switch."""
        self._attr_is_on = self._data.light_is_on
