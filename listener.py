"""Arlo MeshCore listener."""

from __future__ import annotations

import logging
from collections.abc import Callable

from homeassistant.core import Event, HomeAssistant

from .context import Context
from .events import events
from .router import handle_message

_LOGGER = logging.getLogger(__name__)


async def _incoming_message(
    hass: HomeAssistant,
    event: Event,
) -> None:
    """Handle incoming MeshCore messages."""

    _LOGGER.warning("========================================")
    _LOGGER.warning("ARLO LISTENER")
    _LOGGER.warning("Received MeshCore event")

    ctx = Context.from_event(hass, event)

    _LOGGER.warning("Sender : %s", ctx.sender)
    _LOGGER.warning("Pubkey : %s", ctx.pubkey)
    _LOGGER.warning("Message: %s", ctx.message)
    _LOGGER.warning("Type   : %s", ctx.message_type)

    await handle_message(ctx)


async def _message_sent(data: dict) -> None:
    """Handle outgoing MeshCore message status."""

    _LOGGER.warning("========================================")
    _LOGGER.warning("ARLO TRANSPORT")

    _LOGGER.warning("Receiver : %s", data.get("receiver"))
    _LOGGER.warning("ACK      : %s", data.get("ack_received"))
    _LOGGER.warning("Send ID  : %s", data.get("send_id"))


def async_register(hass: HomeAssistant) -> Callable[[], None]:
    """Register Arlo listeners."""

    async def incoming_message(event: Event) -> None:
        await _incoming_message(hass, event)

    unregister_message = events.register_message_handler(incoming_message)
    unregister_message_sent = events.register_message_sent_handler(_message_sent)

    events.register_with_homeassistant(hass)

    def unregister() -> None:
        unregister_message()
        unregister_message_sent()
        events.unregister_from_homeassistant()
        _LOGGER.info("Arlo listeners unregistered")

    _LOGGER.info("Arlo listeners registered")

    return unregister
