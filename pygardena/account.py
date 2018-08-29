import json
from custom_components.pygardena.location import *
import requests


class GardenaSmartAccount:
    def __init__(self, email_address=None, password=None):
        self.locations = set()
        self.raw_locations = None
        self.s = requests.session()
        self.email_address = email_address
        self.password = password
        self.update_authtokens()

    def load_locations(self):
        url = "https://smart.gardena.com/sg-1/locations/"
        params = (
            ('user_id', self.userID),
        )
        headers = self.create_header(Token=self.AuthToken)
        response = self.s.get(url, headers=headers, params=params)
        response_data = json.loads(response.content.decode('utf-8'))
        self.raw_locations = response_data
        for location in response_data['locations']:
            self.locations.add(GardenaSmartLocation(self, location))

    def get_raw_location_data(self, location_id):
        for location in self.raw_locations:
            if location.id == location_id:
                return location
        # @todo trow exception if not found

    def create_header(self, Token=None, ETag=None):
        headers={
            'Content-Type': 'application/json',
        }
        if Token is not None:
            headers['X-Session']=Token
        if ETag is not None:
            headers['If-None-Match'] = ETag
        return headers

    def update_authtokens(self):
        """Get authentication token from servers"""
        data = '{"sessions":{"email":"' + self.email_address + '","password":"' + self.password + '"}}'
        url = 'https://smart.gardena.com/sg-1/sessions'
        headers = self.create_header()
        response = self.s.post(url, headers=headers, data=data)
        response_data = json.loads(response.content.decode('utf-8'))
        self.AuthToken = response_data['sessions']['token']
        self.refreshToken = response_data['sessions']['refresh_token']
        self.userID = response_data['sessions']['user_id']

    def get_all_mowers(self):
        all_mowers = set()
        for location in self.locations:
            for mower in location.get_mowers():
                all_mowers.add(mower)
        return all_mowers

