from unittest.mock import Mock, patch, call

import pytest
from valid8 import ValidationError

from ssd_library_TUI.menu.menu import Description, Key, Command, Menu


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


@patch('builtins.print')
def test_command_print_description(mocked_print: Mock):
    cmd = Command.create_command(1, 'Stampa ciao', lambda: print("ciao"))
    cmd.action()
    assert mocked_print.mock_calls == [call('ciao')]


def test_menu_not_duplicate_action():
    cmd = Command.create_command(1, 'Stampa ciao', lambda: print("ciao"))
    menu = Menu.Builder("prova").with_command(cmd)

    with pytest.raises(ValidationError):
        menu.with_command(cmd)


def test_menu_has_exit_command():
    cmd = Command.create_command(1, 'Stampa ciao', lambda: print("ciao"))
    menu = Menu.Builder("prova").with_command(cmd)

    with pytest.raises(ValidationError):
        menu.build()


@patch('builtins.input', side_effect=['1', '2', '3'])
@patch('builtins.print')
def test_menu_calls_command_correctly(mocked_print: Mock, mocked_input):
    menu = Menu.Builder("prova").\
        with_command(Command.create_command(1, "prova", lambda: print("1"))). \
        with_command(Command.create_command(2, "prova2", lambda: print("2"))). \
        with_command(Command.create_command(3, "prova3", lambda: print("3"), is_exit=True)).build()

    menu.run()
    mocked_print.assert_any_call('1')
    mocked_print.assert_any_call('2')
    mocked_print.assert_any_call('3')


@patch('builtins.input', side_effect=['-1', 'prova', '47492', '1', '0'])
@patch('builtins.print')
def test_menu_handles_wrong_values(mocked_print: Mock, mocked_input: Mock):
    menu = Menu.Builder("prova"). \
        with_command(Command.create_command(1, "prova", lambda: print("Hello"))).\
        with_command(Command.create_command(0, "Exit", is_exit=True)).build()

    menu.run()
    mocked_print.assert_any_call('Invalid command, retry!')
    mocked_print.assert_any_call("Hello")












