"""Arlo persistent storage."""

from __future__ import annotations

import logging
from datetime import date

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

_LOGGER = logging.getLogger(__name__)

STORAGE_VERSION = 1
STORAGE_KEY = "arlo"

DEFAULT_DATA = {
    "users": {}
}


class ArloStorage:
    """Persistent storage for Arlo."""

    def __init__(self, hass: HomeAssistant) -> None:
        self._store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self._data = DEFAULT_DATA.copy()

    async def load(self) -> None:
        """Load database."""

        data = await self._store.async_load()

        if data is None:
            _LOGGER.info("Creating new Arlo database")
            self._data = DEFAULT_DATA.copy()
            await self.save()
        else:
            self._data = data

    async def save(self) -> None:
        """Save database."""

        await self._store.async_save(self._data)

    async def register_user(
        self,
        pubkey: str,
        name: str,
    ) -> None:
        """Register or update a user."""

        users = self._data["users"]

        if pubkey not in users:

            users[pubkey] = {
                "name": name,
                "joined": date.today().isoformat(),
                "last_seen": date.today().isoformat(),
                "total_checkins": 0,
                "current_streak": 0,
                "best_streak": 0,
            }

            _LOGGER.info("Registered new user %s", name)

        else:

            users[pubkey]["name"] = name
            users[pubkey]["last_seen"] = date.today().isoformat()

        await self.save()

    def get_user(
        self,
        pubkey: str,
    ) -> dict | None:
        """Return a user."""

        return self._data["users"].get(pubkey)

    def get_users(self) -> dict:
        """Return all users."""

        return self._data["users"]


storage: ArloStorage | None = None


async def async_setup_storage(
    hass: HomeAssistant,
) -> ArloStorage:
    """Initialize storage."""

    global storage

    storage = ArloStorage(hass)

    await storage.load()

    return storage