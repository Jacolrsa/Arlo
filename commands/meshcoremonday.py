"""MeshCore Monday command."""

from __future__ import annotations

from ..context import Context
from ..games.meshcore_monday import handle_command
from ..storage import get_storage

COMMAND = "#meshcoremonday"


async def execute(ctx: Context) -> None:
    """Handle the #meshcoremonday command."""

    storage_service = get_storage()

    if storage_service is None:
        return

    await handle_command(ctx, storage_service)
