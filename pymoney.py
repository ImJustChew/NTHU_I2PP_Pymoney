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

def parse_record(record):
    [item, str_amount] = record.split()
    return (item, int(str_amount))


init_amount = int(input("How much money do you have? "))
records = []
while(True):
    command = input("What do you want to do (add / view / delete / exit)? ")
    if command == "add":
        print("Add an expense or income record with description and amount:")
        records.append(parse_record(input()))
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
        del records[int(input())-1]
    elif command == "exit":
        break;
    print("")