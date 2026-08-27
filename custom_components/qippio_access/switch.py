"""Switch platform for Qippio Access."""

from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import (
    AddConfigEntryEntitiesCallback,
)

from . import (
    CONF_CLIENT_USER_ID,
    CONF_INSTALLER_USER_ID,
    DOMAIN,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Qippio Access switch."""

    async_add_entities(
        [
            QippioAccessSwitch(
                hass,
                entry,
            )
        ],
        update_before_add=True,
    )


class QippioAccessSwitch(SwitchEntity):
    """Control Qippio remote access."""

    _attr_has_entity_name = True
    _attr_name = "Accès distant"
    _attr_icon = "mdi:account-key"

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the switch."""

        self.hass = hass
        self._entry = entry

        self._installer_user_id = entry.data[
            CONF_INSTALLER_USER_ID
        ]

        self._client_user_id = entry.data[
            CONF_CLIENT_USER_ID
        ]

        self._attr_unique_id = (
            f"{entry.entry_id}_remote_access"
        )

    async def _async_check_authorized_user(self) -> None:
        """Check that the caller is the configured client."""

        if self._context.user_id != self._client_user_id:
            raise HomeAssistantError(
                "Utilisateur non autorisé à modifier "
                "l'accès Qippio."
            )

    async def async_turn_on(
        self,
        **kwargs: Any,
    ) -> None:
        """Allow Qippio remote access."""

        await self._async_check_authorized_user()

        user = await self.hass.auth.async_get_user(
            self._installer_user_id
        )

        if user is None:
            raise HomeAssistantError(
                "Le compte Qippio configuré "
                "est introuvable."
            )

        await self.hass.auth.async_update_user(
            user,
            local_only=False,
        )

        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(
        self,
        **kwargs: Any,
    ) -> None:
        """Block Qippio remote access."""

        await self._async_check_authorized_user()

        user = await self.hass.auth.async_get_user(
            self._installer_user_id
        )

        if user is None:
            raise HomeAssistantError(
                "Le compte Qippio configuré "
                "est introuvable."
            )

        await self.hass.auth.async_update_user(
            user,
            local_only=True,
        )

        self._attr_is_on = False
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update the switch from the real HA user state."""

        user = await self.hass.auth.async_get_user(
            self._installer_user_id
        )

        if user is None:
            self._attr_available = False
            return

        self._attr_available = True

        # Switch ON = accès distant autorisé.
        # local_only False = accès distant autorisé.
        self._attr_is_on = not user.local_only
