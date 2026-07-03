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

    _LOGGER.warning("========================================")
    _LOGGER.warning("ARLO ROUTER")
    _LOGGER.warning("Sender  : %s", ctx.sender)
    _LOGGER.warning("Message : %s", message)
    _LOGGER.warning("Type    : %s", ctx.message_type)

    if not message:
        _LOGGER.warning("Ignoring empty message")
        return

    #
    # Ignore Arlo's own replies
    #
    if ctx.sender == "Arlo":
        _LOGGER.warning("Ignoring Arlo's own message")
        return

    #
    # Direct messages
    #
    if ctx.is_direct:

        _LOGGER.warning("Looking up direct command")

        command = get_direct_command(message)

        if command is None:
            _LOGGER.warning("Unknown command")

            await messages.error(
                ctx,
                f"Unknown command:\n{message}\n\nType #help",
            )
            return

        _LOGGER.warning("Executing command %s", message)

        await command.execute(ctx)

        _LOGGER.warning("Command finished")

        return

    #
    # Channel messages
    #
    if ctx.is_channel:

        _LOGGER.warning("Looking up channel command")

        command = get_channel_command(message)

        if command is None:
            _LOGGER.warning("No channel command found")
            return

        _LOGGER.warning("Executing channel command %s", message)

        await command.execute(ctx)