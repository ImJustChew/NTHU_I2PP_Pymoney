import sys

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
    return {
        'category': cat,
        'item': item,
        'amount': int(str_amount)
    }

def initialize():
    """Load file and initialize initial_money and records"""
    try:
        file = open("records.txt", "r")
        try:
            initial_money = int(file.readline())
            records = [parse_record(record) for record in file.readlines()]
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
    return initial_money, records

def initialize_categories():
    """Initialize categories"""
    categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]
    return categories



def add(records):
    """Handles parsing user input and adding a record to records"""
    print("Add some expense or income records with category, description, and amount (separate by spaces):")
    print("cat1 desc1 amt1, cat2 desc2 amt2, cat3 desc3 amt3, ...")
    try:
        new_records = [parse_record(x) for x in input().split(',')]
        records.extend(new_records)
        return records
    except:
        sys.stderr.write("Fail to add a record.\n")

def view(initial_money, records):
    """Prints out all records and the total amount"""
    print("Here's your expense and income records:")
    print('   {:15s} {:20s} {:6s}'.format('Category', 'Description', 'Amount'))
    print("=== =============== ==================== ======")
    # for record in records:
    #     print('{:20s} {:6s}'.format(record[0], record[1]))
    # enumerate
    for i, record in enumerate(records):
        print('{:3d} {:15s} {:20s} {:d}'.format(i+1, record['category'], record['item'], record['amount']))
    print("===============================================")

    amount = sum([record['amount'] for record in records])
    print(f'Now you have {initial_money + amount} dollars.')

def view_categories(categories, depth=0):
    """Prints out all categories"""
    for cat in categories:
        if type(cat) is list:
            view_categories(cat, depth+1)
        else:
            # add - infront and spaces for each depth
            print('  ' * depth + '- '  + cat)

def find_subcategories(categories, category): 
    """Find a category and return the category and its subcategories flattened"""
    def flatten(arr):
        result = []
        for item in arr:
            if type(item) is list:
                result.extend(flatten(item))
            else:
                result.append(item)
        return result
    if type(categories) is list:
        for i, cat in enumerate(categories):
            if type(cat) is list:
                result = find_subcategories(cat, category)
                if result:
                    return result
            elif cat == category:
                return flatten(([cat] + categories[i+1]) if i+1 < len(categories) and type(categories[i+1]) is list else [cat])
    return []
        
def find(records, categories):
    """Find a category and print out all records under that category"""
    print("Which category do you want to find?")
    category = input()
    subcategories = find_subcategories(categories, category)
    if not subcategories:
        sys.stderr.write("Category not found.\n")
        return
    print(f"Here's your expense and income records under category \"{category}\":")
    print('   {:15s} {:20s} {:6s}'.format('Category', 'Description', 'Amount'))
    print("=== =============== ==================== ======")
    for i, record in enumerate(filter(lambda x: x['category'] in subcategories, records)):
        print('{:3d} {:15s} {:20s} {:d}'.format(i+1, record['category'], record['item'], record['amount']))
    print("===============================================")
    amount = sum([record['amount'] for record in records if record['category'] in subcategories])
    print(f"The total amount above is {amount}.")


def delete(records):
    """Delete a record from records"""
    print("Which record do you want to delete? (1,2,3,...)")
    index = int(input())-1
    if index < 0 or index >= len(records):
        sys.stderr.write("There's no record with index "+ str(index + 1) +". Fail to delete a record.\n")
    else:
        del records[index]
        return records

def save(initial_money, records):
    """Save initial_money and records to file"""
    with open("records.txt", "w") as file:
        file.write(str(initial_money)+'\n')
        file.writelines([f"{record['category']} {record['item']} {record['amount']}\n" for record in records])

initial_money, records = initialize()
categories = initialize_categories()
while True:
    command = input('\nWhat do you want to do (add / view / delete / view categories / find / exit)? ')
    if command == 'add':
        records = add(records)
    elif command == 'view':
        view(initial_money, records)
    elif command == 'view categories':
        view_categories(categories)
    elif command == 'find':
        find(records, categories)
    elif command == 'delete':
        records = delete(records)
    elif command == 'exit':
        save(initial_money, records)
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')
