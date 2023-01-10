"""The SkyRC integration."""
from __future__ import annotations

from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ADDRESS, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SkyRC from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    address: str = entry.data[CONF_ADDRESS]

    ble_device = bluetooth.async_ble_device_from_address(hass, address.upper())
    if not ble_device:
        raise ConfigEntryNotReady(f"Could not find SkyRC device with address {address}")

    # coordinator = hass.data[DOMAIN][entry.entry_id] = SwitchbotDataUpdateCoordinator(
    #     hass,
    #     _LOGGER,
    #     ble_device,
    #     device,
    #     entry.unique_id,
    #     entry.data.get(CONF_NAME, entry.title),
    #     connectable,
    #     switchbot_model,
    # )
    # entry.async_on_unload(coordinator.async_start())
    # if not await coordinator.async_wait_ready():
    #     raise ConfigEntryNotReady(f"{address} is not advertising state")

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
        if not hass.config_entries.async_entries(DOMAIN):
            hass.data.pop(DOMAIN)

    return unload_ok
