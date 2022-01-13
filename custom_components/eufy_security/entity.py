import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NAME, Device
from .coordinator import EufySecurityDataUpdateCoordinator

_LOGGER: logging.Logger = logging.getLogger(__package__)


class EufySecurityEntity(CoordinatorEntity):
    def __init__(
        self,
        coordinator: EufySecurityDataUpdateCoordinator,
        entry: ConfigEntry,
        device: Device,
    ):
        super().__init__(coordinator)
        self.entry: ConfigEntry = entry
        self.device: Device = device

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.device.serial_number)},
            "name": self.device.name,
            "model": self.device.model,
            "hardware": self.device.hardware_version,
            "software": self.device.software_version,
            "manufacturer": NAME,
        }

    @property
    def available(self) -> bool:
        return not not self.coordinator.data

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def state_attributes(self):
        return {
            "type": self.device.type,
            "category": self.device.category,
            "state": self.device.state,
            "properties": self.device.properties,
            "properties_metadata": self.device.properties_metadata,
        }
