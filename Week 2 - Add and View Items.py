import sys

inventory = []

def view_items():
    print("\n--- VIEW ITEMS ---")
    if len(inventory) == 0:
        print("Your inventory is currently empty.")
    else:
        for number, food in enumerate(inventory, start=1):
            print(number, food["name"], "- Quantity:", food["quantity"], "- Price: $" + format(food["price"], ".2f"))
    input("\nPress Enter to return to the menu.")

def add_item():
    print("\n--- ADD ITEM ---")
    name = input("Food name: ")
    quantity = int(input("Quantity: "))
    price = float(input("Price: $"))
    food = {"name": name, "quantity": quantity, "price": price}
    inventory.append(food)
    print(name, "has been added.")

while True:
    print("\nSMART PANTRY")
    print("1. View items")
    print("2. Add item")
    print("3. Exit")
    choice = input("Choose an option: ")
    if choice == "1": view_items()
    elif choice == "2": add_item()
    elif choice == "3": sys.exit()
    else: print("Invalid option")
