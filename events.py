"""Arlo event handling."""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import Any

from homeassistant.core import Event, HomeAssistant

_LOGGER = logging.getLogger(__name__)


class EventBus:
    """Simple internal event bus for Arlo."""

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
        """Register incoming MeshCore message handler."""

        self._message_handlers.append(handler)

    def register_message_sent_handler(
        self,
        handler: Callable[[dict[str, Any]], Awaitable[None]],
    ) -> None:
        """Register outgoing MeshCore message handler."""

        self._message_sent_handlers.append(handler)

    async def dispatch_message(
        self,
        event: Event,
    ) -> None:
        """Dispatch an incoming message."""

        for handler in self._message_handlers:
            try:
                await handler(event)
            except Exception:
                _LOGGER.exception("Message handler failed")

    async def dispatch_message_sent(
        self,
        data: dict[str, Any],
    ) -> None:
        """Dispatch an outgoing message event."""

        for handler in self._message_sent_handlers:
            try:
                await handler(data)
            except Exception:
                _LOGGER.exception("Message sent handler failed")

    def register_with_homeassistant(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Register Home Assistant listeners."""

        async def _message(event: Event) -> None:
            await self.dispatch_message(event)

        async def _message_sent(event: Event) -> None:
            await self.dispatch_message_sent(event.data)

        hass.bus.async_listen(
            "meshcore_message",
            lambda event: asyncio.create_task(_message(event)),
        )

        hass.bus.async_listen(
            "meshcore_message_sent",
            lambda event: asyncio.create_task(_message_sent(event)),
        )

        _LOGGER.info("Arlo event bus registered")


events = EventBus()