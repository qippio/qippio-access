"""Qippio Access integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

DOMAIN = "qippio_access"

CONF_INSTALLER_USER_ID = "installer_user_id"
CONF_CLIENT_USER_ID = "client_user_id"

PLATFORMS = [Platform.SWITCH]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Qippio Access."""

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload Qippio Access."""

    return await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )
