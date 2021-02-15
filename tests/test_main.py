import pytest
from berlin_clock.__main__ import parse_args_and_run


def test_help_message(capsys):
    with pytest.raises(SystemExit) as system_exit:
        parse_args_and_run(["berlin_clock", "-h"])
        assert system_exit.code == 0
    assert "berlin_clock" in capsys.readouterr().out
