# 1000
# add
# breakfast -50
# add
# lunch -70
# add
# dinner -100
# view
# add
# breakfast -50
# add
# salary 3500
# view
# delete
# 4
# view
# exit

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


# load file
try:
    file = open("records.txt", "r")
    try:
        init_amount = int(file.readline())
        records = [parse_record(record) for record in file.readlines()]
    except:
        sys.stderr.write("Invalid format in records.txt. Deleting the contents.\n")
        try:
            init_amount = int(input("How much money do you have? "))
            records = []
        except:
            sys.stderr.write("Invalid value for money. Set to 0 by default.\n")
            init_amount = 0
            records = []
    file.close()
except:
    init_amount = int(input("How much money do you have? "))
    records = []
    
while(True):
    command = input("What do you want to do (add / view / delete / exit)? ")
    if command == "add":
        print("Add an expense or income record with description and amount:")
        try:
            records.append(parse_record(input()))
        except:
            sys.stderr.write("Fail to add a record.\n")
    elif command == "view":
        print("Here's your expense and income records:")
        print('    {:20s} {:6s}'.format('Description', 'Amount'))
        print("=== ==================== ======")
        # for record in records:
        #     print('{:20s} {:6s}'.format(record[0], record[1]))
        # enumerate
        for i, record in enumerate(records):
            print('{:3d} {:20s} {:d}'.format(i+1, record[0], record[1]))


        amount = sum([record[1] for record in records])
        print(f'Now you have {init_amount + amount} dollars.')
    elif command == "delete":
        print("Which record do you want to delete? (1,2,3,...)")
        index = int(input())-1
        if index < 0 or index >= len(records):
            sys.stderr.write("There's no record with index "+ str(index + 1) +". Fail to delete a record.\n")
        else:
            del records[index]
    elif command == "exit":
        with open("records.txt", "w") as file:
            file.write(str(init_amount)+'\n')
            file.writelines([f"{record[0]} {record[1]}\n" for record in records])
        break;
    else:
        sys.stderr.write("Invalid command. Try again.\n")
    print("")