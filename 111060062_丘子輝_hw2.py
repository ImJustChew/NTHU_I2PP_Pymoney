def parse_record(record):
    [item, str_amount] = record.split()
    return (item, int(str_amount))

init_amount = int(input("How much money do you have? "))

print("Add an expense or income record with description and amount:")
print("desc1 amt1, desc2 amt2, desc3 amt3, ...")

records = [parse_record(record) for record in input().split(',')]

print("Here's your expense and income records:")
for record in records:
    print(f'{record[0]} {record[1]}')

amount = sum([record[1] for record in records])

print(f'Now you have {init_amount + amount} dollars.')