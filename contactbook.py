from seed import *
import datetime
from datetime import date
import re
import phonenumbers
from abc import ABC, abstractmethod


class Field(ABC):
    def __init__(self, value: str) -> None:
        self.__value = None
        self.value = value

    def __repr__(self) -> str:
        return f'{self.value}'

    def __str__(self) -> str:
        return f'{self.value}'


    @abstractmethod
    def value(self):
        ...


class Name(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value.title()


class LastName(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value.title()


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            value.isdigit()
        except Exception:
            print("Value Error, phone should contain numbers")
            raise ValueError


class Birthday(Field):
    def __str__(self):
        if self.value is None:
            return 'N/A'
        else:
            return f'{self.value:%d %b %Y}'

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if value is None:
            self.__value = None
        else:
            try:
                self.__value = datetime.datetime.strptime(value, '%d.%m.%Y').date()
            except ValueError:
                print("Enter the date of birth in the format dd.mm.yyyy")


class Email(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        result = None
        get_email = re.findall(r'\b[a-zA-Z]\w+@[a-zA-Z]+\.[a-zA-Z]{2,}', value)
        for i in get_email:
            result = i
        if result is None:
            raise AttributeError(f" Incorrect email {value}")
        self.__value = result


class Record:
    def __init__(self, name: Name, last_name=None, phones=None, birthday=None, email=None, address=None) -> None:
        if phones is None:
            phones = []
        self.name = name
        self.last_name = last_name
        self.phone_list = phones
        self.birthday = birthday
        self.address = address
        self.email = email

    def __str__(self) -> str:
        return f' Contact:  {self.name.value.title()} {self.last_name.value}\n' \
               f' Phones:   {", ".join([phone.value for phone in self.phone_list])}\n' \
               f' Birthday: {self.birthday}\n' \
               f' Email:    {self.email}\n'

    def add_number(self, phone: Phone) -> None:
        self.phone_list.append(phone)

    def remove_number(self, phone: Phone) -> None:
        self.phone_list.remove(phone)

    def edit_number(self, phone: Phone, new_phone: Phone) -> None:
        self.phone_list.remove(phone)
        self.phone_list.append(new_phone)

    @staticmethod
    def days_to_birthday(self, birthday: Birthday):
        if birthday.value is None:
            return None
        this_day = date.today()
        birthday_day = date(this_day.year, birthday.value.month, birthday.value.day)
        if birthday_day < this_day:
            birthday_day = date(this_day.year + 1, birthday.value.month, birthday.value.day)
        return (birthday_day - this_day).days


class InputError:
    def __init__(self, func) -> None:
        self.func = func

    def __call__(self, *args):
        try:
            return self.func(*args)
        except IndexError:
            return 'Unknown command'
        except KeyError:
            return 'User with this phone number does not exist'
        except ValueError:
            return 'Incorrect input'
        except AttributeError:
            return "Birthday should be in the format dd.mm.yyyy"


def greeting(*args):
    return 'Hello! How can I help you?'


def end():
    return 'Good bye!'


@InputError
def add_contact(*args):
    name = Name(args[0])
    if len(args) == 3:
        last_name = LastName(args[1])
        phone = Phone(args[2])
    create_contact(name.value, last_name.value, phone.value)
    return f'Add user {name.value.title()} {last_name.value.title()} with phone number {phone}'


@InputError
def change_contact(*args):
    name, last_name, new_phone = args[0], args[1], args[2]
    change_number(name, last_name, new_phone)
    return f'Change phone number {new_phone} to user {name} {last_name}'


@InputError
def show_phone(*args):
    name = args[0]
    last_name = args[1]
    phones = show_number(name, last_name)
    if phones:
        return f'Contact {name} {last_name} have phone {phones}'
    else:
        return f'Contact {name} {last_name} not found!'


@InputError
def remove_number(*args):
    name, last_name = args[0], args[1]
    delete_number(name, last_name)
    return f'Delete phone from user {name} {last_name}'


@InputError
def show_all(*args):
    all_users = show_all()
    if all_users > 0:
        return f'Contactbook has {all_users} contacts'
    else:
        return f'No data'


@InputError
def add_email(*args):
    name, last_name, email = args[0], args[1], args[2]
    update_email(name, last_name, email)
    return f'email {email} addd - {name} {last_name}'


@InputError
def add_last_name(*args):
    name, last_name = args[0], args[1]
    update_last_name(name, last_name)
    return f'last name {last_name} added - {name}'


@InputError
def add_birthday(*args):
    name, last_name, birthday = args[0], args[1], args[2]
    update_birthday(name, last_name, birthday)
    return f'{birthday} added - {name} {last_name}'


@InputError
def user_birthday(*args):
    name = args[0]
    last_name = args[1]
    birthday = show_birthday(name, last_name)
    if not birthday:
        return 'N/A'
    else:
        return f'Birthday {name} {last_name} in: {birthday}'


@InputError
def remove_contact(*args):
    name = args[0]
    last_name = args[1]
    yes_no = input(f'Are you sure you want to delete the user {name}? (y/n) ')
    if yes_no == 'y':
        remove_contact(name, last_name)
        return f'Delete user {name} {last_name}'

    else:
        return 'User not deleted'


@InputError
def delete_all():
    yes_no = input('Are you sure you want to delete all users? (y/n) ')
    if yes_no == 'y':
        delete_all()
        return 'Address book is empty'
    else:
        return 'Removal canceled'


@InputError
def find(*args):
    sub = ' '.join(args)
    data = find(sub)
    return data


def info():
    return """
    Choose the command
    "help", "?"                       >>> Commands list
    "close", "exit", "."              >>> Exit from AddressBook
    "add" name phone                  >>> Add user to AddressBook
    "change" name old_phone new_phone >>> Change the user's phone number
    "add birthday" name birthday          >>> Add/edit user birthday
    "email" name email                >>> Add/edit user email
    "last name" name last name        >>> Add/edit user last name
    "remove" name phone               >>> Delete phone number
    "delete" name                     >>> Delete user
    "clear"                           >>> Delete all users
    "show" name                       >>> Show user info
    "show all"                        >>> Show all users info
    "birthday" name                   >>> Show how many days to user birthday
    "find" data                        >>> Find any data 
    """


def unknown_command(*args):
    return 'Unknown command'


COMMANDS = {greeting: ['hello'],
            add_contact: ['add '],
            change_contact: ['change '],
            info: ['help', '?'],
            show_all: ['show all'],
            end: ['good bye', 'close', 'exit', '.'],
            delete_number: ['remove'],
            add_birthday: ['add birthday'],
            user_birthday: ['birthday '],
            show_number: ['show '],
            remove_contact: ['remove'],
            delete_all: ['clear'],
            add_email: ['email '],
            add_last_name: ['last name'],
            find: ['find']}


def command_parser(user_command: str) -> (str, list):
    for key, list_value in COMMANDS.items():
        for value in list_value:
            if user_command.lower().startswith(value):
                args = user_command[len(value):].split()
                return key, args
    else:
        return unknown_command, []


def main():
    print(info())
    while True:
        user_command = input('Enter command please >>> ')
        if user_command == 'exit':
            return f'Exit'
        command, data = command_parser(user_command)
        print(command(*data))
        if command is end:
            break
