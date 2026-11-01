import sys
from datetime import date

inventory = []

def get_expiry_date():
    while True:
        raw = input("Expiry date (DD/MM or DD/MM/YYYY): ")
        try:
            parts = raw.split("/")
            if len(parts) == 2:
                day, month = int(parts[0]), int(parts[1])
                today = date.today()
                expiry = date(today.year, month, day)
                if expiry < today: expiry = date(today.year + 1, month, day)
                return expiry.isoformat()
            elif len(parts) == 3:
                day, month, year = map(int, parts)
                return date(year, month, day).isoformat()
            print("Use DD/MM or DD/MM/YYYY.")
        except ValueError:
            print("Invalid date.")

def display_date(expiry):
    return date.fromisoformat(expiry).strftime("%d/%m/%Y")

def expiry_status(expiry):
    days = (date.fromisoformat(expiry) - date.today()).days
    if days < 0: return "EXPIRED"
    if days == 0: return "EXPIRES TODAY"
    if days <= 3: return "USE SOON"
    if days <= 7: return "EXPIRING SOON"
    return "OK"

def add_item():
    name = input("Food name: ")
    quantity = int(input("Quantity: "))
    price = float(input("Price: $"))
    expiry = get_expiry_date()
    inventory.append({"name":name,"quantity":quantity,"price":price,"expiry":expiry})

def view_items():
    print("\n--- VIEW ITEMS ---")
    for food in inventory:
        print(food["name"], "| Qty:", food["quantity"], "| Expiry:", display_date(food["expiry"]), "|", expiry_status(food["expiry"]))
    if not inventory: print("Your inventory is currently empty.")
    input("\nPress Enter to return.")

while True:
    print("\nSMART PANTRY\n1. View items\n2. Add item\n3. Exit")
    choice=input("Choose an option: ")
    if choice=="1": view_items()
    elif choice=="2": add_item()
    elif choice=="3": sys.exit()
    else: print("Invalid option")
