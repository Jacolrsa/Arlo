"""Arlo message router."""

from __future__ import annotations

from .registry import get_direct_command


async def handle_message(ctx):
    """Route incoming messages."""

    if ctx.sender == "Arlo":
        return

    command = get_direct_command(ctx.message.strip())

    if command:
        await command.execute(ctx)
