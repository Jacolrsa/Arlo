"""Arlo MeshCore listener."""

from __future__ import annotations

import logging

from homeassistant.core import Event, HomeAssistant

from .context import Context
from .router import handle_message

_LOGGER = logging.getLogger(__name__)


def async_register(hass: HomeAssistant) -> None:
    """Register MeshCore event listener."""

    async def _handle(event: Event) -> None:
        """Handle a MeshCore message event."""

        _LOGGER.info("========================================")
        _LOGGER.info("ARLO LISTENER")
        _LOGGER.info("Received MeshCore event")

        ctx = Context.from_event(hass, event)

        _LOGGER.info("Sender : %s", ctx.sender)
        _LOGGER.info("Message: %s", ctx.message)
        _LOGGER.info("Type   : %s", ctx.message_type)

        await handle_message(ctx)

    hass.bus.async_listen(
        "meshcore_message",
        _handle,
    )