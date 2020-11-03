"""Life 360 interace
Very basic functionailty to create and interact
with a life360 session"""

import os
import requests
from requests.auth import HTTPBasicAuth

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) '\
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

class Life360Session:
    family_id = os.environ["LIFE360_CIRCLE"]
    def __init__(self):
        self.authenticate()
    def family(self):
        family_info(self.access_token, self.family_id)
    def authenticate(self):
        self.access_token= authenticate()

def authenticate():
    user = os.environ["LIFE360_USER"]
    pas = os.environ["LIFE360_PASS"]
    basicauth_user = os.environ["LIFE360_BASICAUTH_USER"]
    basicauth_pass = os.environ["LIFE360_BASICAUTH_PASS"]
    response = requests.post(
        'https://www.life360.com/v3/oauth2/token',
        data={'username': user, 'password': pas, 'grant_type': 'password'},
        headers={'Accept': 'application/json', 'User-Agent' : USER_AGENT},
        auth=HTTPBasicAuth(basicauth_user, basicauth_pass))
    print(response.request.headers)
    print(response.request.url)
    response = response.json()
    return response['access_token']

def get(auth_token, endpoint):
    auth = 'Bearer ' + auth_token
    response = requests.get('https://www.life360.com/v3/' + endpoint,
    headers={'Accept': 'application/json', 'User-Agent' : USER_AGENT, \
        'Authorization' : auth})
    return response.json()

def circles(auth_token):
    response = get(auth_token, 'circles')
    return response

def get_circle(auth_token, circle_id):
    response = get(auth_token, 'circles/' + circle_id)
    return response

def parse_member(member):
    info = {}
    location = member['location']
    if location:
        info['name'] = location['name'] 
        battery = location['battery']
        info['battery_critical'] = (battery is None or int(battery) < 5)
        info['driving'] = location['isDriving']
    return info

def family_info(auth_token,circle_id):
    circle = get_circle(auth_token, circle_id)
    return {member['firstName'] : parse_member(member) for member in circle['members']}
