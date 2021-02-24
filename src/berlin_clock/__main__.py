import argparse
import sched
import sys
import time
from datetime import datetime
from itertools import cycle, islice
from functools import partial
from curses import wrapper

from berlin_clock import __version__


def convert_to_blocks(timestamp):
    hours, minutes, seconds = parse_time(timestamp)

    large_hours = hours // 5
    small_hours = hours - (large_hours * 5)
    large_minutes = minutes // 5
    small_minutes = minutes - (large_minutes * 5)

    return [large_hours, small_hours, large_minutes, small_minutes]


def parse_time(timestamp):
    return [int(timestamp[:2]), int(timestamp[3:5]), int(timestamp[6:8])]


def make_parser(prog):
    """
    :param prog: string name of the utility.
    :returns: Parser for the CLI utility berlin_clock.
    """
    parser = argparse.ArgumentParser(
        prog=prog, description="Displays a berlin clock in the terminal."
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )
    return parser


def parse_args(argv):
    """
    Parses the given list of command line arguments.

    :param argv: List of arguments, e.g. ["berlin_clock", "-v"]
    :returns: argparse namespace of the parsed arguments.
    """
    parser = make_parser(argv[0])
    return parser.parse_args(argv[1:])


def print_image_clock(timestamp):
    timeblocks = convert_to_blocks(timestamp)


def generate_string(n, color="Y"):
    return color * n + "O" * (4 - n)


def generate_special_string(n):
    basis = "YYR"
    return "".join(islice(cycle(basis), n)) + "O" * (11 - n)


def generate_top_row(timestamp):
    _, _, seconds = parse_time(timestamp)
    if seconds % 2 == 0:
        return "Y"
    else:
        return "O"


def print_row_clock(timestamp):
    print(generate_top_row(timestamp))

    (
        first_row_lamps,
        second_row_lamps,
        third_row_lamps,
        fourth_row_lamps,
    ) = convert_to_blocks(timestamp)

    print(generate_string(first_row_lamps))
    print(generate_string(second_row_lamps))
    print(generate_special_string(third_row_lamps))
    print(generate_string(fourth_row_lamps, color="R"))


def print_berlin_clock(time):
    """
    Prints a representation of the given time similar to The Berlin Uhr. On the
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

    Y = Yellow
    R = Red
    O = Off


    :param time: A datetime object for the time to be displayed.
    """
    current_time = time.strftime("%H:%M:%S")
    print("\rCurrent Time =", current_time)
    print_row_clock(current_time)


def run_berlin_clock(args):
    """
    Runs print_berlin_clock every second.

    :param args: argparse namespace of the command line arguments.
    """
    scheduler = sched.scheduler(time.time, time.sleep)

    def event_loop():
        print_berlin_clock(datetime.now())
        scheduler.enter(1, 1, event_loop)

    scheduler.enter(1, 1, event_loop)
    scheduler.run()


def parse_args_and_run(argv):
    """
    parses the given list of arguments and runs run_berlin_clock.

    :param argv: List of arguments, e.g. ["berlin_clock", "-v"]
    """
    run_berlin_clock(parse_args(argv))


def main():
    parse_args_and_run(sys.argv)


if __name__ == "__main__":
    main()
