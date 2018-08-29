from custom_components.pygardena.account import *
import objectpath


class GardenaSmartDevice:
    def __init__(self, location, raw_data):
        self.location = location  # type:GardenaSmartLocation
        self.raw_data = raw_data
        self.name = raw_data['name']
        self.zone = None
        self.id = raw_data['id']
        self.category = 'unknown'
        self.update()

    def get_value_of_property(self, ability, property):
        abilities = objectpath.Tree(self.raw_data)
        ability = objectpath.Tree(list(abilities.execute('$.abilities[@.type is '+ability+']'))[0])
        return list(ability.execute('$.properties[@.name is '+property+']'))[0]['value']

    def update(self):
        try:
            self.raw_data = self.location.get_raw_device_data(self.id)
        except:
            return False  # failed to fetch new data.

    def get_category(self):
        return self.category

    def get_battery_level(self):
        return self.get_value_of_property('battery_power', 'level')

    def get_radio_quality(self):
        return self.get_value_of_property('radio_link', 'quality')

    def get_radio_connection_status(self):
        return self.get_value_of_property('radio_link', 'connection_status')

    def get_radio_state(self):
        return self.get_value_of_property('radio_link', 'state')

    def get_info(self):
        device_info = {}
        device_info['category'] = self.get_category()
        device_info['battery_level'] = self.get_battery_level()
        device_info['radio_quality'] = self.get_radio_quality()
        device_info['radio_connection_status'] = self.get_radio_connection_status()
        device_info['radio_state'] = self.get_radio_state()
        return device_info

    def send_command(self, name, parameters=None):
        data = {'name': name}
        if parameters is not None:
            data['parameters'] = parameters
        data = json.dumps(data)

        url = 'https://smart.gardena.com/sg-1/devices/' + self.id + '/abilities/' + self.category + '/command?locationId=' + self.location.id
        headers = self.location.gardena_hub.create_header(Token=self.location.gardena_hub.AuthToken)
        self.location.gardena_hub.s.post(url, headers=headers, data=data)
        # @todo, maybe check response and do some error handing?


