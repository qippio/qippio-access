"""Config flow for Qippio Access."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from . import DOMAIN


class QippioAccessConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle a Qippio Access config flow."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Handle the initial setup."""

        if user_input is not None:
            return self.async_create_entry(
                title="Qippio Access",
                data=user_input,
            )

        users = await self.hass.auth.async_get_users()

        user_options = {
            user.id: (
                user.name
                or getattr(user, "username", None)
                or user.id
            )
            for user in users
            if not user.system_generated
        }

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "installer_user_id"
                    ): vol.In(user_options),

                    vol.Required(
                        "client_user_id"
                    ): vol.In(user_options),
                }
            ),
        )
