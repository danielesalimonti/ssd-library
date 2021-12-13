from dataclasses import dataclass, field, InitVar
from typing import Callable, List, Dict, Any, Optional

from typeguard import typechecked
from valid8 import validate

from ssd_library_TUI.misc.dataclass import validate_dataclass
from ssd_library_TUI.misc.regex import matches_pattern


#La descrizione del comando
@dataclass(frozen=True)
@typechecked
class Description:
    desc: str

    __regex = r'[a-zA-Z0-9!, \.\']*'

    def __post_init__(self):
        validate_dataclass(self)
        validate('Pattern', value=self.desc, min_len=1, max_len=100, custom=matches_pattern(self.__regex))

    def __str__(self):
        return self.desc


#Il tasto che scatena l'evento
@dataclass(frozen=True)
@typechecked
class Key:
    value: int

    def __post_init__(self):
        validate_dataclass(self)

    def __str__(self):
        return str(self.value)


#Il comando intero, con descrizione, pulsante e azione
@dataclass(frozen=True)
@typechecked
class Command:
    key: Key
    description: Description
    action: Callable[[], None] = field(default=lambda: None)
    is_exit: bool = field(default=False)

    def __post_init__(self):
        validate_dataclass(self)

    @staticmethod
    def create_command(key: int, description: str, action: Callable[[], None] = lambda: None,
                       is_exit: bool = False) -> 'Command':
        return Command(Key(key), Description(description), action, is_exit)


#Il menu completo
@dataclass(frozen=True)
@typechecked
class Menu:
    description: Description
    __commands: List[Command] = field(default_factory=list, init=False)
    __keyToCommand: Dict[Key, Command] = field(default_factory=dict, init=False)

    create_key: InitVar[Any] = field(default=None)

    def __post_init__(self, create_key: Any):
        validate_dataclass(self)
        validate('valid key', value=create_key, custom=Menu.Builder.check_key)

    def add_command(self, command: Command, create_key: Any):
        validate('valid key', value=create_key, custom=Menu.Builder.check_key)
        validate('key non present', value=command.key, custom=lambda key: key not in self.__keyToCommand)
        self.__commands.append(command)
        self.__keyToCommand[command.key] = command

    def has_exit(self):
        return len(list(filter(lambda command: command.is_exit, self.__commands))) > 0

    def print_menu(self):
        desc = f'* {self.description} *'
        print(f'{desc}\n')

        for command in self.__commands:
            print(f'{command.key}. {command.description}')

    def read_from_input(self):
        while True:
            try:
                choice = input("Choice: ")
                key = Key(int(choice.strip()))
                command = self.__keyToCommand[key]
                command.action()
                return command.is_exit
            except (KeyError, ValueError, TypeError) as e:
                print("Invalid command, retry!")

    def run(self):
        while True:
            self.print_menu()
            if self.read_from_input():
                return

    @typechecked
    @dataclass
    class Builder:
        __menu: Optional['Menu']
        __create_key = object()

        def __init__(self, description: str):
            self.__menu = Menu(Description(description), self.__create_key)

        @staticmethod
        def check_key(create_key: Any):
            return create_key == Menu.Builder.__create_key

        def with_command(self, command: Command) -> 'Menu.Builder':
            validate('menu not null', value=self.__menu)
            self.__menu.add_command(command, self.__create_key)
            return self

        def build(self) -> 'Menu':
            validate('menu not null', value=self.__menu)
            validate('menu has exit', value=self.__menu.has_exit(), equals=True)
            return self.__menu


