"""Coordinator for the omlet integration."""

from __future__ import annotations

from datetime import timedelta
import logging

from smartcoop.api.models import Device

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, REFRESH_INTERVAL

_LOGGER = logging.getLogger(__name__)


class OmletDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Device]]):
    """Class to manage fetching Omlet data."""

    def __init__(self, entry: ConfigEntry, hass: HomeAssistant) -> None:
        """Initialize the coordinator."""
        self.api_key = entry.data[CONF_API_KEY]
        self.host = entry.data[CONF_HOST]
        self.session = async_get_clientsession(hass)

        super().__init__(
            hass,
            _LOGGER,
            name="omlet_data",
            update_method=self._async_update_data,
            update_interval=timedelta(seconds=entry.data.get(REFRESH_INTERVAL, 120)),
        )

    async def _async_update_data(self) -> dict[str, Device]:
        devices_json = await self.fetch_devices()
        return {
            d["deviceId"]: Device.from_json(d)
            for d in devices_json
            if d["deviceType"] == "Autodoor"
        }

    async def fetch_devices(self):
        """Retrieve device status from the Omlet API."""
        url = f"{self.host}/api/v1/device"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with self.session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return None

    async def fetch_device_info(self, device_id):
        """Retrieve device status from the Omlet API."""
        url = f"{self.host}/api/v1/device/{device_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with self.session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return None

    async def control_device(self, device_id, action):
        """Invoke an action on a device."""
        url = f"{self.host}/api/v1/device/{device_id}/action/{action}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with self.session.post(url, headers=headers) as response:
            return response.status == 204

    async def update_single_entity(self, device_id):
        """Fetch and update data for a single entity."""
        # Fetch the updated data for the entity
        new_data = await self.fetch_device_info(device_id)
        self.data[device_id] = Device.from_json(new_data)
        # Notify listeners
        self.async_update_listeners()

    async def async_added_to_hass(self):
        """Register dispatcher listener when entity is added."""
        async_dispatcher_connect(
            self.hass, f"{DOMAIN}_webhook_event", self.handle_webhook_event
        )
