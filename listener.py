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

        _LOGGER.warning("========================================")
        _LOGGER.warning("ARLO LISTENER")
        _LOGGER.warning("Received MeshCore event")

        ctx = Context.from_event(hass, event)

        _LOGGER.warning("Sender : %s", ctx.sender)
        _LOGGER.warning("Message: %s", ctx.message)
        _LOGGER.warning("Type   : %s", ctx.message_type)

        await handle_message(ctx)

    hass.bus.async_listen(
        "meshcore_message",
        _handle,
    )