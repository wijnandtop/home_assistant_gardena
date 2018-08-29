from custom_components.pygardena.account import *
from custom_components.pygardena.mower import *
import json


class GardenaSmartLocation:
    def __init__(self, gardena_hub, raw_data):
        self.gardena_hub = gardena_hub  # type:GardenaSmartAccount
        self.raw_data = raw_data
        self.raw_devices = None
        self.name = raw_data['name']
        self.id = raw_data['id']
        self.devices_mower = set()
        self.load_devices()

    def update(self):
        try:
            self.raw_data = self.gardena_hub.get_raw_location_data(self.id)
        except:
            return False  # failed to fetch new data.

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_latitude(self):
        return self.raw_data['geo_position']['latitude']

    def get_longitude(self):
        return self.raw_data['geo_position']['longitude']

    def get_address(self):
        return self.raw_data['geo_position']['address']

    def get_city(self):
        return self.raw_data['geo_position']['city']

    def get_sunrise(self):
        return self.raw_data['geo_position']['sunrise']

    def get_sunset(self):
        return self.raw_data['geo_position']['sunset']

    def get_info(self):
        location_info = {}
        location_info['id'] = self.get_id()
        location_info['name'] = self.get_name()
        location_info['latitude'] = self.get_latitude()
        location_info['longitude'] = self.get_longitude()
        location_info['address'] = self.get_address()
        location_info['city'] = self.get_city()
        location_info['sunrise'] = self.get_sunrise()
        location_info['sunset'] = self.get_sunset()
        return location_info

    def get_devices(self):
        return self.devices

    def update_devices(self):
        self.update_raw_data()
        for device in self.devices_mower:
            device.update()

    def update_raw_data(self):
        url = "https://smart.gardena.com/sg-1/devices"
        params = (
            ('locationId', self.id),
        )
        headers = self.gardena_hub.create_header(Token=self.gardena_hub.AuthToken)
        response = self.gardena_hub.s.get(url, headers=headers, params=params)
        response_data = json.loads(response.content.decode('utf-8'))
        self.raw_devices = response_data

    def get_raw_device_data(self, device_id):
        for device in self.raw_json:
            if device.id == device_id:
                return device
        # @todo trow exception if not found

    def get_mowers(self):
        return self.devices_mower

    def load_devices(self):
        self.update_raw_data()
        for device in self.raw_devices['devices']:
            if device['category'] == 'mower':
                self.devices_mower.add(GardenaSmartMower(self, device))


