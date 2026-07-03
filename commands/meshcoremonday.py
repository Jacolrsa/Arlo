"""MeshCore Monday command."""

from .. import storage, messages


COMMAND = "#meshcoremonday"


async def execute(ctx):
    """Handle #meshcoremonday."""

    pubkey = ctx.pubkey
    name = ctx.sender

    users = await storage.get_users(ctx.hass)

    user = users.get(pubkey)

    if user is None:
        user = {
            "name": name,
            "points": 1,
            "checkins": 1,
            "streak": 1,
        }

        users[pubkey] = user

        await storage.save_users(ctx.hass, users)

        await messages.reply(
            ctx,
            f"✅ Welcome to MeshCore Monday!\n\n"
            f"You are participant #{len(users)}."
        )
        return

    user["name"] = name
    user["points"] += 1
    user["checkins"] += 1

    await storage.save_users(ctx.hass, users)

    await messages.reply(
        ctx,
        f"✅ Check-in recorded.\n\n"
        f"Points: {user['points']}"
    )