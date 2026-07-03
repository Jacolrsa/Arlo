from .commands import help
from .commands import meshcoremonday

DIRECT_COMMANDS = {
    help.COMMAND: help,
    meshcoremonday.COMMAND: meshcoremonday,
}


async def handle_message(ctx):
    """Route incoming messages."""

    if ctx.sender == "Arlo":
        return

    command = DIRECT_COMMANDS.get(ctx.message.strip().lower())

    if command:
        await command.execute(ctx)