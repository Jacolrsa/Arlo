"""#help command."""

from __future__ import annotations

from .. import messages
from ..context import Context


async def execute(ctx: Context) -> None:
    """Handle the #help command."""

    text = (
        "📟 Arlo\n\n"
        "Available commands:\n"
        "#help\n"
        "#leaderboard"
    )

    messages.reply(ctx, text)