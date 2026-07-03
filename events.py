"""Arlo event handling."""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any

from homeassistant.core import Event, HomeAssistant

_LOGGER = logging.getLogger(__name__)


class EventBus:
    """Internal event bus for Arlo."""

    def __init__(self) -> None:
        self._message_handlers: list[
            Callable[[Event], Awaitable[None]]
        ] = []

        self._message_sent_handlers: list[
            Callable[[dict[str, Any]], Awaitable[None]]
        ] = []

    def register_message_handler(
        self,
        handler: Callable[[Event], Awaitable[None]],
    ) -> None:
        """Register incoming message handler."""
        self._message_handlers.append(handler)

    def register_message_sent_handler(
        self,
        handler: Callable[[dict[str, Any]], Awaitable[None]],
    ) -> None:
        """Register outgoing message handler."""
        self._message_sent_handlers.append(handler)

    async def _dispatch_message(self, event: Event) -> None:
        """Dispatch incoming MeshCore message."""
        for handler in self._message_handlers:
            try:
                await handler(event)
            except Exception:
                _LOGGER.exception("Incoming message handler failed")

    async def _dispatch_message_sent(self, event: Event) -> None:
        """Dispatch outgoing MeshCore message."""
        for handler in self._message_sent_handlers:
            try:
                await handler(event.data)
            except Exception:
                _LOGGER.exception("Outgoing message handler failed")

    def register_with_homeassistant(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Register Home Assistant event listeners."""

        async def message_listener(event: Event) -> None:
            await self._dispatch_message(event)

        async def message_sent_listener(event: Event) -> None:
            await self._dispatch_message_sent(event)

        hass.bus.async_listen(
            "meshcore_message",
            message_listener,
        )

        hass.bus.async_listen(
            "meshcore_message_sent",
            message_sent_listener,
        )

        _LOGGER.info("Arlo event bus registered")


events = EventBus()