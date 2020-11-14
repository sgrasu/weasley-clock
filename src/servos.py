import common
try:
    from adafruit_servokit import ServoKit
except NotImplementedError:
    assert common.debugging
    from servo_mock import ServoKit
from common import CLOCK


MAX_ROTATIONS = 2
kit = ServoKit(channels=16)
SERVO_COUNT = 4
assert 360 % len(CLOCK['face']) == 0
QUADRANT_ANGLE = 360 // len(CLOCK['face'])

for name, person in CLOCK['hands'].items():
    kit.servo[person['servo']].actuation_range = person['range']
    kit.servo[person['servo']].set_pulse_width_range(person['min'], person['max'])


def set_servo_angle(servo, angle):
    kit.servo[servo].angle = angle * 2  # gear ratio of 2 from servo to hand


def current_angle(servo):
    return int(kit.servo[servo].angle // 2)


def face_2_angle(region):
    return region * QUADRANT_ANGLE

def unit_angle(angle):
    return angle % 360 - angle % QUADRANT_ANGLE

def calculate_offset(num):
    offset = QUADRANT_ANGLE / (SERVO_COUNT + 2)
    return offset * [0, 1, -1, 2][num]  #alternating offset


def next_angle(servo, curr, dest):
    print(dest)
    pos_curr = unit_angle(curr)
    servos_in_quadrant = len([x for x in range(SERVO_COUNT) if x < servo and unit_angle(current_angle(x)) == unit_angle(dest)])
    pos_dest = (dest + calculate_offset(servos_in_quadrant)) % 360
    curr_rotations = curr // 360
    if -180 <= pos_curr - pos_dest <= 180:
        nxt_rotations = curr_rotations * 360
    elif 180 <= pos_curr - pos_dest <= 360:
        if curr_rotations + 1 >= MAX_ROTATIONS:
            nxt_rotations = curr_rotations * 360
        else:
            nxt_rotations = (curr_rotations + 1) * 360
    elif -360 <= pos_curr - pos_dest <= -180:
        if curr_rotations <= 0:
            nxt_rotations = curr_rotations * 360
        else:
            nxt_rotations = (curr_rotations - 1) * 360
    else:
        nxt_rotations = 0
    print("conv:", nxt_rotations, pos_dest)
    return nxt_rotations + pos_dest


def move_hand(servo, region):
    angle = next_angle(servo, current_angle(servo), face_2_angle(region))
    set_servo_angle(servo, angle)
