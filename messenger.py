"""Low-level MeshCore messaging."""

from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


async def send_direct(
    hass: HomeAssistant,
    *,
    pubkey: str,
    name: str,
    message: str,
) -> None:
    """Send a direct MeshCore message."""

    _LOGGER.warning("========================================")
    _LOGGER.warning("ARLO MESSENGER")
    _LOGGER.warning("To      : %s", name)
    _LOGGER.warning("Pubkey  : %s", pubkey)
    _LOGGER.warning("Message : %s", message)

    await hass.services.async_call(
        "meshcore",
        "send_message",
        {
            "pubkey_prefix": pubkey,
            "message": message,
        },
        blocking=True,
    )

    _LOGGER.warning("Message sent")