"""Life 360 mock
for testing clock"""

import random
import yaml
from common import CLOCK

class Life360Session:

    def __init__(self):
        self.access_token = None
        self.authenticate()

    def authenticate(self):
        self.access_token = authenticate()

    def family(self):
        return family_info()

    def circles(self):
        return circles()


def authenticate():
    return "we dont care"


def circles():
    return ["1234-567-890"]


def get_circle():
    return "123456789"

location_options = list(CLOCK['face'].keys())

def create_member():
    info = {}
    info['name'] = location_options[random.randrange(len(location_options))]
    info['battery_critical'] = random.random() > 0.8
    info['driving'] = random.random() > 0.8
    info['location'] = 'battery' if info['battery_critical'] \
        else 'driving' if info['driving'] \
        else info['name']
    return info

def family_info():
    return {member.lower(): create_member()
            for member in CLOCK['hands'].keys()}
