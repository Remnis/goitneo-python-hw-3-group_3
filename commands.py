from address_book import AddressBook
from record import Record

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Error: {e}"
    return wrapper

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
