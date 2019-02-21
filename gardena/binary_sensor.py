"""
Gardena smart sensor which registeres a couple of sensors.

@ todo something with documentation

"""
import logging
from datetime import timedelta

from homeassistant.components.binary_sensor import BinarySensorDevice
from custom_components.gardena import (GARDENA_SENSORS, GARDENA_WATERING_COMPUTERS, GARDENA_LOGIN)

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['gardena']

SCAN_INTERVAL = timedelta(minutes=5)

NO_FROST = 'no_frost'

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Demo sensors."""
    dev = []
    for sensor in hass.data[GARDENA_SENSORS]:
        dev.append(GardenaSmartFrostWarningSensor(hass, sensor))
    for watering_computer in hass.data[GARDENA_WATERING_COMPUTERS]:
        dev.append(GardenaSmartFrostWarningSensor(hass, watering_computer))

    _LOGGER.debug("Adding gardena sensors as binarysensors %s", dev)
    add_entities(dev, True)

class GardenaSmartBinarySensor(BinarySensorDevice):
    """Representation of a Demo sensor."""

    def __init__(self, hass, sensor):
        """Initialize the sensor."""
        self._sensor = sensor
        self.gardena = hass.data[GARDENA_LOGIN]

    def update(self):
        """Update the states of Gardena devices."""
        _LOGGER.debug("Running Gardena update")
        self.gardena.update_devices()  # is a throttled update

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return self._device_class

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._sensor.get_generic_info()


class GardenaSmartFrostWarningSensor(GardenaSmartBinarySensor):
    def __init__(self, hass, sensor):
        """Initialize the sensor."""
        super().__init__(hass, sensor)
        self._name = sensor.name + ' ambient frost warning'
        self._device_class = 'cold'

    @property
    def is_on(self):
        return self._sensor.get_ambient_frost_warning() != NO_FROST