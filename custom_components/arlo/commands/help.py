"""#help command."""

from __future__ import annotations

from .. import messages


async def execute(ctx):
    """Handle the #help command."""

    text = (
        "📟 Arlo\n\n"
        "Available commands:\n"
        "#help\n"
        "#leaderboard"
    )

    messages.reply(ctx, text)