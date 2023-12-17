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
