"""Arlo MeshCore listener."""

from __future__ import annotations

import logging

from homeassistant.core import Event, HomeAssistant

_LOGGER = logging.getLogger(__name__)


def async_register(hass: HomeAssistant) -> None:
    """Register MeshCore event listener."""

    async def _handle(event: Event) -> None:

        _LOGGER.info("========================================")
        _LOGGER.info("ARLO LISTENER")
        _LOGGER.info("Received MeshCore event")
        _LOGGER.info("%s", event.data)

    hass.bus.async_listen(
        "meshcore_message",
        _handle,
    )