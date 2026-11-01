import sys
from datetime import date

inventory = []

def display_date(expiry):
    return date.fromisoformat(expiry).strftime("%d/%m/%Y")

def add_item():
    name=input("Food name: ")
    quantity=int(input("Quantity: "))
    price=float(input("Price: $"))
    expiry=input("Expiry in YYYY-MM-DD: ")
    date.fromisoformat(expiry)
    inventory.append({"name":name,"quantity":quantity,"price":price,"expiry":expiry})

def update_item():
    if not inventory:
        print("Inventory is empty.")
        return
    for n, food in enumerate(inventory, start=1):
        print(n, food["name"], "-", display_date(food["expiry"]))
    try:
        pos=int(input("Select item: "))-1
        food=inventory[pos]
    except (ValueError, IndexError):
        print("Invalid item.")
        return
    print("1. Update quantity\n2. Delete item")
    action=input("Choose: ")
    if action=="1":
        new_q=int(input("New quantity: "))
        if input("Confirm change? (Y/N): ").lower()=="y":
            food["quantity"]=new_q
            print("Quantity updated.")
    elif action=="2":
        if input("Confirm delete? (Y/N): ").lower()=="y":
            inventory.pop(pos)
            print("Item deleted.")

def view_items():
    for food in inventory:
        print(food["name"], food["quantity"], display_date(food["expiry"]))
    if not inventory: print("Inventory is empty.")

while True:
    print("\nSMART PANTRY\n1. View\n2. Add\n3. Update\n4. Exit")
    c=input("Choose: ")
    if c=="1": view_items()
    elif c=="2": add_item()
    elif c=="3": update_item()
    elif c=="4": sys.exit()
    else: print("Invalid option")
