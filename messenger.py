"""Arlo message transport."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime

from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

TX_DELAY = 2.0


@dataclass(slots=True)
class QueuedMessage:
    """Outgoing message."""

    pubkey: str
    recipient: str
    message: str
    created: datetime = datetime.now()


class Messenger:
    """Handles all outgoing MeshCore traffic."""

    def __init__(self) -> None:
        self._queue: asyncio.Queue[QueuedMessage] = asyncio.Queue()
        self._worker: asyncio.Task | None = None
        self._hass: HomeAssistant | None = None

    async def start(self, hass: HomeAssistant) -> None:
        """Start background worker."""

        self._hass = hass

        if self._worker is None:
            self._worker = asyncio.create_task(self._run())

            _LOGGER.info("Messenger worker started")

    async def stop(self) -> None:
        """Stop background worker."""

        if self._worker:
            self._worker.cancel()

            self._worker = None

    async def send_direct(
        self,
        *,
        pubkey: str,
        recipient: str,
        message: str,
    ) -> None:
        """Queue a direct message."""

        await self._queue.put(
            QueuedMessage(
                pubkey=pubkey,
                recipient=recipient,
                message=message,
            )
        )

        _LOGGER.info(
            "Queued message (%d waiting)",
            self._queue.qsize(),
        )

    async def _run(self) -> None:
        """Background sender."""

        while True:

            item = await self._queue.get()

            try:

                _LOGGER.info(
                    "Sending to %s",
                    item.recipient,
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

                _LOGGER.info("Sent successfully")

            except Exception:
                _LOGGER.exception("Transmit failed")

            finally:
                self._queue.task_done()


messenger = Messenger()