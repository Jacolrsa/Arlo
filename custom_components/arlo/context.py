"""Arlo message context."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.core import HomeAssistant


@dataclass(slots=True)
class Context:
    """Information about a MeshCore message."""

    hass: HomeAssistant

    sender: str
    pubkey: str

    message: str

    message_type: str

    channel: str
    channel_idx: int

    event: dict

    @property
    def is_direct(self) -> bool:
        """True if this is a direct message."""
        return self.message_type == "direct"

    @property
    def is_channel(self) -> bool:
        """True if this is a channel message."""
        return self.message_type == "channel"