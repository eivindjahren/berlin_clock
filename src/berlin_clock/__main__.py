import argparse
import sched
import sys
import time
from datetime import datetime

from berlin_clock import __version__


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


def print_top_circle(time):
    if time.second % 2:
        print("  Y")
    else:
        print("  O")


def print_top_row(time):
    row = ""
    for five_mult in range(5, 24, 5):
        if time.hour >= five_mult:
            row += "R"
        else:
            row += "O"
    print(row)


def print_second_row(time):
    num_on = time.hour % 5
    print("R" * num_on + "O" * (4 - num_on))


def print_third_row(time):
    row = ""
    for five_mult in range(5, 60, 5):
        if time.minute >= five_mult:
            if five_mult % 15 == 0:
                row += "R"
            else:
                row += "Y"
        else:
            row += "O"
    print(row)


def print_last_row(time):
    num_on = time.minute % 5
    print("Y" * num_on + "O" * (4 - num_on))


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
    print_top_circle(time)
    print_top_row(time)
    print_second_row(time)
    print_third_row(time)
    print_last_row(time)
    print("")


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
