"""Config flow for Qippio Access."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from . import (
    CONF_CLIENT_USER_ID,
    CONF_INSTALLER_USER_ID,
    DOMAIN,
)


class QippioAccessConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle the Qippio Access config flow."""

    VERSION = 1

    async def _get_user_options(self) -> dict[str, str]:
        """Return selectable Home Assistant users."""

        users = await self.hass.auth.async_get_users()

        return {
            user.id: (
                user.name
                or getattr(user, "username", None)
                or user.id
            )
            for user in users
            if not user.system_generated
        }

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Handle initial setup."""

        # Only one Qippio Access instance is allowed.
        if self._async_current_entries():
            return self.async_abort(
                reason="single_instance_allowed"
            )

        if user_input is not None:
            return self.async_create_entry(
                title="Qippio Access",
                data=user_input,
            )

        user_options = await self._get_user_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_INSTALLER_USER_ID
                    ): vol.In(user_options),

                    vol.Required(
                        CONF_CLIENT_USER_ID
                    ): vol.In(user_options),
                }
            ),
        )

    async def async_step_reconfigure(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Reconfigure Qippio Access."""

        entry = self._get_reconfigure_entry()

        if user_input is not None:
            return self.async_update_reload_and_abort(
                entry,
                data_updates=user_input,
            )

        user_options = await self._get_user_options()

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_INSTALLER_USER_ID,
                        default=entry.data[
                            CONF_INSTALLER_USER_ID
                        ],
                    ): vol.In(user_options),

                    vol.Required(
                        CONF_CLIENT_USER_ID,
                        default=entry.data[
                            CONF_CLIENT_USER_ID
                        ],
                    ): vol.In(user_options),
                }
            ),
        )
