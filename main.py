from collections import UserDict

class Field:
    required = False
    def __init__(self, value):
        self.value = value

    def __str__(self):  
        return str(self.value)

class Name(Field):
    required = True
    def __init__(self, value):
        if len(value) < 3:
            raise ValueError("Name lenght should has min 3 symbools")
        super().__init__(value)

class Phone(Field):
   def __init__(self, value):
       if len(value) < 10:
            raise ValueError("Phone lenght should has 10 symbools")
       super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

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
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"

    def get_name(self):
        return self.name.value



class AddressBook(UserDict):
    def add_record(self, record):
        if isinstance(record,Record) == False:
           raise TypeError("Should be instance of Record class")
        self.data[record.get_name()] = record
    
    def find(self, name):
        if name not in self.data:
            return None
        return self.data[name]
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]



# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")


# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")