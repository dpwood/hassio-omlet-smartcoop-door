"""Platform for sensor integration."""

import logging

from smartcoop.api.models import Device

from homeassistant.components.cover import CoverEntity
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import OmletDataUpdateCoordinator
from .entity import OmletCoopEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the sensor platform."""

    coordinator: OmletDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            sensor
            for device_id in coordinator.data
            for sensor in (
                OmletBatterySensor(device_id, coordinator),
                OmletDoorSensor(device_id, coordinator),
            )
        ]
    )


class OmletBatterySensor(OmletCoopEntity, SensorEntity):
    """Representation of a Battery Sensor."""

    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_native_unit_of_measurement = "%"

    def __init__(
        self,
        device_id: str,
        coordinator: OmletDataUpdateCoordinator,
    ) -> None:
        """Initialize a battery sensor."""
        super().__init__(device_id, coordinator)

        self._attr_name = f"Omlet Smart Coop {device_id} Battery"
        self._attr_unique_id = "{self._device_id}-battery"

    @callback
    def _update_attr(self, device: Device) -> None:
        self._attr_native_value = device.state.general.batteryLevel
        _LOGGER.debug(
            "Updated door battery level for device %s: %s%%",
            self._device_id,
            self._attr_native_value,
        )


class OmletDoorSensor(OmletCoopEntity, SensorEntity):
    """Representation of a Door Sensor."""

    @callback
    def _update_attr(self, device: Device) -> None:
        self._attr_native_value = device.state.door.state

    def __init__(
        self,
        device_id: str,
        coordinator: OmletDataUpdateCoordinator,
    ) -> None:
        """Initialize a door sensor."""
        super().__init__(device_id, coordinator)

        self._attr_name = f"Omlet Smart Coop {device_id} Door State"
        self._attr_unique_id = "{self._device_id}-doorstate"
