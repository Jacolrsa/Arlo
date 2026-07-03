from .commands import help
from .commands import leaderboard
from .commands import meshcoremonday

DIRECT_COMMANDS = {
    help.COMMAND: help,
    leaderboard.COMMAND: leaderboard,
    meshcoremonday.COMMAND: meshcoremonday,
}


async def handle_message(ctx):
    """Route incoming messages."""

    if ctx.sender == "Arlo":
        return

    if ctx.message_type == "direct":
        command = DIRECT_COMMANDS.get(ctx.message.strip().lower())

        if command:
            await command.execute(ctx)
        return

    if ctx.message_type == "channel":
        command = DIRECT_COMMANDS.get(ctx.message.strip().lower())

        if command:
            await command.execute(ctx)
        return