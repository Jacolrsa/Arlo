"""MeshCore Monday game rules."""

from __future__ import annotations

import logging
from datetime import date

from homeassistant.util import dt as dt_util

from ...const import DEFAULT_DISABLE_MONDAY_CHECK
from ...const import DEFAULT_MESHCORE_MONDAY_CHANNEL
from ...const import DOMAIN
from ...const import OPTION_DISABLE_MONDAY_CHECK
from ...const import OPTION_MESHCORE_MONDAY_CHANNEL
from ...context import Context
from ... import messages
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
        await messages.reply(
            ctx,
            "MeshCore Monday check-ins must be performed from a MeshCore channel.",
        )
        return

    if not monday_check_passed:
        await messages.reply(
            ctx,
            "MeshCore Monday check-ins are only available on Mondays.",
        )
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
        await messages.reply(
            ctx,
            "You have already checked in this week.",
        )
        return

    await storage.record_meshcore_monday_checkin(
        pubkey=ctx.pubkey,
        name=ctx.sender,
        monday_id=monday_id,
    )

    _LOGGER.warning("MeshCore Monday diagnostic: checkin_recorded=True")

    position = storage.get_meshcore_monday_position(
        pubkey=ctx.pubkey,
        monday_id=monday_id,
    )
    user = storage.get_user(ctx.pubkey) or {}
    total_checkins = user.get("total_checkins", 0)
    channel_idx = _meshcore_monday_channel(ctx)

    await messages.channel(
        channel_idx,
        f"{ctx.sender} checked in.\n\n"
        f"You are currently #{position} this week.",
    )

    await messages.reply(
        ctx,
        "MeshCore Monday check-in succeeded.\n\n"
        f"You are currently #{position} this week.\n"
        f"Total check-ins: {total_checkins}\n"
        "Current streak: TODO",
    )


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


def _meshcore_monday_channel(ctx: Context) -> int:
    """Return the configured MeshCore Monday channel."""

    entries = ctx.hass.config_entries.async_entries(DOMAIN)

    if not entries:
        return DEFAULT_MESHCORE_MONDAY_CHANNEL

    return entries[0].options.get(
        OPTION_MESHCORE_MONDAY_CHANNEL,
        DEFAULT_MESHCORE_MONDAY_CHANNEL,
    )
