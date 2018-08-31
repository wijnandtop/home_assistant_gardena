"""
Gardena smart sensor which registers a couple of sensors.

@ todo something with documentation

"""
import logging
from datetime import timedelta

from homeassistant.components.switch import SwitchDevice
from custom_components.gardena import (GARDENA_WATERING_COMPUTERS, GARDENA_LOGIN)

DEPENDENCIES = ['gardena']

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)
ICON_WATER_ON = 'mdi:water'
ICON_WATER_OFF = 'mdi:water-off'


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the gardena water computer as switches."""
    dev = []
    for watering_computer in hass.data[GARDENA_WATERING_COMPUTERS]:
        dev.append(GardenaSmartSwitch(hass, watering_computer))
    _LOGGER.debug("Adding gardena watering computers as switch")
    add_entities(dev, True)


class GardenaSmartSwitch(SwitchDevice):

    def __init__(self, hass, switch):
        """Initialize the Demo switch."""
        self._gardena = hass.data[GARDENA_LOGIN]
        self._switch = switch
        self._name = switch.name
        self._state = switch.get_valve_open()

    def update(self):
        _LOGGER.debug("Running Gardena update")
        self._gardena.update_devices()  # is a throttled update
        self._state = self._switch.get_valve_open()

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        if self._state:
            return ICON_WATER_ON
        return ICON_WATER_OFF

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        self._switch.start()

    def turn_off(self, **kwargs):
        self._switch.stop()

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._switch.get_info()
