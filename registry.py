"""Arlo command registry."""

from __future__ import annotations

from .commands import help
from .commands import meshcoremonday

#
# Direct message commands
#

_DIRECT_COMMANDS = {
    help.COMMAND: help,
    meshcoremonday.COMMAND: meshcoremonday,
}

#
# Channel commands
#

_CHANNEL_COMMANDS = {
    meshcoremonday.COMMAND: meshcoremonday,
}


def get_direct_command(command: str):
    """Return a direct-message command module."""

    return _DIRECT_COMMANDS.get(command.lower())


def get_channel_command(command: str):
    """Return a channel command module."""

    return _CHANNEL_COMMANDS.get(command.lower())
