"""Arlo - MeshCore Assistant."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, VERSION

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up Arlo from configuration.yaml."""

    _LOGGER.info("========================================")
    _LOGGER.info("Starting Arlo %s", VERSION)
    _LOGGER.info("========================================")

    hass.data.setdefault(DOMAIN, {})

    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Arlo from a config entry."""

    _LOGGER.info("Setting up config entry: %s", entry.title)

    hass.data.setdefault(DOMAIN, {})

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload Arlo."""

    _LOGGER.info("Stopping Arlo")

    hass.data.pop(DOMAIN, None)

    return True