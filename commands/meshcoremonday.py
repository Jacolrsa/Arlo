"""MeshCore Monday command."""

from __future__ import annotations

from .. import messages
from ..context import Context
from ..storage import storage

COMMAND = "#meshcoremonday"


async def execute(ctx: Context) -> None:
    """Handle the #meshcoremonday command."""

    if storage is None:
        await messages.reply(ctx, "❌ Storage is not ready.")
        return

    await storage.register_user(
        pubkey=ctx.pubkey,
        name=ctx.sender,
    )

    user = storage.get_user(ctx.pubkey)

    await messages.reply(
        ctx,
        "✅ Welcome to MeshCore Monday!\n\n"
        f"Callsign: {user['name']}\n"
        f"Joined: {user['joined']}\n"
        f"Total check-ins: {user['total_checkins']}"
    )