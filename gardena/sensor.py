"""
Gardena smart sensor which registers a couple of sensors.

@ todo something with documentation

"""
import logging
from datetime import timedelta

from homeassistant.const import (
    ATTR_BATTERY_LEVEL, TEMP_CELSIUS, DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_TEMPERATURE)
from homeassistant.helpers.entity import Entity
from custom_components.gardena import (GARDENA_SENSORS, GARDENA_WATERING_COMPUTERS, GARDENA_LOGIN)

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['gardena']

SCAN_INTERVAL = timedelta(minutes=5)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Demo sensors."""
    dev = []
    for sensor in hass.data[GARDENA_SENSORS]:
        dev.append(GardenaSmartAmbientTemperatureSensor(hass, sensor))
        dev.append(GardenaSmartSoilTemperatureSensor(hass, sensor))
        dev.append(GardenaSmartSoilHumiditySensor(hass, sensor))
        dev.append(GardenaSmartLightSensor(hass, sensor))
    _LOGGER.debug("Adding gardena sensors as sensors")
    for watering_computer in hass.data[GARDENA_WATERING_COMPUTERS]:
        dev.append(GardenaSmartAmbientTemperatureSensor(hass, watering_computer))
    _LOGGER.debug("Adding gardena watering computers as sensors")
    add_entities(dev, True)

class GardenaSmartSensor(Entity):
    """Representation of a Demo sensor."""

    def __init__(self, hass, sensor):
        self._sensor = sensor
        self.gardena = hass.data[GARDENA_LOGIN]

    def update(self):
        _LOGGER.debug("Running Gardena update")
        self.gardena.update_devices()  # is a throttled update

    @property
    def device_class(self):
        return self._device_class

    @property
    def name(self):
        return self._name

    @property
    def unit_of_measurement(self):
        return self._unit_of_measurement

    @property
    def device_state_attributes(self):
        return self._sensor.get_generic_info()

class GardenaSmartAmbientTemperatureSensor(GardenaSmartSensor):
    def __init__(self, hass, sensor):
        """Initialize the sensor."""
        super().__init__(hass, sensor)
        self._name = sensor.name + ' ambient temperature'
        self._device_class = DEVICE_CLASS_TEMPERATURE
        self._unit_of_measurement = TEMP_CELSIUS

    @property
    def state(self):
        return self._sensor.get_ambient_temperature()


class GardenaSmartSoilTemperatureSensor(GardenaSmartSensor):
    def __init__(self, hass, sensor):
        """Initialize the sensor."""
        super().__init__(hass, sensor)
        self._name = sensor.name + ' soil temperature'
        self._device_class = DEVICE_CLASS_TEMPERATURE
        self._unit_of_measurement = TEMP_CELSIUS

    @property
    def state(self):
        return self._sensor.get_soil_temperature()

class GardenaSmartSoilHumiditySensor(GardenaSmartSensor):
    def __init__(self, hass, sensor):
        """Initialize the sensor."""
        super().__init__(hass, sensor)
        self._name = sensor.name + ' soil humidity'
        self._device_class = DEVICE_CLASS_HUMIDITY
        self._unit_of_measurement = '%'

    @property
    def state(self):
        return self._sensor.get_soil_humidity()


class GardenaSmartLightSensor(GardenaSmartSensor):
    def __init__(self, hass, sensor):
        """Initialize the sensor."""
        super().__init__(hass, sensor)
        self._name = sensor.name + ' light'
        self._device_class = 'illuminance'
        self._unit_of_measurement = 'lux'

    @property
    def state(self):
        return self._sensor.get_light()
