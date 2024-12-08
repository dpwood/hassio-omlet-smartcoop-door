import logging

from smartcoop.api.models import Device

from homeassistant.components.light import ColorMode, LightEntity
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
    """Set up the light platform."""

    coordinator: OmletDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [OmletLight(device_id, coordinator) for device_id in coordinator.data]
    )


class OmletLight(OmletCoopEntity, LightEntity):
    """Representation of a coop light."""

    _attr_supported_color_modes = {ColorMode.ONOFF}

    def __init__(
        self,
        device_id: str,
        coordinator: OmletDataUpdateCoordinator,
    ) -> None:
        """Initialize a light."""
        super().__init__(device_id, coordinator)

        self._attr_color_mode = ColorMode.ONOFF

        self._attr_name = f"Omlet Smart Coop {device_id} Light"
        self._attr_unique_id = f"{self._device_id}-light"

    async def async_turn_on(self):
        """Turn on the light."""
        if await self.coordinator.control_device(self._device_id, "on"):
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.error("Failed to turn on light for device %s", self._device_id)

    async def async_turn_off(self):
        """Turn off the light."""
        if await self.coordinator.control_device(self._device_id, "off"):
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.error("Failed to turn off light for device %s", self._device_id)

    @callback
    def _update_attr(self, device: Device) -> None:
        self._attr_is_on = device.state.light.state in ("on", "onpending")
        _LOGGER.debug(
            "Updated light state for device %s: %s",
            self._device_id,
            device.state.light.state,
        )
