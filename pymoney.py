import sys

def parse_record(record):
    try:
        [item, str_amount] = record.split()
    except:
        sys.stderr.write("The format of a record should be like this: breakfast -50.\n")
        raise
    try:
        int(str_amount)
    except:
        sys.stderr.write("Invalid value for money.\n")
        raise
    return (item, int(str_amount))

def initialize():
    # load file
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

def add(records):
    print("Add an expense or income record with description and amount:")
    try:
        records.append(parse_record(input()))
        return records
    except:
        sys.stderr.write("Fail to add a record.\n")

def view(initial_money, records):
    print("Here's your expense and income records:")
    print('    {:20s} {:6s}'.format('Description', 'Amount'))
    print("=== ==================== ======")
    # for record in records:
    #     print('{:20s} {:6s}'.format(record[0], record[1]))
    # enumerate
    for i, record in enumerate(records):
        print('{:3d} {:20s} {:d}'.format(i+1, record[0], record[1]))


    amount = sum([record[1] for record in records])
    print(f'Now you have {initial_money + amount} dollars.')

def delete(records):
    print("Which record do you want to delete? (1,2,3,...)")
    index = int(input())-1
    if index < 0 or index >= len(records):
        sys.stderr.write("There's no record with index "+ str(index + 1) +". Fail to delete a record.\n")
    else:
        del records[index]
        return records

def save(initial_money, records):
    with open("records.txt", "w") as file:
        file.write(str(initial_money)+'\n')
        file.writelines([f"{record[0]} {record[1]}\n" for record in records])

initial_money, records = initialize()
while True:
    command = input('\nWhat do you want to do (add / view / delete / exit)? ')
    if command == 'add':
        records = add(records)
    elif command == 'view':
        view(initial_money, records)
    elif command == 'delete':
        records = delete(records)
    elif command == 'exit':
        save(initial_money, records)
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')
