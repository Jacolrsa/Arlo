"""#help command."""

from __future__ import annotations

from .. import messages
from ..context import Context

COMMAND = "#help"


async def execute(ctx: Context) -> None:
    """Handle the #help command."""

    text = (
        "📟 Arlo\n\n"
        "Available commands:\n"
        "#help\n"
        "#meshcoremonday"
    )

    await messages.reply(ctx, text)