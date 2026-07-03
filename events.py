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

        self._unsub_listeners: list[Callable[[], None]] = []

    def register_message_handler(
        self,
        handler: Callable[[Event], Awaitable[None]],
    ) -> Callable[[], None]:
        """Register incoming message handler."""
        self._message_handlers.append(handler)

        def unregister() -> None:
            if handler in self._message_handlers:
                self._message_handlers.remove(handler)

        return unregister

    def register_message_sent_handler(
        self,
        handler: Callable[[dict[str, Any]], Awaitable[None]],
    ) -> Callable[[], None]:
        """Register outgoing message handler."""
        self._message_sent_handlers.append(handler)

        def unregister() -> None:
            if handler in self._message_sent_handlers:
                self._message_sent_handlers.remove(handler)

        return unregister

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

        if self._unsub_listeners:
            self.unregister_from_homeassistant()

        async def message_listener(event: Event) -> None:
            await self._dispatch_message(event)

        async def message_sent_listener(event: Event) -> None:
            await self._dispatch_message_sent(event)

        self._unsub_listeners.append(
            hass.bus.async_listen(
                "meshcore_message",
                message_listener,
            )
        )

        self._unsub_listeners.append(
            hass.bus.async_listen(
                "meshcore_message_sent",
                message_sent_listener,
            )
        )

        _LOGGER.info("Arlo event bus registered")

    def unregister_from_homeassistant(self) -> None:
        """Unregister Home Assistant event listeners."""

        while self._unsub_listeners:
            unsubscribe = self._unsub_listeners.pop()
            unsubscribe()

        _LOGGER.info("Arlo event bus unregistered")


events = EventBus()
