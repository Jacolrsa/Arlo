"""Arlo message router."""

from __future__ import annotations

import logging

from .registry import get_channel_command
from .registry import get_direct_command

_LOGGER = logging.getLogger(__name__)


async def handle_message(ctx):
    """Route incoming messages."""

    if ctx.sender == "Arlo":
        return

    message = ctx.message.strip()
    direct_command = get_direct_command(message)
    channel_command = get_channel_command(message)

    _LOGGER.info(
        "Router diagnostic: incoming_message=%r message_type=%r "
        "is_direct=%s is_channel=%s command=%r",
        ctx.message,
        ctx.message_type,
        ctx.is_direct,
        ctx.is_channel,
        message,
    )

    _LOGGER.info(
        "Router diagnostic: direct_command_matched=%s "
        "channel_command_matched=%s",
        direct_command is not None,
        channel_command is not None,
    )

    if ctx.is_channel:
        command = channel_command
    else:
        command = direct_command

    _LOGGER.info(
        "Router diagnostic: selected_handler=%s",
        getattr(command, "__name__", None),
    )

    if command:
        await command.execute(ctx)
    else:
        _LOGGER.info(
            "Router diagnostic: no handler found for command=%r "
            "message_type=%r direct_match=%s channel_match=%s",
            message,
            ctx.message_type,
            direct_command is not None,
            channel_command is not None,
        )
