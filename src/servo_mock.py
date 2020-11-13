import logging


class Servo:
    def __init__(self, idx):
        self.idx = idx
        self._angle = 0

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, new_angle):
        old_angle = self._angle
        self._angle = new_angle
        assert (new_angle / 2) % 1 == 0
        logging.debug(
            "servo %s changed from %s to %s",
            self.idx,
            old_angle / 2,
            new_angle / 2)


class ServoKit:
    servo = {i: Servo(i) for i in range(4)}

    def __init__(self, **_):
        return
