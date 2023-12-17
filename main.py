from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):  
        return str(self.value)
    
class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
            super().__init__(value)
        except ValueError:
            raise ValueError("Wrong date format")

class Name(Field):
    required = True
    def __init__(self, value):
        if len(value) < 3:
            raise ValueError("Name length should be at least 3 symbols")
        super().__init__(value)

class Phone(Field):
   def __init__(self, value):
       if len(value) != 10:
            raise ValueError("Phone length should be exactly 10 symbols")
       super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        if new_phone in self.phones:
            raise ValueError("Phone number already exists in this contact")
        self.phones.append(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def find_phone_index(self, phone):
        for index, p in enumerate(self.phones):
            if p.value == phone:
                return index
        return -1
    
    def edit_phone(self, old_phone, new_phone):
        index = self.find_phone_index(old_phone)
        if index == -1:
            raise ValueError(f"Phone number {old_phone} not found in this contact")
        self.phones[index] = Phone(new_phone)
    
    def remove_phone(self, phone):
        index = self.find_phone_index(phone)
        if index == -1:
            raise ValueError(f"Phone number {phone} not found in this contact")
        del self.phones[index]

    def __str__(self):
        phones_str = '; '.join(str(p) for p in self.phones)
        birthday_str = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, Phones: {phones_str}{birthday_str}"

    def get_name(self):
        return self.name.value


class AddressBook(UserDict):
    WEEK_DAYS_BY_NUMBERS = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }
    
    def add_record(self, record):
        if not isinstance(record, Record):
            raise TypeError("Argument must be an instance of Record class")
        self.data[record.get_name()] = record
    
    def find(self, name):
        return self.data.get(name, None)
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self):
        today = datetime.today().date()
        next_week_birthdays_by_weekday = {day: [] for day in self.WEEK_DAYS_BY_NUMBERS.values()}

        for name, record in self.data.items():
            if record.birthday:
                birthday = datetime.strptime(record.birthday.value, '%d.%m.%Y').date()
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days

                if delta_days < 7:
                    birthday_week_day = birthday_this_year.weekday()
                    weekday_name = self.WEEK_DAYS_BY_NUMBERS[birthday_week_day]
                    next_week_birthdays_by_weekday[weekday_name].append(name)

        return next_week_birthdays_by_weekday


MENU = """
MENU:
# hello : show hello message
# add [name] [phone] [birthday(optional)]: add new Contact
# change [name] [phone]: change Contact number
# phone [name]: show contact phone
# all: show all contacts
# add-birthday [name] [birthday]: add birthday to contact
# show-birthday [name]: show birthday of contact
# birthdays: show upcoming birthdays
# menu: show menu
# exit|close: exit from program
"""

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Error: {e}"
    return wrapper

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

@input_error
def add_contact(args, book):
    if len(args) not in [2, 3]:
        raise ValueError("Add command expects 2 or 3 arguments: name, phone, and optionally birthday.")
    name, phone = args[:2]
    record = Record(name)
    record.add_phone(phone)

    if len(args) == 3:
        birthday = args[2]
        record.add_birthday(birthday)
    
    book.add_record(record)
    return "Contact added."

@input_error
def change_contact(args, book):
    if len(args) != 2:
        raise ValueError("Change command expects 2 arguments: name and phone.")
    name, new_phone = args
    record = book.find(name)
    if not record:
        raise ValueError("Contact not found.")
    record.edit_phone(record.phones[0].value, new_phone)
    return "Contact updated."

@input_error
def show_phone(args, book):
    if len(args) != 1:
        raise ValueError("Phone command expects 1 argument: name.")
    name, = args
    record = book.find(name)
    if record:
        return ', '.join(phone.value for phone in record.phones)
    else:
        return "Contact not found."

@input_error
def show_all(book):
    all_records = ""
    if len(book) == 0:
        return "There are no contacts in the list."
    for name, record in book.items():
        all_records += f"{record}\n"
    return all_records

@input_error
def add_birthday(args, book):
    if len(args) != 2:
        raise ValueError("Add-birthday command expects 2 arguments: name and birthday.")
    name, birthday = args
    record = book.find(name)
    if not record:
        raise ValueError("Contact not found.")
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book):
    if len(args) != 1:
        raise ValueError("Show-birthday command expects 1 argument: name.")
    name, = args
    record = book.find(name)
    if record and record.birthday:
        return record.birthday.value
    else:
        return "Birthday not found or contact not found."

@input_error
def birthdays(book):
    birthdays = book.get_birthdays_per_week()
    result = ""
    for day, names in birthdays.items():
        if names:
            result += f"{day}: {', '.join(names)}\n"
    return result if result else "No birthdays in the next week."


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    print(MENU)

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "menu":
            print(MENU)

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))
        
        elif command == 'add-birthday':
            print(add_birthday(args, book))

        elif command == 'show-birthday':
            print(show_birthday(args, book))

        elif command == 'birthdays':
            print(birthdays(book))
        elif command == 'save_book':
            print(save_book())

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
