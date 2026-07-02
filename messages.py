"""High-level messaging functions."""

from __future__ import annotations

from .messenger import send_direct


def reply(ctx, text: str):
    """Reply to whoever sent the message."""

    send_direct(
        ctx.hass,
        pubkey=ctx.pubkey,
        name=ctx.sender,
        message=text,
    )


def success(ctx, text: str):
    """Send a success message."""

    reply(ctx, f"✅ {text}")


def error(ctx, text: str):
    """Send an error message."""

    reply(ctx, f"❌ {text}")


def info(ctx, text: str):
    """Send an information message."""

    reply(ctx, f"ℹ️ {text}")