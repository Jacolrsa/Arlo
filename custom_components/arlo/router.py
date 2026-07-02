"""Arlo command router."""

from __future__ import annotations

import logging

from .context import Context
from .registry import DIRECT_COMMANDS, CHANNEL_COMMANDS
from . import messages

_LOGGER = logging.getLogger(__name__)


async def handle_message(ctx: Context) -> None:
    """Route an incoming message."""

    message = ctx.message.strip()

    _LOGGER.info("========================================")
    _LOGGER.info("ARLO ROUTER")
    _LOGGER.info("Sender      : %s", ctx.sender)
    _LOGGER.info("Message     : %s", message)
    _LOGGER.info("Type        : %s", ctx.message_type)

    # Ignore empty messages
    if not message:
        return

    # Ignore our own replies
    if ctx.sender == "Arlo":
        _LOGGER.debug("Ignoring Arlo message")
        return

    # -----------------------------
    # Direct Messages
    # -----------------------------
    if ctx.is_direct:

        command = DIRECT_COMMANDS.get(message.lower())

        if command is None:
            await messages.error(
                ctx,
                f"Unknown command: {message}\n\nTry #help",
            )
            return

        _LOGGER.info("Executing %s", message)

        await command.execute(ctx)

        return

    # -----------------------------
    # Channel Messages
    # -----------------------------
    if ctx.is_channel:

        command = CHANNEL_COMMANDS.get(message.lower())

        if command is None:
            return

        _LOGGER.info("Executing %s", message)

        await command.execute(ctx)