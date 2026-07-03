"""High-level messaging API."""

from __future__ import annotations

from .messenger import messenger


async def reply(ctx, text: str) -> None:
    """Reply to the sender."""

    await messenger.send_direct(
        pubkey=ctx.pubkey,
        recipient=ctx.sender,
        message=text,
    )


async def success(ctx, text: str) -> None:
    """Send success message."""

    await reply(ctx, f"✅ {text}")


async def error(ctx, text: str) -> None:
    """Send error message."""

    await reply(ctx, f"❌ {text}")


async def info(ctx, text: str) -> None:
    """Send information message."""

    await reply(ctx, f"ℹ️ {text}")