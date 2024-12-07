import logging

from smartcoop.api.models import Device

from homeassistant.components.cover import CoverDeviceClass, CoverEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import OmletDataUpdateCoordinator
from .entity import OmletCoopEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the cover platform."""

    coordinator: OmletDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [OmletDoorCover(device_id, coordinator) for device_id in coordinator.data]
    )


class OmletDoorCover(OmletCoopEntity, CoverEntity):
    """Representation of a door as a cover entity."""

    _attr_device_class = CoverDeviceClass.DOOR

    def __init__(
        self,
        device_id: str,
        coordinator: OmletDataUpdateCoordinator,
    ) -> None:
        """Initialize a door."""
        super().__init__(device_id, coordinator)

        self._attr_name = f"Omlet Smart Coop {device_id} Door"
        self._attr_unique_id = self._device_id

    async def async_open_cover(self, **kwargs):
        """Open the door."""
        try:
            if await self.coordinator.control_device(self._device_id, "open"):
                _LOGGER.debug("Opened door for device %s", self._device_id)
                await self.coordinator.async_request_refresh()
            else:
                _LOGGER.error("Failed to open door for device %s", self._device_id)
        except Exception as e:
            _LOGGER.error("Error opening door for device %s: %s", self._device_id, e)

    async def async_close_cover(self, **kwargs):
        """Close the door."""
        try:
            if await self.coordinator.control_device(self._device_id, "close"):
                _LOGGER.debug("Closed door for device %s", self._device_id)
                await self.coordinator.async_request_refresh()
            else:
                _LOGGER.error("Failed to close door for device %s", self._device_id)
        except Exception as e:
            _LOGGER.error("Error closing door for device %s: %s", self._device_id, e)

    async def async_stop_cover(self, **kwargs):
        """Stop the door."""
        try:
            if await self.coordinator.control_device(self._device_id, "stop"):
                _LOGGER.debug("Stopped door for device %s", self._device_id)
                await self.coordinator.async_request_refresh()
            else:
                _LOGGER.error("Failed to stop door for device %s", self._device_id)
        except Exception as e:
            _LOGGER.error("Error stopping door for device %s: %s", self._device_id, e)

    @callback
    def _update_attr(self, device: Device) -> None:
        state = device.state.door.state
        if state == "stopping":
            return
        self._attr_is_closed = state == "closed"
        self._attr_is_closing = state == "closepending"
        self._attr_is_opening = state == "openpending"
        _LOGGER.debug(
            "Updated door state for device %s: %s",
            self._device_id,
            "closed" if self.is_closed else "open",
        )
