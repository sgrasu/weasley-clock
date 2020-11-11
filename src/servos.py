import common
try:
    from adafruit_servokit import ServoKit
except NotImplementedError:
    assert common.debugging
    from servo_mock import ServoKit

MAX_ROTATIONS = 2
kit = ServoKit(channels=16)


def set_servo_angle(servo, angle):
    kit.servo[servo].angle = angle * 2  # gear ratio of 2 from servo to hand


def current_angle(servo):
    return kit.servo[servo].angle


def face_2_angle(region):
    return region * 30


def next_angle(curr, dest):
    pos_curr = curr % 360
    pos_dest = dest % 360
    curr_rotations = curr // 360
    if -180 <= pos_curr - pos_dest <= 180:
        next = curr_rotations * 360 + pos_dest
    elif 180 <= pos_curr - pos_dest <= 360:
        if curr_rotations + 1 >= MAX_ROTATIONS:
            next = curr_rotations * 360 + pos_dest
        else:
            next = (curr_rotations + 1) * 360 + pos_dest
    elif -360 <= pos_curr - pos_dest <= -180:
        if curr_rotations <= 0:
            next = curr_rotations * 360 + pos_dest
        else:
            next = (curr_rotations - 1) * 360
    else:
        next = dest
    return next


def move_hand(servo, region):
    angle = next_angle(current_angle(servo), face_2_angle(region))
    set_servo_angle(servo, angle)
