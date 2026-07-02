"""Arlo command router."""

from __future__ import annotations

import logging

from . import messages
from .context import Context
from .registry import (
    get_channel_command,
    get_direct_command,
)

_LOGGER = logging.getLogger(__name__)


async def handle_message(ctx: Context) -> None:
    """Route an incoming MeshCore message."""

    message = ctx.message.strip()

    _LOGGER.info("========================================")
    _LOGGER.info("ARLO ROUTER")
    _LOGGER.info("Sender      : %s", ctx.sender)
    _LOGGER.info("Message     : %s", message)
    _LOGGER.info("Type        : %s", ctx.message_type)

    if not message:
        return

    #
    # Ignore Arlo's own replies
    #

    if ctx.sender == "Arlo":
        return

    #
    # Direct messages
    #

    if ctx.is_direct:

        command = get_direct_command(message)

        if command is None:
            await messages.error(
                ctx,
                f"Unknown command:\n{message}\n\nType #help",
            )
            return

        _LOGGER.info("Executing %s", message)

        await command.execute(ctx)

        return

    #
    # Channel messages
    #

    if ctx.is_channel:

        command = get_channel_command(message)

        if command is None:
            return

        _LOGGER.info("Executing %s", message)

        await command.execute(ctx)