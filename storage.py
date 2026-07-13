"""Arlo persistent storage."""

from __future__ import annotations

import copy
import logging
from datetime import date, timedelta

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
            if self._repair_meshcore_monday_statistics():
                await self.save()

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

    def get_meshcore_monday_stats_data(self) -> dict:
        """Return MeshCore Monday data for statistics."""

        return {
            "users": copy.deepcopy(self._data["users"]),
            "checkins": copy.deepcopy(self._meshcore_monday_checkins()),
        }

    async def record_meshcore_monday_checkin(
        self,
        *,
        pubkey: str,
        name: str,
        monday_id: str,
    ) -> None:
        """Persist a MeshCore Monday check-in."""

        now = dt_util.now().isoformat()
        checkins = self._meshcore_monday_checkins()

        if not self._meshcore_monday_checkins_available():
            _LOGGER.warning("Cannot record MeshCore Monday check-in storage")
            return

        monday_checkins = checkins.setdefault(monday_id, {})

        if not isinstance(monday_checkins, dict):
            _LOGGER.warning(
                "Cannot record MeshCore Monday check-in for malformed "
                "monday_id=%s",
                monday_id,
            )
            return

        if pubkey in monday_checkins:
            return

        await self.register_user(pubkey=pubkey, name=name)

        users = self._data["users"]
        user = users[pubkey]

        monday_checkins[pubkey] = {
            "pubkey": pubkey,
            "name": name,
            "checked_in_at": now,
        }

        current_streak, best_streak = self._calculate_player_streaks(pubkey)
        trusted_existing_total = self._stored_stat(user.get("total_checkins"))
        trusted_existing_best_streak = self._stored_stat(
            user.get("best_streak"),
        )

        user["total_checkins"] = trusted_existing_total + 1
        user["current_streak"] = current_streak
        user["best_streak"] = max(trusted_existing_best_streak, best_streak)
        user["last_checkin"] = monday_id

        await self.save()

    async def reset_meshcore_monday_data(self) -> None:
        """Clear MeshCore Monday test data."""

        self._data["meshcore_monday"] = {
            "checkins": {},
        }

        for user in self._data["users"].values():
            user["total_checkins"] = 0
            user["current_streak"] = 0
            user["best_streak"] = 0
            user.pop("last_checkin", None)

        await self.save()

    def _meshcore_monday_checkins(self) -> dict:
        """Return MeshCore Monday check-in storage."""

        meshcore_monday = self._data.setdefault("meshcore_monday", {})

        if not isinstance(meshcore_monday, dict):
            return {}

        checkins = meshcore_monday.setdefault("checkins", {})

        if not isinstance(checkins, dict):
            return {}

        return checkins

    def _ensure_schema(self) -> None:
        """Ensure loaded data has the expected persistence shape."""

        if not isinstance(self._data, dict):
            self._data = copy.deepcopy(DEFAULT_DATA)
            return

        self._data.setdefault("users", {})
        self._data.setdefault("meshcore_monday", {})

        if not isinstance(self._data["users"], dict):
            self._data["users"] = {}

        if not isinstance(self._data["meshcore_monday"], dict):
            self._data["meshcore_monday"] = {}

        self._data["meshcore_monday"].setdefault("checkins", {})

    def _repair_meshcore_monday_statistics(self) -> bool:
        """Repair derived MeshCore Monday user statistics."""

        changed = False
        users = self._data["users"]
        histories, names = self._meshcore_monday_histories()

        for pubkey in sorted(set(users) | set(histories), key=str):
            user = users.get(pubkey)

            if not isinstance(user, dict):
                user = {}
                users[pubkey] = user
                changed = True

            dates = sorted(histories.get(pubkey, set()))
            existing_total = self._stored_stat(user.get("total_checkins"))
            existing_current_streak = self._stored_stat(
                user.get("current_streak"),
            )
            existing_best_streak = self._stored_stat(user.get("best_streak"))

            repaired_total = max(existing_total, len(dates))
            current_streak, best_streak = self._calculate_streaks_from_dates(
                dates,
            )
            repaired_best_streak = max(existing_best_streak, best_streak)

            if "name" not in user:
                user["name"] = names.get(pubkey, pubkey)
                changed = True

            if user.get("total_checkins") != repaired_total:
                user["total_checkins"] = repaired_total
                changed = True

            if dates:
                if user.get("current_streak") != current_streak:
                    user["current_streak"] = current_streak
                    changed = True

                if user.get("best_streak") != repaired_best_streak:
                    user["best_streak"] = repaired_best_streak
                    changed = True

                last_checkin = dates[-1].isoformat()

                if user.get("last_checkin") != last_checkin:
                    user["last_checkin"] = last_checkin
                    changed = True
            else:
                if "current_streak" not in user:
                    user["current_streak"] = existing_current_streak
                    changed = True

                if "best_streak" not in user:
                    user["best_streak"] = existing_best_streak
                    changed = True

        return changed

    def _calculate_player_streaks(self, pubkey: str) -> tuple[int, int]:
        """Return current and best streaks from valid historical Mondays."""

        histories, _ = self._meshcore_monday_histories()
        dates = sorted(histories.get(pubkey, set()))

        return self._calculate_streaks_from_dates(dates)

    def _meshcore_monday_histories(
        self,
    ) -> tuple[dict[str, set[date]], dict[str, str]]:
        """Return valid Monday check-in dates by player."""

        histories: dict[str, set[date]] = {}
        names: dict[str, str] = {}

        for monday_id, monday_checkins in self._meshcore_monday_checkins().items():
            day = self._valid_monday_date(monday_id)

            if day is None or not isinstance(monday_checkins, dict):
                continue

            for pubkey, checkin in monday_checkins.items():
                if not isinstance(pubkey, str) or not pubkey:
                    continue

                histories.setdefault(pubkey, set()).add(day)

                if isinstance(checkin, dict):
                    name = checkin.get("name")

                    if isinstance(name, str) and name:
                        names[pubkey] = name

        return histories, names

    def _meshcore_monday_checkins_available(self) -> bool:
        """Return true if the check-in container can be updated."""

        meshcore_monday = self._data.get("meshcore_monday")

        if not isinstance(meshcore_monday, dict):
            return False

        return isinstance(meshcore_monday.get("checkins"), dict)

    @staticmethod
    def _stored_stat(value: object) -> int:
        """Return a trusted stored statistic value."""

        if isinstance(value, bool) or not isinstance(value, int):
            return 0

        if value < 0:
            return 0

        return value

    @staticmethod
    def _valid_monday_date(monday_id: str) -> date | None:
        """Return a valid Monday date from a stored check-in key."""

        if not isinstance(monday_id, str):
            return None

        try:
            day = date.fromisoformat(monday_id)
        except ValueError:
            return None

        if day.weekday() != 0:
            return None

        return day

    @staticmethod
    def _calculate_streaks_from_dates(
        dates: list[date],
    ) -> tuple[int, int]:
        """Return current and best streaks for sorted Monday dates."""

        current_streak = 0
        best_streak = 0
        previous_day: date | None = None

        for day in dates:
            if previous_day is not None and day - previous_day == timedelta(days=7):
                current_streak += 1
            else:
                current_streak = 1

            best_streak = max(best_streak, current_streak)
            previous_day = day

        return current_streak, best_streak


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
