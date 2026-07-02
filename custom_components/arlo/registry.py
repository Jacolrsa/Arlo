"""Arlo command registry."""

from __future__ import annotations

from .commands import help


DIRECT_COMMANDS = {
    "#help": help,
}


CHANNEL_COMMANDS = {
}