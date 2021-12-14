from unittest.mock import patch, Mock, call

import requests

from ssd_library_TUI.libraryClient import App
import pytest


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_pre_login_menu_printed(mocked_print: Mock, mocked_input: Mock):
    app = App().run()

    mocked_print.assert_any_call("* Login menu' of the library *\n")
    mocked_print.assert_any_call("1. Login")
    mocked_print.assert_any_call("2. Register")
    mocked_print.assert_any_call("3. Login as Guest")
    mocked_print.assert_any_call("0. Exit")


@patch('builtins.input', side_effect=['3', '0', '0'])
@patch('builtins.print')
def test_main_menu_printed(mocked_print: Mock, mocked_input: Mock):
    app = App().run()

    mocked_print.assert_any_call("* Main menu of the library *\n")
    mocked_print.assert_any_call("1. Show all books")
    mocked_print.assert_any_call("2. Show my books")
    mocked_print.assert_any_call("3. Rent a book")
    mocked_print.assert_any_call("4. Show book")
    mocked_print.assert_any_call("0. Logout")


@patch('builtins.print')
@patch('builtins.input', side_effect=['3', '1', '0', '0'])
@patch('requests.get')
def test_guest_login_show_all_books(mocked_get: Mock, mocked_input: Mock, mocked_print: Mock):
    class MockedResponse:
        status_code = 200

        def json(self):
            return [{'ISBN': '1', 'author': 'a', 'title': 'b', 'preview': 'c', 'published_date': '21', 'num_pages': '2'}]

    mocked_get.return_value = MockedResponse()
    app = App().run()

    fmt = '%-16s  %-35s  %-45s  %-80s  %-12s  %-3s'
    book = MockedResponse().json()[0]
    response = fmt % (book['ISBN'], book['author'], book['title'], book['preview'], book['published_date'],
                      book['num_pages'])

    mocked_print.assert_any_call(response)


@patch('builtins.print')
@patch('builtins.input', side_effect=['3', '2', '0', '0'])
def test_anon_user_cant_access_my_books(mocked_input: Mock, mocked_print: Mock):
    App().run()

    mocked_print.assert_any_call("Login into your account first!")


@patch('builtins.print')
@patch('builtins.input', side_effect=['3', '3', '0', '0'])
def test_anon_user_cant_rent_book(mocked_input: Mock, mocked_print: Mock):
    App().run()

    mocked_print.assert_any_call("Login into your account first!")


@patch('builtins.print')
@patch('builtins.input', side_effect=['3', '4', '0', '0'])
def test_anon_user_cant_access_rented_book(mocked_input: Mock, mocked_print: Mock):
    App().run()

    mocked_print.assert_any_call("Login into your account first!")


@patch('requests.post')
@patch('builtins.print')
@patch('builtins.input', side_effect=['1', 'prova', 'prova'])
def test_global_exception_handler(mock_input: Mock, mock_print: Mock, mock_post: Mock):
    mock_post.side_effect = requests.exceptions.RequestException()
    App().run()

    mock_print.assert_any_call("FATAL ERROR!")


@patch('requests.post')
@patch('builtins.print')
@patch('builtins.input', side_effect=['1', '      ', ' ', 'prova', ' ', 'prova', '0', '0'])
def test_wrong_value_input(mock_input: Mock, mock_print: Mock, mock_post: Mock):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json = lambda: {'key': 'a'}
    App().run()

    mock_print.assert_any_call("Login successful!\n")


@patch('requests.post')
@patch('builtins.print')
@patch('builtins.input', side_effect=['2', ' ', 'prova', ' ', 'prova', 'prova', 'prova@gmail.com', '0', '0'])
def test_registration(mock_input: Mock, mock_print: Mock, mock_post: Mock):
    mock_post.return_value.status_code = 201
    App().run()

    mock_print.assert_any_call("Registration successful!\n")


@patch('requests.post')
@patch('builtins.print')
@patch('builtins.input', side_effect=['2', ' ', 'prova', ' ', 'prova', 'prova', 'prova@gmail.com', '0', '0'])
def test_registration_fail(mock_input: Mock, mock_print: Mock, mock_post: Mock):
    mock_post.return_value.status_code = 403
    App().run()

    assert call("Registration successful!\n") not in mock_print.mock_calls


@patch('requests.get')
@patch('requests.post')
@patch('builtins.print')
@patch('builtins.input', side_effect=['1', 'try', 'try', '3', 'aaaaaa--aa', '978-134-A3-98', '978-134-23-98', '0', '0'])
def test_read_isbn(mock_input: Mock, mock_print: Mock, mock_post: Mock, mock_get: Mock):
    mock_post.return_value.status_code = 200
    mock_get.return_value.status_code = 200
    mock_post.return_value.json = lambda: {'key': 'a'}
    App().run()

    mock_print.assert_any_call("Invalid ISBN, retry!")
    mock_print.assert_any_call("Rented successfully!\n")
