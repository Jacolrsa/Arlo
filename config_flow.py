"""Config flow for Arlo."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DEFAULT_DISABLE_MONDAY_CHECK
from .const import DEFAULT_MESHCORE_MONDAY_CHANNEL
from .const import DOMAIN
from .const import OPTION_DISABLE_MONDAY_CHECK
from .const import OPTION_MESHCORE_MONDAY_CHANNEL


class ArloConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""

        return ArloOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        return self.async_create_entry(
            title="Arlo",
            data={},
        )


class ArloOptionsFlow(config_entries.OptionsFlow):
    """Handle Arlo options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""

        self.config_entry = config_entry

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ):
        """Manage Arlo options."""

        if user_input is not None:
            return self.async_create_entry(
                title="",
                data=user_input,
            )

        options = self.config_entry.options

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        OPTION_DISABLE_MONDAY_CHECK,
                        default=options.get(
                            OPTION_DISABLE_MONDAY_CHECK,
                            DEFAULT_DISABLE_MONDAY_CHECK,
                        ),
                    ): bool,
                    vol.Optional(
                        OPTION_MESHCORE_MONDAY_CHANNEL,
                        default=options.get(
                            OPTION_MESHCORE_MONDAY_CHANNEL,
                            DEFAULT_MESHCORE_MONDAY_CHANNEL,
                        ),
                    ): int,
                }
            ),
        )
