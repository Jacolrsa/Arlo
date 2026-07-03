"""Arlo message context."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.core import Event, HomeAssistant


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

    @classmethod
    def from_event(
        cls,
        hass: HomeAssistant,
        event: Event,
    ) -> "Context":
        """Create a Context from a MeshCore event."""

        data = event.data

        return cls(
            hass=hass,
            sender=data.get("sender_name", ""),
            pubkey=data.get("pubkey_prefix", ""),
            message=data.get("message", ""),
            message_type=data.get("message_type", ""),
            channel=data.get("channel_name", ""),
            channel_idx=data.get("channel_index", 0),
            event=data,
        )

    @property
    def is_direct(self) -> bool:
        """True if this is a direct message."""
        return self.message_type == "direct"

    @property
    def is_channel(self) -> bool:
        """True if this is a channel message."""
        return self.message_type == "channel"