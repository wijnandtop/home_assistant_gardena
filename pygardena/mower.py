from custom_components.pygardena.device import *

class GardenaSmartMower(GardenaSmartDevice):
    def __init__(self, location, raw_data):
        super().__init__(location, raw_data)
        self.category = "mower"

    def start(self, duration=1440):
        self.send_command('start_override_timer', {'duration': duration})

    def park_until_timer(self):
        self.send_command('park_until_next_timer')

    def park(self):
        self.send_command('park_until_further_notice')

    # def get_mower_error(self):
    #     abilities = objectpath.Tree(self.device_info[id]);
    #     ability = objectpath.Tree(list(abilities.execute('$.abilities[@.type is robotic_mower]'))[0])
    #     """Return error and last ts"""
    #         return self.get_value_of_property('robotic_mower', 'status')
    #     return (list(ability.execute('$.properties[@.name is error]'))[0]['value'], list(ability.execute('$.properties[@.name is timestamp_last_error_code]'))[0]['value'])

    def get_manual_operation(self):
        return self.get_value_of_property('robotic_mower', 'manual_operation')
    def get_status(self):
        return self.get_value_of_property('robotic_mower', 'status')
    def get_last_error_code(self):
        return self.get_value_of_property('robotic_mower', 'last_error_code')
    def get_source_for_next_start(self):
        return self.get_value_of_property('robotic_mower', 'source_for_next_start')
    def get_timestamp_next_start(self):
        return self.get_value_of_property('robotic_mower', 'timestamp_next_start')
    def get_cutting_time(self):
        return self.get_value_of_property('robotic_mower_stats', 'cutting_time')
    def get_charging_cycles(self):
        return self.get_value_of_property('robotic_mower_stats', 'charging_cycles')
    def get_collisions(self):
        return self.get_value_of_property('robotic_mower_stats', 'collisions')
    def get_running_time(self):
        return self.get_value_of_property('robotic_mower_stats', 'running_time')

    def get_info(self):
        device_info = super().get_info()
        #add mower specific details to device info
        device_info['manual_operation'] = self.get_manual_operation()
        device_info['status'] = self.get_status()
        device_info['last_error_code'] = self.get_last_error_code()
        device_info['source_for_next_start'] = self.get_source_for_next_start()
        device_info['timestamp_next_start'] = self.get_timestamp_next_start()
        device_info['cutting_time'] = self.get_cutting_time()
        device_info['charging_cycles'] = self.get_charging_cycles()
        device_info['collisions'] = self.get_collisions()
        device_info['running_time'] = self.get_running_time()
        return  device_info
