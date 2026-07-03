"""Arlo integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, VERSION
from .listener import async_register
from .messenger import messenger

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = []


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Arlo integration."""

    _LOGGER.info("Starting Arlo %s", VERSION)

    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Arlo from a config entry."""

    _LOGGER.info("Setting up Arlo")

    #
    # Start messenger worker
    #
    await messenger.start(hass)

    #
    # Register MeshCore listener
    #
    async_register(hass)

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    _LOGGER.info("Arlo is ready")

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload Arlo."""

    await messenger.stop()

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:
        _LOGGER.info("Arlo unloaded")

    return unload_ok