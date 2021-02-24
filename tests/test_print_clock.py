from datetime import time

import pytest

import berlin_clock.__main__ as bclock


@pytest.mark.parametrize(
    "time, expected",
    [
        (time(12, 30), "RROO\n"),
        (time(10, 15), "RROO\n"),
        (time(15, 15), "RRRO\n"),
    ],
)
def test_print_top_row(capsys, time, expected):
    bclock.print_top_row(time)
    captured = capsys.readouterr()

    assert captured.out == expected


@pytest.mark.parametrize(
    "time, expected",
    [
        (time(12, 30, 0), "  O\n"),
        (time(12, 30, 1), "  Y\n"),
        (time(10, 15, 2), "  O\n"),
    ],
)
def test_print_top_circle(capsys, time, expected):
    bclock.print_top_circle(time)
    captured = capsys.readouterr()

    assert captured.out == expected


@pytest.mark.parametrize(
    "time, expected",
    [
        (time(12, 30), "RROO\n"),
        (time(13, 30), "RRRO\n"),
        (time(8, 15, 2), "RRRO\n"),
        (time(6, 15, 2), "ROOO\n"),
    ],
)
def test_print_second_row(capsys, time, expected):
    bclock.print_second_row(time)
    captured = capsys.readouterr()

    assert captured.out == expected


@pytest.mark.parametrize(
    "time, expected",
    [
        (time(12, 30), "YYRYYROOOOO\n"),
        (time(8, 15), "YYROOOOOOOO\n"),
        (time(8, 10, 2), "YYOOOOOOOOO\n"),
    ],
)
def test_print_third_row(capsys, time, expected):
    bclock.print_third_row(time)
    captured = capsys.readouterr()

    assert captured.out == expected


@pytest.mark.parametrize(
    "time, expected",
    [
        (time(12, 30), "OOOO\n"),
        (time(13, 31), "YOOO\n"),
        (time(8, 18), "YYYO\n"),
        (time(8, 4), "YYYY\n"),
    ],
)
def test_print_last_row(capsys, time, expected):
    bclock.print_last_row(time)
    captured = capsys.readouterr()

    assert captured.out == expected


def test_print_clock_example(capsys):
    bclock.print_berlin_clock(time(13, 17, 2))
    captured = capsys.readouterr()
    assert captured.out == "  O\n" "RROO\n" "RRRO\n" "YYROOOOOOOO\n" "YYOO\n" "\n"
