"""Arlo command registry."""

from __future__ import annotations

from .commands import help

#
# Direct message commands
#

_DIRECT_COMMANDS = {
    "#help": help,
}

#
# Channel commands
#

_CHANNEL_COMMANDS = {
}


def get_direct_command(command: str):
    """Return a direct-message command module."""

    return _DIRECT_COMMANDS.get(command.lower())


def get_channel_command(command: str):
    """Return a channel command module."""

    return _CHANNEL_COMMANDS.get(command.lower())