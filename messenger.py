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

    _LOGGER.info("========================================")
    _LOGGER.info("ARLO MESSENGER")
    _LOGGER.info("To      : %s", name)
    _LOGGER.info("Pubkey  : %s", pubkey)
    _LOGGER.info("Message : %s", message)

    #
    # We will replace this later with the real MeshCore service call.
    #