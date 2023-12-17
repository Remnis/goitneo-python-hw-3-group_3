from commands import add_contact, change_contact, show_phone, show_all, add_birthday, show_birthday, birthdays, save_contacts, load_contacts
from address_book import AddressBook


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
# save-contacts: save all contacts
# load-contacts: load all contacts
# exit|close: exit from program
"""

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

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
        
        elif command == 'save-contacts':
            print(save_contacts(book))
        
        elif command == 'load-contacts':
            print(load_contacts(book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
