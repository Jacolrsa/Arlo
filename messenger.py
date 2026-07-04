"""Arlo message transport."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

TX_DELAY = 2.0
MAX_RETRIES = 3
RETRY_DELAY = 5.0


@dataclass(slots=True)
class QueuedMessage:
    """Outgoing message."""

    pubkey: str
    recipient: str
    message: str
    retries: int = 0
    created: datetime = field(default_factory=datetime.now)


class Messenger:
    """Handles all outgoing MeshCore traffic."""

    def __init__(self) -> None:
        self._queue: asyncio.Queue[QueuedMessage] = asyncio.Queue()
        self._worker: asyncio.Task | None = None
        self._hass: HomeAssistant | None = None

    async def start(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """Start the background sender."""

        self._hass = hass

        if self._worker is None:
            self._worker = entry.async_create_background_task(
                hass,
                self._run(),
                "Arlo messenger worker",
            )
            _LOGGER.info("Messenger worker started")

    async def stop(self) -> None:
        """Stop the background sender."""

        if self._worker is not None:
            self._worker.cancel()

            try:
                await self._worker
            except asyncio.CancelledError:
                pass

            self._worker = None
            self._hass = None

            _LOGGER.info("Messenger worker stopped")

    async def send_direct(
        self,
        *,
        pubkey: str,
        recipient: str,
        message: str,
    ) -> None:
        """Queue a direct message."""

        if self._hass is None or self._worker is None:
            raise RuntimeError("Messenger has not been started")

        item = QueuedMessage(
            pubkey=pubkey,
            recipient=recipient,
            message=message,
        )

        await self._queue.put(item)

        _LOGGER.info(
            "Queued message for %s (%d waiting)",
            recipient,
            self._queue.qsize(),
        )

    async def _run(self) -> None:
        """Background queue worker."""

        if self._hass is None:
            raise RuntimeError("Messenger has not been started")

        try:
            while True:

                item = await self._queue.get()

                try:

                    _LOGGER.info(
                        "Sending to %s (attempt %d)",
                        item.recipient,
                        item.retries + 1,
                    )

                    await asyncio.sleep(TX_DELAY)

                    await self._hass.services.async_call(
                        "meshcore",
                        "send_message",
                        {
                            "pubkey_prefix": item.pubkey,
                            "message": item.message,
                        },
                        blocking=True,
                    )

                    _LOGGER.info("Message sent successfully")

                except Exception:

                    item.retries += 1

                    if item.retries <= MAX_RETRIES:

                        _LOGGER.warning(
                            "Send failed, retry %d/%d",
                            item.retries,
                            MAX_RETRIES,
                        )

                        await asyncio.sleep(RETRY_DELAY)
                        await self._queue.put(item)

                    else:

                        _LOGGER.exception(
                            "Message permanently failed after %d attempts",
                            MAX_RETRIES,
                        )

                finally:

                    self._queue.task_done()

        except asyncio.CancelledError:
            _LOGGER.info("Messenger worker cancelled")
            raise


messenger = Messenger()
