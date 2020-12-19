"""Life 360 interace
Very basic functionailty to create and interact
with a life360 session"""

import logging
import sys
import os
import requests
from requests.auth import HTTPBasicAuth

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) '\
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'


class LogoutError(Exception):
    pass


def reauthenticate(f):
    def wrapper(session):
        try:
            return f(session)
        except LogoutError:
            session.authenticate()
            return f(session)
    return wrapper


class Life360Session:
    family_id = os.environ["LIFE360_CIRCLE"]

    def __init__(self):
        self.access_token = None
        self.authenticate()

    def authenticate(self):
        self.access_token = authenticate()

    @reauthenticate
    def family(self):
        return family_info(self.access_token, self.family_id)

    @reauthenticate
    def circles(self):
        return circles(self.access_token)


def log_and_retry(f):
    def wrapper(*args):
        retry = 0
        while True:
            try:
                return f(*args)
            except ConnectionError:
                logging.error("internet connection error")
            except LogoutError:
                logging.info("credentials expired")
                raise
            except BaseException:
                logging.error("Unknown error: %s", sys.exc_info()[0])
                raise
            finally:
                if retry == 2:
                    logging.error("Life360 retries exceeded, exiting")
                    quit()
                retry += 1
    return wrapper


@log_and_retry
def authenticate():
    logging.info("auth attempt")
    user = os.environ["LIFE360_USER"]
    pas = os.environ["LIFE360_PASS"]
    basicauth_user = os.environ["LIFE360_BASICAUTH_USER"]
    basicauth_pass = os.environ["LIFE360_BASICAUTH_PASS"]
    response = requests.post(
        'https://www.life360.com/v3/oauth2/token',
        data={'username': user, 'password': pas, 'grant_type': 'password'},
        headers={'Accept': 'application/json', 'User-Agent': USER_AGENT},
        auth=HTTPBasicAuth(basicauth_user, basicauth_pass))
    if response.status_code == 403:
        logging.error("incorrect auth: %s", response.json()['errorMessage'])
        quit()
    return response.json()['access_token']


@log_and_retry
def get(auth_token, endpoint):
    auth = 'Bearer ' + auth_token
    response = requests.get(
        'https://www.life360.com/v3/' + endpoint,
        headers={
            'Accept': 'application/json',
            'User-Agent': USER_AGENT,
            'Authorization': auth})
    if response.status_code != 200:
        if response.status_code == 401:
            raise LogoutError
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
        info['name'] = location['name'].lower() if location['name'] else "lost"
        battery = location['battery']
        info['battery_critical'] = (battery is None or float(battery) < 5)
        info['driving'] = location['speed'] > 13
    info['location'] = 'battery' if info['battery_critical'] \
        else 'driving' if info['driving'] \
        else info['name'].split('-')[-1].strip().lower() if info['name'] \
        else 'lost'
    return info


def family_info(auth_token, circle_id):
    circle = get_circle(auth_token, circle_id)
    return {member['firstName'].lower(): parse_member(member)
            for member in circle['members']}
