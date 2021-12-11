from typing import Optional

import requests
import typeguard
import json

from ssd_library_TUI.menu.menu import Menu, Command

api = "http://localhost:8000/api/v1"


@typeguard.typechecked
class App:
    __login_menu: Menu
    __library_menu: Menu

    __access_token: str = ""

    def __init__(self):
        self.__login_menu = Menu.Builder("Login menu' for the library") \
            .with_command(Command.create_command(1, "Login", lambda: self.do_login())) \
            .with_command(Command.create_command(2, "Register", lambda: self.do_registration())) \
            .with_command(Command.create_command(0, "Exit", lambda: print("BYE!"), is_exit=True)) \
            .build()

        self.__library_menu = Menu.Builder("Main menu' of the library") \
            .with_command(Command.create_command(1, "Show all books", lambda: self.fetch_books())) \
            .with_command(Command.create_command(0, "Exit", lambda: print("BYE!"), is_exit=True)) \
            .build()

    def do_login(self):
        username = input("Username: ")
        password = input("Password: ")

        res = requests.post(url=f'{api}/auth/login/', data={'username': {username}, 'password': {password}})
        if res.status_code != 200:
            print(res.content)

        json = res.json()
        self.__acces_token = json['key']
        print("Login successful")
        self.__library_menu.run()

    @staticmethod
    def do_registration():
        username = input("Username: ")
        password = input("Password: ")
        email = input("Email: ")

        res = requests.post(url=f'{api}/auth/registration/', data={"username": {username}, "password1": {password},
                                                                   "password2": {password}, "email": {email}})

        if res.status_code != 201:
            return res.content

        return "Registration successful"

    def fetch_books(self):
        res = requests.get(url=f'{api}/', headers={'Authorization': f'Token {self.__acces_token}'})
        if res.status_code != 200:
            return None

        self.__print_books(res.json())

    def __print_books(self, all_books):
        print("-" * 160)
        fmt = '%-13s  %-15s  %15s  %-80s  %-12s  %-3s'
        print(fmt % ("ISBN", "AUTHOR", "TITLE", "PREVIEW", "PUB DATE", "#PAGES"))
        print("-" * 160)
        for book in all_books:
            print(fmt % (book['ISBN'], book['author'], book['title'], book['preview'], book['published_date'],
                         book['num_pages']))

    @staticmethod
    def welcome():
        print("-------- Welcome to our library --------")

    def run(self):
        self.__login_menu.run()


def main():
    App().run()


if __name__ == "__main__":
    main()
