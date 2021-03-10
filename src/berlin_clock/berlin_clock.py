from dataclasses import dataclass
from enum import Enum


class Color(Enum):
    YELLOW = 1
    RED = 2


@dataclass
class Light:
    color: Color = Color.YELLOW
    on: bool = False


def set_light_row(light_row: [Light], num_lights: int):
    """
    Sets the number of lights in a light row of a berlin clock,
    which is on to the left, and off to the right.
    """
    if num_lights < 0:
        raise ValueError("negative amount of lights to set!")
    if num_lights > len(light_row):
        raise ValueError("Tried to set more lights than length of row.")
    for i, l in enumerate(light_row):
        l.on = i < num_lights


def num_lights_on(light_row: [Light]):
    """
    Counts the number of lights in a light row of a berlin clock,
    which is on to the left, and off to the right.
    raises an error if the number of lights on is not on first and
    then off.
    """
    off = False
    num_on = 0
    for l in light_row:
        if not l.on:
            off = True
        if l.on:
            if off:
                raise ValueError("Lights on are not in order!")
            num_on += 1
    return num_on


class BerlinClock:
    """
    The Berlin Uhr. On the
    top of the berlin uhr there is a yellow lamp that blinks on/off every two
    seconds. The time is calculated by adding turned on lamps.

    The top two rows of lamps are red. These indicate the hours of a day. In
    the top row there are 4 red lamps. Every lamp represents 5 hours. In the
    lower row of red lamps every lamp represents 1 hour. So if two lamps of the
    first row and three of the second row are switched on that indicates
    5+5+3=13h or 1 pm.

    The two rows of lamps at the bottom count the minutes. The first of these
    rows has 11 lamps, the second 4. In the first row every lamp represents 5
    minutes. In this first row the 3rd, 6th and 9th lamp are red and indicate
    the first quarter, half and last quarter of an hour. The other lamps are
    yellow. In the last row with 4 lamps every lamp represents 1 minute.

    The lamps are switched on from left to right.
    """

    def __init__(self):
        self.top_light = Light()
        self.first_row = [Light(Color.RED) for _ in range(4)]
        self.second_row = [Light(Color.RED) for _ in range(4)]
        self.third_row = [
            Light(Color.YELLOW),
            Light(Color.YELLOW),
            Light(Color.RED),
            Light(Color.YELLOW),
            Light(Color.YELLOW),
            Light(Color.RED),
            Light(Color.YELLOW),
            Light(Color.YELLOW),
            Light(Color.RED),
            Light(Color.YELLOW),
            Light(Color.YELLOW),
        ]
        self.last_row = [Light() for _ in range(4)]

    def set_time(self, time):
        self.top_light.on = time.second % 2 == 0
        set_light_row(self.first_row, time.hour // 5)
        set_light_row(self.second_row, time.hour % 5)
        set_light_row(self.third_row, time.minute // 5)
        set_light_row(self.last_row, time.minute % 5)
