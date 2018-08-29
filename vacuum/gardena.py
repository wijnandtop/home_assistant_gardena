"""
Support for Neato Connected Vacuums.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/vacuum.neato/
"""
import logging
from datetime import timedelta

from homeassistant.components.vacuum import (
    StateVacuumDevice, SUPPORT_BATTERY, SUPPORT_PAUSE, SUPPORT_RETURN_HOME,
    SUPPORT_STATE, SUPPORT_STOP, SUPPORT_START, STATE_IDLE,
    STATE_PAUSED, STATE_CLEANING, STATE_DOCKED, STATE_RETURNING, STATE_ERROR,
    SUPPORT_MAP, ATTR_STATUS, ATTR_BATTERY_LEVEL, ATTR_BATTERY_ICON,
    SUPPORT_LOCATE)
from custom_components.gardena import (GARDENA_MOWERS, GARDENA_LOGIN)

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['gardena']

SCAN_INTERVAL = timedelta(minutes=5)

SUPPORT_GARDENA = SUPPORT_BATTERY | SUPPORT_RETURN_HOME | \
                SUPPORT_STOP | SUPPORT_START | \
                SUPPORT_STATE


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Neato vacuum."""
    dev = []
    for mower in hass.data[GARDENA_MOWERS]:
        dev.append(GardenaSmartMower(hass, mower))
    _LOGGER.debug("Adding mower as vacuums %s", dev)
    add_entities(dev, True)


class GardenaSmartMower(StateVacuumDevice):
    """Representation of a Neato Connected Vacuum."""

    def __init__(self, hass, robot):
        """Initialize the Neato Connected Vacuum."""
        self.robot = robot  # type:
        self.gardena = hass.data[GARDENA_LOGIN]
        self._name = '{}'.format(self.robot.name)

    def update(self):
        """Update the states of Gardena devices."""
        _LOGGER.debug("Running Gardena update")
        self.gardena.update_devices()  # is a throttled update

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def supported_features(self):
        """Flag lawn mower robot features that are supported."""
        return SUPPORT_GARDENA

    @property
    def battery_level(self):
        """Return the battery level of the lawn mower."""
        return self.robot.get_battery_level()

    @property
    def state(self):
        """Return the status of the lawn mower."""
        return self.robot.get_status()

    @property
    def device_state_attributes(self):
        """Return the state attributes of the lawn mower."""
        return self.robot.get_info()

    def start(self):
        """Start cleaning or resume cleaning."""
        self.robot.start()

    def return_to_base(self, **kwargs):
        """Set the lawn mower to return to the dock."""
        # self._clean_state = STATE_RETURNING
        self.robot.park_until_timer()

    def stop(self, **kwargs):
        """Stop the lawn mower."""
        self.robot.park()
