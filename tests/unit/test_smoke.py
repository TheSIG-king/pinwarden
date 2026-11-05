"""Smoke tests: the package imports and the CLI answers ``--version``."""

import pytest

import pinwarden
from pinwarden.cli import main


def test_version_is_exposed() -> None:
    assert isinstance(pinwarden.__version__, str)
    assert pinwarden.__version__


def test_cli_version_exits_cleanly(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert pinwarden.__version__ in capsys.readouterr().out


def test_cli_without_args_prints_help(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 0
    assert "usage:" in capsys.readouterr().out
