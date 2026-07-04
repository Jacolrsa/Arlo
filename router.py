"""Arlo message router."""

from __future__ import annotations

from .registry import get_channel_command
from .registry import get_direct_command


async def handle_message(ctx):
    """Route incoming messages."""

    if ctx.sender == "Arlo":
        return

    message = ctx.message.strip()

    if ctx.is_channel:
        command = get_channel_command(message)
    else:
        command = get_direct_command(message)

    if command:
        await command.execute(ctx)
