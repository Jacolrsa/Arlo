"""Home Assistant services for Arlo."""

from __future__ import annotations

from collections import Counter
from datetime import date
from typing import Any

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.util import dt as dt_util

from .const import DOMAIN
from .storage import get_storage

SERVICE_MESHCORE_MONDAY_STATS = "meshcore_monday_stats"


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up Arlo services."""

    async def meshcore_monday_stats(call: ServiceCall) -> None:
        """Create a MeshCore Monday statistics notification."""

        storage = get_storage()

        if storage is None:
            message = "Arlo storage is not ready."
        else:
            message = _build_meshcore_monday_stats(
                storage.get_meshcore_monday_stats_data(),
                dt_util.now().date(),
            )

        await hass.services.async_call(
            "persistent_notification",
            "create",
            {
                "title": "MeshCore Monday Statistics",
                "message": message,
                "notification_id": "arlo_meshcore_monday_stats",
            },
            blocking=True,
        )

    hass.services.async_register(
        DOMAIN,
        SERVICE_MESHCORE_MONDAY_STATS,
        meshcore_monday_stats,
    )


async def async_unload_services(hass: HomeAssistant) -> None:
    """Unload Arlo services."""

    if hass.services.has_service(DOMAIN, SERVICE_MESHCORE_MONDAY_STATS):
        hass.services.async_remove(DOMAIN, SERVICE_MESHCORE_MONDAY_STATS)


def _build_meshcore_monday_stats(data: dict[str, Any], today: date) -> str:
    """Build copyable MeshCore Monday statistics."""

    users = data["users"]
    checkins = data["checkins"]
    iso_year, iso_week, _ = today.isocalendar()
    this_month = (today.year, today.month)

    week_checkins = _checkins_for_week(checkins, iso_year, iso_week)
    month_checkins = _checkins_for_month(checkins, this_month)
    lifetime_checkins = _flatten_checkins(checkins)

    return "\n".join(
        [
            "MeshCore Monday Statistics",
            "",
            "This week",
            f"ISO year/week: {iso_year}-W{iso_week:02d}",
            f"Total check-ins: {len(week_checkins)}",
            "All check-ins:",
            *_format_ranked_checkins(week_checkins),
            "All streaks:",
            *_format_user_field(users, "current_streak", "week"),
            "",
            "This month",
            f"Total check-ins: {len(month_checkins)}",
            f"Unique players: {len({item['pubkey'] for item in month_checkins})}",
            "All players by check-ins:",
            *_format_counter(_count_by_player(month_checkins), users),
            "",
            "Lifetime",
            f"Total check-ins: {len(lifetime_checkins)}",
            f"Total players: {len({item['pubkey'] for item in lifetime_checkins})}",
            "All total check-ins:",
            *_format_user_field(users, "total_checkins", "check-in"),
            "All longest streaks:",
            *_format_user_field(users, "best_streak", "week"),
        ]
    )


def _checkins_for_week(
    checkins: dict[str, dict[str, dict[str, Any]]],
    iso_year: int,
    iso_week: int,
) -> list[dict[str, Any]]:
    """Return check-ins for an ISO week."""

    items = []

    for monday_id, monday_checkins in checkins.items():
        try:
            day = date.fromisoformat(monday_id)
        except ValueError:
            continue

        checkin_year, checkin_week, _ = day.isocalendar()

        if checkin_year == iso_year and checkin_week == iso_week:
            items.extend(monday_checkins.values())

    return items


def _checkins_for_month(
    checkins: dict[str, dict[str, dict[str, Any]]],
    year_month: tuple[int, int],
) -> list[dict[str, Any]]:
    """Return check-ins for a calendar month."""

    items = []

    for monday_id, monday_checkins in checkins.items():
        try:
            day = date.fromisoformat(monday_id)
        except ValueError:
            continue

        if (day.year, day.month) == year_month:
            items.extend(monday_checkins.values())

    return items


def _flatten_checkins(
    checkins: dict[str, dict[str, dict[str, Any]]],
) -> list[dict[str, Any]]:
    """Return all check-ins."""

    items = []

    for monday_checkins in checkins.values():
        items.extend(monday_checkins.values())

    return items


def _format_ranked_checkins(checkins: list[dict[str, Any]]) -> list[str]:
    """Format ranked check-ins."""

    if not checkins:
        return ["None"]

    return [
        f"{index}. {item.get('name', 'Unknown')}"
        for index, item in enumerate(checkins, start=1)
    ]


def _format_user_field(
    users: dict[str, dict[str, Any]],
    field: str,
    label: str,
) -> list[str]:
    """Format top users by a numeric field."""

    ranked = sorted(
        users.values(),
        key=lambda user: user.get(field, 0),
        reverse=True,
    )
    ranked = [user for user in ranked if user.get(field, 0) > 0]

    if not ranked:
        return ["None"]

    return [
        f"{index}. {user.get('name', 'Unknown')} - "
        f"{user.get(field, 0)} {_plural(label, user.get(field, 0))}"
        for index, user in enumerate(ranked, start=1)
    ]


def _count_by_player(checkins: list[dict[str, Any]]) -> Counter[str]:
    """Count check-ins by player."""

    return Counter(item["pubkey"] for item in checkins if item.get("pubkey"))


def _format_counter(
    counter: Counter[str],
    users: dict[str, dict[str, Any]],
) -> list[str]:
    """Format a player counter."""

    if not counter:
        return ["None"]

    lines = []

    for index, (pubkey, count) in enumerate(counter.most_common(), start=1):
        user = users.get(pubkey, {})
        name = user.get("name", pubkey)
        lines.append(f"{index}. {name} - {count} {_plural('check-in', count)}")

    return lines


def _plural(label: str, count: int) -> str:
    """Return a singular or plural label."""

    if count == 1:
        return label

    return f"{label}s"
