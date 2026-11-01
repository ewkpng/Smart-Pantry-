import sys

inventory = []

def get_name():
    while True:
        name = input("Food name: ").strip()
        if name == "": print("Food name cannot be empty.")
        else: return name

def get_quantity():
    while True:
        try:
            quantity = int(input("Quantity: "))
            if quantity < 0: print("Quantity cannot be negative.")
            else: return quantity
        except ValueError:
            print("Please enter a whole number.")

def get_price():
    while True:
        try:
            price = float(input("Price: $"))
            if price < 0: print("Price cannot be negative.")
            else: return price
        except ValueError:
            print("Please enter a valid price.")

def add_item():
    food = {"name": get_name(), "quantity": get_quantity(), "price": get_price()}
    inventory.append(food)
    print(food["name"], "has been added.")

def view_items():
    print("\n--- VIEW ITEMS ---")
    if not inventory: print("Your inventory is currently empty.")
    for number, food in enumerate(inventory, start=1):
        print(number, food["name"], food["quantity"], "$" + format(food["price"], ".2f"))
    input("\nPress Enter to return.")

while True:
    print("\nSMART PANTRY\n1. View items\n2. Add item\n3. Exit")
    choice = input("Choose an option: ")
    if choice == "1": view_items()
    elif choice == "2": add_item()
    elif choice == "3": sys.exit()
    else: print("Invalid option")
