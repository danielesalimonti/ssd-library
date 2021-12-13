from unittest.mock import Mock

import pytest
from valid8 import ValidationError

from ssd_library_TUI.menu.menu import Description, Key, Command


def test_menu_description_is_str():
    Description('prova')
    with pytest.raises(TypeError):
        Description(2)
        Description(None)
        Description(['ciao', 'mondo'])


def test_menu_description_valid():
    good_values = ['prova', 'Hello World', 'Description! ', 'Type 20 commands.']

    for value in good_values:
        Description(value)


def test_menu_description_invalid():
    wrong_values = ['', 'a'*101, '\n', '\t', '$', '*', 'Description&']

    for value in wrong_values:
        with pytest.raises(ValidationError):
            Description(value)


def test_menu_key_is_int():
    Key(1)
    with pytest.raises(TypeError):
        Key('a')
        Key(None)
        Key([1, 2])


def test_command_call_its_action():
    mocked_action = Mock()
    cmd = Command.create_command(1, 'prova', lambda: mocked_action())
    cmd.action()
    mocked_action.assert_called_once()






