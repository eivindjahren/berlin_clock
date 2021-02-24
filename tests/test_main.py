import pytest
from berlin_clock.__main__ import (
    parse_args_and_run,
    parse_time,
    convert_to_blocks,
    generate_string,
    generate_row_clock_strings,
    generate_special_string,
)


def test_help_message(capsys):
    with pytest.raises(SystemExit) as system_exit:
        parse_args_and_run(["berlin_clock", "-h"])
        assert system_exit.code == 0
    assert "berlin_clock" in capsys.readouterr().out


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("00:00:00", [0, 0, 0]),
        ("01:00:00", [1, 0, 0]),
        ("01:02:03", [1, 2, 3]),
        ("11:12:13", [11, 12, 13]),
    ],
)
def test_parse_time(test_input, expected):
    assert parse_time(test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("00:00:00", [0, 0, 0, 0]),
        ("01:00:00", [0, 1, 0, 0]),
        ("06:00:00", [1, 1, 0, 0]),
        ("06:05:00", [1, 1, 1, 0]),
        ("06:17:00", [1, 1, 3, 2]),
        ("13:17:00", [2, 3, 3, 2]),
    ],
)
def test_convert_to_blocks(test_input, expected):
    assert convert_to_blocks(test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (1, "YOOO"),
        (2, "YYOO"),
        (3, "YYYO"),
        (4, "YYYY"),
    ],
)
def test_generate_string(test_input, expected):
    assert generate_string(test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (1, "ROOO"),
        (2, "RROO"),
        (3, "RRRO"),
        (4, "RRRR"),
    ],
)
def test_generate_string(test_input, expected):
    assert generate_string(test_input, color="R") == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (1, "YOOOOOOOOOO"),
        (3, "YYROOOOOOOO"),
        (4, "YYRYOOOOOOO"),
        (11, "YYRYYRYYRYY"),
    ],
)
def test_generate_special_row(test_input, expected):
    assert generate_special_string(test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("00:00:00", ["Y", "OOOO", "OOOO", "OOOOOOOOOOO", "OOOO"]),
        ("01:00:00", ["Y", "OOOO", "YOOO", "OOOOOOOOOOO", "OOOO"]),
        ("06:00:00", ["Y", "YOOO", "YOOO", "OOOOOOOOOOO", "OOOO"]),
        ("06:05:00", ["Y", "YOOO", "YOOO", "YOOOOOOOOOO", "OOOO"]),
        ("06:17:01", ["O", "YOOO", "YOOO", "YYROOOOOOOO", "RROO"]),
        ("13:17:02", ["Y", "YYOO", "YYYO", "YYROOOOOOOO", "RROO"]),
        ("13:38:03", ["O", "YYOO", "YYYO", "YYRYYRYOOOO", "RRRO"]),
    ],
)
def test_row_clock(test_input, expected):
    assert generate_row_clock_strings(test_input) == expected
