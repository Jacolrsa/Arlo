"""MeshCore Monday game rules."""

from __future__ import annotations

import logging
from datetime import date

from homeassistant.util import dt as dt_util

from ...const import DEFAULT_DISABLE_MONDAY_CHECK
from ...const import DOMAIN
from ...const import OPTION_DISABLE_MONDAY_CHECK
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

    _LOGGER.warning(
        "MeshCore Monday diagnostic: channel_idx=%s channel_check_passed=%s",
        ctx.channel_idx,
        channel_check_passed,
    )

    disable_monday_check = _disable_monday_check(ctx)
    monday_check_passed = disable_monday_check or _is_monday(today)

    _LOGGER.warning(
        "MeshCore Monday diagnostic: local_date=%s weekday=%s "
        "disable_monday_check=%s monday_check_passed=%s",
        today.isoformat(),
        today.weekday(),
        disable_monday_check,
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

    _LOGGER.warning(
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

    _LOGGER.warning("MeshCore Monday diagnostic: checkin_recorded=True")


def _today() -> date:
    """Return the current Home Assistant local date."""

    return dt_util.now().date()


def _is_monday(day: date) -> bool:
    """Return true if the date is Monday."""

    return day.weekday() == 0


def _disable_monday_check(ctx: Context) -> bool:
    """Return true if the development Monday override is enabled."""

    entries = ctx.hass.config_entries.async_entries(DOMAIN)

    if not entries:
        return DEFAULT_DISABLE_MONDAY_CHECK

    return entries[0].options.get(
        OPTION_DISABLE_MONDAY_CHECK,
        DEFAULT_DISABLE_MONDAY_CHECK,
    )
