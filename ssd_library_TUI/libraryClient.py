from typing import Optional

import requests
import typeguard
import json

from valid8 import ValidationError

from ssd_library_TUI.menu.menu import Menu, Command
from ssd_library_TUI.misc.models import ISBN
from ssd_library_TUI.misc.regex import matches_pattern


@typeguard.typechecked
class App:
    __login_menu: Menu
    __library_menu: Menu

    api = "http://localhost:8000/api/v1"

    __access_token: str = ""

    def __init__(self):
        self.__login_menu = Menu.Builder("Login menu' of the library") \
            .with_command(Command.create_command(1, "Login", lambda: self.__do_login())) \
            .with_command(Command.create_command(2, "Register", lambda: self.__do_registration())) \
            .with_command(Command.create_command(3, "Login as Guest", lambda: self.__login_guest())) \
            .with_command(Command.create_command(0, "Exit", lambda: print("BYE!"), is_exit=True)) \
            .build()

        self.__library_menu = Menu.Builder("Main menu of the library") \
            .with_command(Command.create_command(1, "Show all books", lambda: self.fetch_books())) \
            .with_command(Command.create_command(2, "Show my books", lambda: self.fetch_my_books())) \
            .with_command(Command.create_command(3, "Rent a book", lambda: self.rent_book())) \
            .with_command(Command.create_command(4, "Show book", lambda: self.show_book())) \
            .with_command(Command.create_command(0, "Logout", lambda: self.__do_logout(), is_exit=True)) \
            .build()

    def __login_guest(self):
        print()
        self.__library_menu.run()

    @staticmethod
    def __input_parameter(param):
        is_valid = False
        val: str = " "
        while not is_valid:
            val = input(f"{param}: ")
            if len(val.strip()) == 0:
                continue

            is_valid = True

        return val

    def __do_logout(self):
        if self.__access_token == "":
            print()
            return

        res = requests.post(url=f'{self.api}/auth/logout/', headers={'Authentication': f'Token {self.__access_token}'})
        if res.status_code != 200:
            print("Error during logout!")
            return

        print("Logout successful!\n")
        self.__access_token = ""

    def __do_login(self):
        username = self.__input_parameter("Username")
        password = self.__input_parameter("Password")

        res = requests.post(url=f'{self.api}/auth/login/', data={'username': {username}, 'password': {password}})
        if res.status_code != 200:
            print("Cannot login!")
            return

        res_json = res.json()
        self.__access_token = res_json['key']
        print("Login successful!\n")
        self.__library_menu.run()

    def __do_registration(self):
        username = App.__input_parameter("Username")
        password = App.__input_parameter("Password")
        email = App.__input_parameter("Email")

        res = requests.post(url=f'{App.api}/auth/registration/', data={"username": {username}, "password1": {password},
                                                                       "password2": {password}, "email": {email}})

        if res.status_code != 201:
            print("Cannot register!")
            return

        print("Registration successful!\n")

    def fetch_books(self):
        res = requests.get(url=f'{self.api}/')
        if res.status_code != 200:
            print("Cannot fetch books!")
            return None

        self.__print_books(res.json())

    def fetch_my_books(self):
        if self.__access_token == "":
            print("Login into your account first!\n")
            return

        res = requests.get(url=f'{self.api}/my-books/', headers={'Authorization': f'Token {self.__access_token}'})
        if res.status_code != 200:
            print("cannot fetch books!")
            return None

        self.__print_books(res.json(), is_preview=False)

    def __print_books(self, all_books, is_preview: bool = True):
        print()
        arg = 'preview'
        if not is_preview:
            arg = 'text'

        print("-" * 205)
        fmt = '%-20s  %-35s  %-45s  %-80s  %-12s  %-3s'
        print(fmt % ("ISBN", "AUTHOR", "TITLE", arg.upper(), "PUB DATE", "#PAGES"))
        print("-" * 205)
        for book in all_books:
            book[arg] = str(book[arg]).replace('\n', ' ')
            print(fmt % (book['ISBN'], book['author'], book['title'], book[arg][0:min(len(book[arg]), 80)],
                         book['published_date'], book['num_pages']))

        print()

    def __read_isbn(self):
        is_valid = False
        isbn_str: str = ""
        while not is_valid:
            try:
                isbn_str = input("ISBN: ").strip()
                isbn = ISBN(isbn_str)
                is_valid = True
                return isbn_str
            except (TypeError, ValueError, ValidationError) as e:
                print(e)
                print("Invalid ISBN, retry!")

    def rent_book(self):
        if self.__access_token == "":
            print("Login into your account first!\n")
            return

        isbn_str: str = self.__read_isbn()

        res = requests.get(f'{self.api}/rent/{isbn_str}/', headers={'Authorization': f'Token {self.__access_token}'})

        if res.status_code != 200:
            print("Cannot rent book!")
            return

        print("Rented successfully!\n")

    def show_book(self):
        if self.__access_token == "":
            print("Login into your account first!\n")
            return

        isbn_str: str = self.__read_isbn()

        res = requests.get(f'{self.api}/my-books/{isbn_str}/', headers={'Authorization': f'Token {self.__access_token}'})

        if res.status_code == 403:
            print("You don't own this book!")
            return

        if res.status_code != 200:
            print("Cannot fetch book!")
            return

        self.__print_book(res.json())

    @staticmethod
    def __format_str(string):
        string = string.replace('\n', ' ')
        for i in range(0, len(string)):
            if i > 0 and i % 150 == 0:
                string = string[:i] + '\n' + ' ' * 8 + string[i:]

        return string

    @staticmethod
    def __print_book(book):
        print("\n* BOOK DETAIL *")
        print(f"ISBN: {book['ISBN']}")
        print(f"AUTHOR: {book['author']}")
        print(f"TITLE: {book['title']}")
        print(f"TEXT: {App.__format_str(book['text'])}")
        print(f"PUB DATE: {book['published_date']}")
        print(f"# PAGES: {book['num_pages']}")
        print()

    def run(self):
        try:
            self.__login_menu.run()
        except Exception as e:
            print("FATAL ERROR!")


def main(name: str):
    if name == "__main__":
        App().run()


main(__name__)

