from custom_components.pygardena.device import *

class GardenaSmartSensor(GardenaSmartDevice):
    def __init__(self, location, raw_data):
        super().__init__(location, raw_data)
        self.category = "sensor"


    def get_battery_status(self):
        return self.get_value_of_property('battery_power', 'disposable_battery_status')
    def get_ambient_temperature(self):
        return self.get_value_of_property('ambient_temperature_sensor', 'temperature')
    def get_ambient_frost_warning(self):
        return self.get_value_of_property('ambient_temperature_sensor', 'frost_warning')
    def get_soil_temperature(self):
        return self.get_value_of_property('soil_temperature_sensor', 'temperature')
    def get_soil_humidity(self):
        return self.get_value_of_property('soil_humidity_sensor', 'humidity')
    def get_light(self):
        return self.get_value_of_property('light_sensor', 'light')

    def get_generic_info(self):
        device_info = super().get_info()
        #add sensor specific details to device info
        device_info['battery_status'] = self.get_battery_status()
        return device_info

    def get_info(self):
        device_info = self.get_generic_info()
        device_info['ambient_temperature'] = self.get_ambient_temperature()
        device_info['ambient_frost_warning'] = self.get_ambient_frost_warning()
        device_info['soil_temperature'] = self.get_soil_temperature()
        device_info['soil_humidity'] = self.get_soil_humidity()
        device_info['light'] = self.get_light()
        return  device_info
