"""CLI entry-point contracts without changing frozen slug algorithms."""
import importlib
import sys
from unittest.mock import patch
import pytest

cli = importlib.import_module('slugify.__main__')

def test_main_uses_process_arguments_when_omitted(capsys):
    with patch.object(sys, 'argv', ['slugify', 'Hello', 'World']):
        cli.main()
    assert capsys.readouterr().out == 'hello-world\n'

def test_keyboard_interrupt_exits_without_traceback(capsys):
    with patch.object(cli, 'slugify', side_effect=KeyboardInterrupt):
        with pytest.raises(SystemExit) as error:
            cli.main(['slugify', 'hello'])
    assert error.value.code == -1
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''
