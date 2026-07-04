"""Arlo persistent storage."""

from __future__ import annotations

import copy
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)

STORAGE_VERSION = 1
STORAGE_KEY = "arlo"

DEFAULT_DATA = {
    "users": {},
    "meshcore_monday": {
        "checkins": {},
    },
}


class ArloStorage:
    """Persistent storage for Arlo."""

    def __init__(self, hass: HomeAssistant) -> None:
        self._store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self._data = copy.deepcopy(DEFAULT_DATA)

    async def load(self) -> None:
        """Load database."""

        data = await self._store.async_load()

        if data is None:
            _LOGGER.info("Creating new Arlo database")
            self._data = copy.deepcopy(DEFAULT_DATA)
            await self.save()
        else:
            self._data = data
            self._ensure_schema()

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
        today = dt_util.now().date().isoformat()

        if pubkey not in users:
            users[pubkey] = {
                "name": name,
                "joined": today,
                "last_seen": today,
                "total_checkins": 0,
                "current_streak": 0,
                "best_streak": 0,
            }

            _LOGGER.info("Registered new user %s", name)

        else:
            users[pubkey]["name"] = name
            users[pubkey]["last_seen"] = today

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

    def has_meshcore_monday_checkin(
        self,
        *,
        pubkey: str,
        monday_id: str,
    ) -> bool:
        """Return true if a stored MeshCore Monday check-in exists."""

        return pubkey in self._meshcore_monday_checkins().get(monday_id, {})

    def get_meshcore_monday_position(
        self,
        *,
        pubkey: str,
        monday_id: str,
    ) -> int | None:
        """Return a player's MeshCore Monday position."""

        monday_checkins = self._meshcore_monday_checkins().get(monday_id, {})

        for position, checked_in_pubkey in enumerate(monday_checkins, start=1):
            if checked_in_pubkey == pubkey:
                return position

        return None

    async def record_meshcore_monday_checkin(
        self,
        *,
        pubkey: str,
        name: str,
        monday_id: str,
    ) -> None:
        """Persist a MeshCore Monday check-in."""

        await self.register_user(pubkey=pubkey, name=name)

        users = self._data["users"]
        user = users[pubkey]
        now = dt_util.now().isoformat()
        checkins = self._meshcore_monday_checkins()
        monday_checkins = checkins.setdefault(monday_id, {})

        monday_checkins[pubkey] = {
            "pubkey": pubkey,
            "name": name,
            "checked_in_at": now,
        }

        user["total_checkins"] = user.get("total_checkins", 0) + 1
        user["last_checkin"] = monday_id

        await self.save()

    def _meshcore_monday_checkins(self) -> dict:
        """Return MeshCore Monday check-in storage."""

        meshcore_monday = self._data.setdefault("meshcore_monday", {})
        return meshcore_monday.setdefault("checkins", {})

    def _ensure_schema(self) -> None:
        """Ensure loaded data has the expected persistence shape."""

        self._data.setdefault("users", {})
        self._data.setdefault("meshcore_monday", {})
        self._data["meshcore_monday"].setdefault("checkins", {})


storage: ArloStorage | None = None


def get_storage() -> ArloStorage | None:
    """Return the active Arlo storage instance."""

    return storage


async def async_setup_storage(
    hass: HomeAssistant,
) -> ArloStorage:
    """Initialize storage."""

    global storage

    storage = ArloStorage(hass)

    await storage.load()

    return storage
