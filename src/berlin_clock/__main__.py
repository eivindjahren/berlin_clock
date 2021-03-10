import argparse
import sched
import sys
import time
from datetime import datetime

import berlin_clock.berlin_clock as bc
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


def print_berlin_clock(berlin_clock: bc.BerlinClock):
    """
    Prints a representation of the given berlin clock to the terminal
    using the following characters to represent lamps:

    Y = Yellow
    R = Red
    O = Off


    :param berlin_clock: The berlin clock object for the time to be displayed.
    """

    def light_char(light):
        if not light.on:
            return "O"
        if light.color == bc.Color.YELLOW:
            return "Y"
        if light.color == bc.Color.RED:
            return "R"
        raise ValueError("Unexpected light format")

    print(light_char(berlin_clock.top_light))
    for row in [
        berlin_clock.first_row,
        berlin_clock.second_row,
        berlin_clock.third_row,
        berlin_clock.last_row,
    ]:
        print("".join([light_char(l) for l in row]))


def run_berlin_clock(args):
    """
    Runs print_berlin_clock every second.

    :param args: argparse namespace of the command line arguments.
    """
    berlin_clock = bc.BerlinClock()
    scheduler = sched.scheduler(time.time, time.sleep)

    def event_loop():
        berlin_clock.set_time(datetime.now())
        print_berlin_clock(berlin_clock)
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
