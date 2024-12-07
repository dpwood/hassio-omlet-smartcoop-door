"""Entity for Surepetcare."""

from __future__ import annotations

from abc import abstractmethod

from smartcoop.api.models import Device

from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import OmletDataUpdateCoordinator


class OmletCoopEntity(CoordinatorEntity[OmletDataUpdateCoordinator]):
    """An implementation for Omlet entities."""

    def __init__(
        self,
        device_id: str,
        coordinator: OmletDataUpdateCoordinator,
    ) -> None:
        """Initialize an Omlet entity."""
        super().__init__(coordinator)

        self._device_id = device_id
        # self._device_name = device_id

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=f"Omlet Smart Coop {device_id}",
            manufacturer="Omlet",
            model="Smart Coop",
        )
        self._update_attr(coordinator.data[device_id])

    @abstractmethod
    @callback
    def _update_attr(self, device: Device) -> None:
        """Update the state and attributes."""

    @callback
    def _handle_coordinator_update(self) -> None:
        """Get the latest data and update the state."""
        self._update_attr(self.coordinator.data[self._device_id])
        self.async_write_ha_state()
