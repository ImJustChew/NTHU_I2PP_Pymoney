import sys

class Record:
    """Represents a record."""
    def __init__(self, category, item, amount):
        """Initialize a record with category, item, and amount."""
        self._category = category
        self._item = item
        self._amount = amount

    @staticmethod
    def parse_record(record):
        """Parse a record into a dictionary with keys: category, item, amount"""
        try:
            [cat, item, str_amount] = record.split()
        except:
            sys.stderr.write("The format of a record should be like this: breakfast -50.\n")
            raise
        try:
            int(str_amount)
        except:
            sys.stderr.write("Invalid value for money.\n")
            raise
        return Record(cat, item, int(str_amount))

    
    @property
    def category(self):
        """Return the category of the record."""
        return self._category
    
    @property
    def item(self):
        """Return the item of the record."""
        return self._item
    
    @property
    def amount(self):
        """Return the amount of the record."""
        return self._amount

    def __str__(self):
        """Return a string representation of the record."""
        return f'{self._category} {self._item} {self._amount}'

    def __repr__(self):
        """Return a string representation of the record."""
        return f'Record({self._category}, {self._item}, {self._amount})'

class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):
        """Initialize a list of records and the initial amount of money."""
        try:
            file = open("records.txt", "r")
            try:
                initial_money = int(file.readline())
                records = [Record.parse_record(record) for record in file.readlines()]
            except:
                sys.stderr.write("Invalid format in records.txt. Deleting the contents.\n")
                try:
                    initial_money = int(input("How much money do you have? "))
                    records = []
                except:
                    sys.stderr.write("Invalid value for money. Set to 0 by default.\n")
                    initial_money = 0
                    records = []
            file.close()
        except:
            initial_money = int(input("How much money do you have? "))
            records = []
        self._initial_money = initial_money
        self._records = records
    
    def add(self, records_str, categories):
        """Add a record to the list of records."""
        try:
            new_records = [Record.parse_record(x) for x in records_str.split(',')]
            for record in new_records:
                if not categories.is_category_valid(record.category):
                    sys.stderr.write("The specified category is not in the category list.\n")
                    sys.stderr.write("You can check the category list by command \"view categories\".\n")
                    raise
            self._records.extend(new_records)
        except:
            sys.stderr.write("Fail to add a record.\n")

    def view(self):
        """Prints out all records and the total amount"""
        print("Here's your expense and income records:")
        print('   {:15s} {:20s} {:6s}'.format('Category', 'Description', 'Amount'))
        print("=== =============== ==================== ======")
        # for record in records:
        #     print('{:20s} {:6s}'.format(record[0], record[1]))
        # enumerate
        for i, record in enumerate(self._records):
            print('{:3d} {:15s} {:20s} {:d}'.format(i+1, record.category, record.item, record.amount))
        print("===============================================")

        amount = sum([record.amount for record in self._records])
        print(f'Now you have {self._initial_money + amount} dollars.')

    def delete(self, _index):
        """Delete a record from records"""
        index = int(_index) - 1
        if index < 0 or index >= len(self._records):
            sys.stderr.write("There's no record with index "+ str(index + 1) +". Fail to delete a record.\n")
        else:
            del self._records[index]
    
    def find(self, subcategories):
        """Find records with specified subcategories"""
        print(f"Here's your expense and income records under category \"{subcategories[0]}\":")
        print('   {:15s} {:20s} {:6s}'.format('Category', 'Description', 'Amount'))
        print("=== =============== ==================== ======")
        for i, record in enumerate(filter(lambda x: x.category in subcategories, self._records)):
            print('{:3d} {:15s} {:20s} {:d}'.format(i+1, record.category, record.item, record.amount))
        print("===============================================")
        amount = sum([record.amount for record in self._records if record.category in subcategories])
        print(f"The total amount above is {amount}.")

    def save(self):
        """Save initial_money and records to file"""
        with open("records.txt", "w") as file:
            file.write(str(self._initial_money)+'\n')
            file.writelines([f"{str(record)}\n" for record in self._records])

class Categories:
    """Maintain the category list and provide some methods."""

    def __init__(self):
        """Initialize categories"""
        categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]
        self._categories = categories
    
    def view(self):
        """Prints out all categories"""
        def resursive_view_categories(categories, depth=0):
            """Prints out all categories"""
            for cat in categories:
                if type(cat) is list:
                    resursive_view_categories(cat, depth+1)
                else:
                    # add - infront and spaces for each depth
                    print('  ' * depth + '- '  + cat)
        resursive_view_categories(self._categories)

    def is_category_valid(self, category):
        """Check if the category is valid"""
        def resursive_nested_check(arr, category):
            if type(arr) is list:
                for item in arr:
                    if resursive_nested_check(item, category):
                        return True
                return False
            else:
                return arr == category
        return resursive_nested_check(self._categories, category)
        
    def find_subcategories(self, category):
        """Find all subcategories of the specified category"""
        def find_subcategories_gen(category, categories):
            if type(categories) is list:
                for i, cat in enumerate(categories):
                    if type(cat) is list:
                        yield from find_subcategories_gen(category, cat)
                    elif cat == category:
                        yield from ([cat] + categories[i+1]) if i+1 < len(categories) and type(categories[i+1]) is list else [cat]
        return list(find_subcategories_gen(category, self._categories))
    
categories = Categories()
records = Records()

while True:
    command = input('\nWhat do you want to do (add / view / delete / view categories / find / exit)? ')
    if command == 'add':
        record = input('Add some expense or income records with category, description, and amount (separate by spaces):\ncat1 desc1 amt1, cat2 desc2 amt2, cat3 desc3 amt3, ...\n')
        records.add(record, categories)
    elif command == 'view':
        records.view()
    elif command == 'delete':
        delete_record = input("Which record do you want to delete? (1,2,3)")
        records.delete(delete_record)
    elif command == 'view categories':
        categories.view()
    elif command == 'find':
        category = input('Which category do you want to find? ')
        target_categories = categories.find_subcategories(category)
        print(target_categories)
        records.find(target_categories)
    elif command == 'exit':
        records.save()
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')