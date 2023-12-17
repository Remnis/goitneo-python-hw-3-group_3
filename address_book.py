from collections import UserDict
from datetime import datetime
from record import Record
from copy import deepcopy

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
    
    def __deepcopy__(self,memo):
        copy_object = AddressBook()
        memo[id(copy_object)] = copy_object
        copy_object.data = deepcopy(self.data, memo)
        return copy_object

