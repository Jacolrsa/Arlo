"""High-level messaging functions."""

from __future__ import annotations

from .messenger import send_direct


async def reply(ctx, text: str) -> None:
    """Reply to whoever sent the message."""

    await send_direct(
        ctx.hass,
        pubkey=ctx.pubkey,
        name=ctx.sender,
        message=text,
    )


async def success(ctx, text: str) -> None:
    """Send a success message."""

    await reply(ctx, f"✅ {text}")


async def error(ctx, text: str) -> None:
    """Send an error message."""

    await reply(ctx, f"❌ {text}")


async def info(ctx, text: str) -> None:
    """Send an information message."""

    await reply(ctx, f"ℹ️ {text}")