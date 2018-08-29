"""
Support for Gardena Smart connected devices.
For more details about this component, please refer to the documentation at
https://home-assistant.io/components/@todo
"""
import logging
from datetime import timedelta
# from urllib.error import HTTPError

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers import discovery
from homeassistant.util import Throttle
from custom_components.pygardena.account import *

_LOGGER = logging.getLogger(__name__)

# REQUIREMENTS = ['pybotvac==0.0.9']

# _LOGGER.warn('component gardena bla')

DOMAIN = 'gardena'
GARDENA_MOWERS = 'gardena_smart_mowers'
GARDENA_LOGIN = 'gardena_login'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    })
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Set up the Gardena component."""
    hass.data[GARDENA_LOGIN] = GardenaHub(hass, config[DOMAIN], GardenaSmartAccount)
    hub = hass.data[GARDENA_LOGIN]
    _LOGGER.info('component gardena setup')

    # if not hub.login():
    #     _LOGGER.debug("Failed to login to Gardena API")
    #     return False
    hub.update_devices()
    # for component in ('vacuum','sensor'):
    discovery.load_platform(hass, 'vacuum', DOMAIN, {}, config)

    return True


class GardenaHub:
    """A My Gardena hub wrapper class."""

    def __init__(self, hass, domain_config, gardena):
        """Initialize the Gardena hub."""
        self.config = domain_config
        self._gardena = gardena
        self._hass = hass

        self.my_gardena = gardena(
            domain_config[CONF_USERNAME],
            domain_config[CONF_PASSWORD]) # type: GardenaSmartAccount
        self._hass.data[GARDENA_MOWERS] = self.my_gardena.get_all_mowers()

    # def login(self):
    #     """Login to Gardena."""
    #     try:
    #         _LOGGER.debug("Trying to connect to Gardena API")
    #         self.my_neato = self._gardena(
    #             self.config[CONF_USERNAME], self.config[CONF_PASSWORD])
    #         return True
    #     except HTTPError:
    #         _LOGGER.error("Unable to connect to Gardena API")
    #         return False

    @Throttle(timedelta(seconds=300))
    def update_devices(self):
        """load all locations, locations will autoload their devices"""
        self.my_gardena.load_locations()
        """Update the robot states, will be used by the seperate devices."""
        _LOGGER.debug("Running HUB.update_robots %s",
                      self._hass.data[GARDENA_MOWERS])
        self._hass.data[GARDENA_MOWERS] = self.my_gardena.get_all_mowers()
        _LOGGER.info(self._hass.data[GARDENA_MOWERS])
