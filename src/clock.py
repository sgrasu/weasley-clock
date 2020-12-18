import logging
import time
import common
if not common.debugging:
    from life_api import Life360Session
else:
    from life_api_mock import Life360Session
import servos
from common import CLOCK


def zero_hands():
    for servo in range(3):
        servos.set_servo_angle(servo, 0)
        

def hand_position(location, **_):
    return CLOCK['face'].get(location, CLOCK['face']['lost'])


def move_hand(servo, location_data):
    region = hand_position(**location_data)
    servos.move_hand(servo, region)


def update_clock(tracker):
    fam = tracker.family()
    clock = {
        name: {
            'servo': config['servo'],
            'location_data': fam[name]} for name,
        config in CLOCK['hands'].items()}
    for name, data in clock.items():
        logging.debug("loc data for %s, servo: %s, location : %s, region : %s",
                      name,
                      data['servo'],
                      data['location_data']['location'],
                      hand_position(**data['location_data']))
        move_hand(**data)


def start_clock_service():
    tracker = Life360Session()
    if common.debugging:
        logging.basicConfig(level=logging.DEBUG)
    while True:
        update_clock(tracker)
        time.sleep(common.interval)


if __name__ == "__main__":
   start_clock_service()
