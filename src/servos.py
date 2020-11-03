from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

MAX_ROTATIONS = 2

def set_servo_angle(servo,angle):
    kit.servo[servo].angle = angle * 2

def face_2_angle(face):
    return face * 30

def next_angle(curr, dest):
    pos_curr = curr % 360
    pos_dest = dest % 360
    curr_rotations = curr // 360
    if -180 <= pos_curr - pos_dest <= 180:
        next = curr_rotations * 360 + pos_dest
    elif 180 <= pos_curr - pos_dest <= 360:
        if curr_rotations >= MAX_ROTATIONS:
            next = curr_rotations * 360 + pos_dest
        else: next = (curr_rotations + 1) * 360
    elif -360 <= pos_curr - pos_dest <= -180:
        if curr_rotations <= 0:
            next = curr_rotations * 360 + pos_dest
        else: next = (curr_rotations - 1) * 360
    else: next = dest
    return next
