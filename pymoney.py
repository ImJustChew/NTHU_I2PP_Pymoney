init_amount = int(input("How much money do you have? "))

print("Add an expense or income record with description and amount:")

[item, str_amount] = input().split()
amount = int(str_amount)

print(f'Now you have {init_amount + amount} dollars.')