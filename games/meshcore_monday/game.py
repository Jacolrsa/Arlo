"""MeshCore Monday game rules."""

from __future__ import annotations

import logging
from datetime import date

from homeassistant.util import dt as dt_util

from ...context import Context
from ...storage import ArloStorage

MESHCORE_MONDAY_CHANNEL = 1

_LOGGER = logging.getLogger(__name__)


async def handle_command(
    ctx: Context,
    storage: ArloStorage,
) -> None:
    """Handle a MeshCore Monday command."""

    today = _today()
    channel_check_passed = ctx.is_channel

    _LOGGER.info(
        "MeshCore Monday diagnostic: channel_idx=%s channel_check_passed=%s",
        ctx.channel_idx,
        channel_check_passed,
    )

    monday_check_passed = _is_monday(today)

    _LOGGER.info(
        "MeshCore Monday diagnostic: local_date=%s weekday=%s monday_check_passed=%s",
        today.isoformat(),
        today.weekday(),
        monday_check_passed,
    )

    if not channel_check_passed:
        return

    if not monday_check_passed:
        return

    monday_id = today.isoformat()
    duplicate_checkin = storage.has_meshcore_monday_checkin(
        pubkey=ctx.pubkey,
        monday_id=monday_id,
    )

    _LOGGER.info(
        "MeshCore Monday diagnostic: duplicate_checkin_detected=%s",
        duplicate_checkin,
    )

    if duplicate_checkin:
        return

    await storage.record_meshcore_monday_checkin(
        pubkey=ctx.pubkey,
        name=ctx.sender,
        monday_id=monday_id,
    )

    _LOGGER.info("MeshCore Monday diagnostic: checkin_recorded=True")


def _today() -> date:
    """Return the current Home Assistant local date."""

    return dt_util.now().date()


def _is_monday(day: date) -> bool:
    """Return true if the date is Monday."""

    return day.weekday() == 0
