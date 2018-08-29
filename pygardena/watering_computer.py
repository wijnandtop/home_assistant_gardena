from custom_components.pygardena.device import *

class GardenaSmartWateringComputer(GardenaSmartDevice):
    def __init__(self, location, raw_data):
        super().__init__(location, raw_data)
        self.category = "watering_computer"


    def get_battery_status(self):
        return self.get_value_of_property('battery_power', 'disposable_battery_status')
    def get_ambient_temperature(self):
        return self.get_value_of_property('ambient_temperature_sensor', 'temperature')
    def get_ambient_frost_warning(self):
        return self.get_value_of_property('ambient_temperature_sensor', 'frost_warning')
    def get_valve_open(self):
        return self.get_valve_open('watering_outlet', 'valve_open')
    def get_manual_override(self):
        return self.get_valve_open('watering_outlet', 'manual_override')
    def get_button_manual_override_time(self):
        return self.get_valve_open('watering_outlet', 'button_manual_override_time')
    def get_last_manual_override_time(self):
        return self.get_valve_open('watering_outlet', 'last_manual_override_time')
    def get_scheduled_watering_next_start(self):
        return self.get_valve_open('scheduling', 'scheduled_watering_next_start')
    def get_scheduled_watering_end(self):
        return self.get_valve_open('scheduling', 'scheduled_watering_end')
    def get_adaptive_scheduling_last_decision(self):
        return self.get_valve_open('scheduling', 'adaptive_scheduling_last_decision')

    def get_generic_info(self):
        device_info = super().get_info()
        #add sensor specific details to device info
        device_info['battery_status'] = self.get_battery_status()
        return device_info

    def get_info(self):
        device_info = self.get_generic_info()
        device_info['ambient_temperature'] = self.get_ambient_temperature()
        device_info['ambient_frost_warning'] = self.get_ambient_frost_warning()
        device_info['valve_open'] = self.get_valve_open()
        device_info['manual_override'] = self.get_manual_override()
        device_info['button_manual_override_time'] = self.get_button_manual_override_time()
        device_info['last_manual_override_time'] = self.get_last_manual_override_time()
        device_info['scheduled_watering_next_start'] = self.get_scheduled_watering_next_start()
        device_info['scheduled_watering_end'] = self.get_scheduled_watering_end()
        device_info['adaptive_scheduling_last_decision'] = self.get_adaptive_scheduling_last_decision()
        return  device_info

    def start(self, duration=30):
        self.send_command('manual_override', {'duration': duration})

    def stop(self):
        self.send_command('cancel_override')
