"""MeshCore Monday game rules."""

from __future__ import annotations

from datetime import date

from homeassistant.util import dt as dt_util

from ...context import Context
from ...storage import ArloStorage

MESHCORE_MONDAY_CHANNEL = 1


async def handle_command(
    ctx: Context,
    storage: ArloStorage,
) -> None:
    """Handle a MeshCore Monday command."""

    today = _today()

    if ctx.channel_idx != MESHCORE_MONDAY_CHANNEL:
        return

    if not _is_monday(today):
        return

    monday_id = today.isoformat()

    if storage.has_meshcore_monday_checkin(
        pubkey=ctx.pubkey,
        monday_id=monday_id,
    ):
        return

    await storage.record_meshcore_monday_checkin(
        pubkey=ctx.pubkey,
        name=ctx.sender,
        monday_id=monday_id,
    )


def _today() -> date:
    """Return the current Home Assistant local date."""

    return dt_util.now().date()


def _is_monday(day: date) -> bool:
    """Return true if the date is Monday."""

    return day.weekday() == 0
