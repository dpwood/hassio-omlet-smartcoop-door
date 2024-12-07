"""Intégration de la Omlet Smart Coop Door avec Home Assistant."""

import asyncio
import logging

import aiohttp
import voluptuous as vol

from homeassistant.components.webhook import async_register
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_DEVICE_ID, CONF_HOST, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.entity import Entity

from .const import DOMAIN
from .coordinator import OmletDataUpdateCoordinator

PLATFORMS = [Platform.COVER, Platform.SENSOR, Platform.LIGHT]

_LOGGER = logging.getLogger(__name__)

WEBHOOK_EVENT = f"{DOMAIN}_webhook_event"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Omlet Smart Coop from a config entry."""

    # Store the API instance for later use by platforms
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator = OmletDataUpdateCoordinator(
        entry,
        hass,
    )
    webhook_id = f"{DOMAIN}_{entry.entry_id}"
    # Register the webhook handler
    #   async_register(
    #       hass,
    #       DOMAIN,
    #       "Omlet Webhook",
    #       webhook_id,
    #       async_handle_webhook,
    #   )
    # TODO This webhook needs to be unloaded too otherwise reloading the integration fails

    # Store webhook info for potential future use
    # hass.data.setdefault(DOMAIN, {})
    # hass.data[DOMAIN][entry.entry_id] = {"webhook_id": webhook_id}

    # TODO initial refresh

    await coordinator.async_config_entry_first_refresh()

    # Forward entry to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_handle_webhook(hass, webhook_id, request):
    """Handle incoming webhook requests."""
    try:
        data = await request.json()
        _LOGGER.debug("Received webhook data: %s", data)
        # Dispatch the event to entities
        async_dispatcher_send(hass, WEBHOOK_EVENT, data)
    except Exception as e:
        _LOGGER.error("Error handling webhook: %s", e)
