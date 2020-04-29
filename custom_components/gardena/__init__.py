"""
Support for Gardena Smart connected devices.
For more details about this component, please refer to the documentation at
https://home-assistant.io/components/@todo
"""
import logging
from datetime import timedelta

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers import discovery
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['wt.pygardena==0.9.6']

SCAN_INTERVAL = timedelta(minutes=5)

DOMAIN = 'gardena'
GARDENA_MOWERS = 'gardena_smart_mowers'
GARDENA_SENSORS = 'gardena_smart_sensors'
GARDENA_WATERING_COMPUTERS = 'gardena_smart_watering_computers'
GARDENA_LOGIN = 'gardena_login'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    })
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Set up the Gardena component."""
    from wt.pygardena.account import GardenaSmartAccount
    hass.data[GARDENA_LOGIN] = GardenaHub(hass, config[DOMAIN], GardenaSmartAccount)
    _LOGGER.debug('component gardena setup')
    # for component in ('vacuum','sensor'):
    discovery.load_platform(hass, 'vacuum', DOMAIN, {}, config)
    discovery.load_platform(hass, 'sensor', DOMAIN, {}, config)
    discovery.load_platform(hass, 'binary_sensor', DOMAIN, {}, config)
    discovery.load_platform(hass, 'switch', DOMAIN, {}, config)

    return True


class GardenaHub:
    """A My Gardena hub wrapper class."""

    def __init__(self, hass, domain_config, gardena):
        """Initialize the Gardena hub."""
        self.config = domain_config
        self._gardena = gardena
        self._hass = hass

        self.my_gardena = gardena(domain_config[CONF_USERNAME], domain_config[CONF_PASSWORD])
        self._hass.data[GARDENA_MOWERS] = self.my_gardena.get_all_mowers()
        self._hass.data[GARDENA_SENSORS] = self.my_gardena.get_all_sensors()
        self._hass.data[GARDENA_WATERING_COMPUTERS] = self.my_gardena.get_all_watering_computers()

    @Throttle(timedelta(seconds=300))
    def update_devices(self):
        """load all locations, locations will autoload their devices"""
        """Update the robot states, will be used by the seperate devices."""
        self.my_gardena.update_devices()
        _LOGGER.debug("Running HUB.update_devices")

