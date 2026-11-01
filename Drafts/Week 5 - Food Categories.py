import sys
from datetime import date

inventory=[]
next_item_id=1

def choose_category():
    while True:
        print("1. Fridge / Fresh\n2. Pantry\n3. Frozen")
        c=input("Choose category: ")
        if c=="1": return "Fridge / Fresh"
        if c=="2": return "Pantry"
        if c=="3": return "Frozen"
        print("Invalid option")

def add_item():
    global next_item_id
    name=input("Food name: ")
    quantity=int(input("Quantity: "))
    price=float(input("Price: $"))
    expiry=input("Expiry YYYY-MM-DD: ")
    date.fromisoformat(expiry)
    category=choose_category()
    inventory.append({"id":next_item_id,"name":name,"quantity":quantity,"price":price,"expiry":expiry,"category":category})
    next_item_id += 1

def view_items():
    for category in ["Fridge / Fresh","Pantry","Frozen"]:
        foods=[f for f in inventory if f["category"]==category]
        if foods:
            print("\n---",category.upper(),"---")
            for f in foods:
                print(f["name"], "Qty:",f["quantity"], "Expiry:",f["expiry"])
    if not inventory: print("Inventory is empty.")

while True:
    print("\nSMART PANTRY\n1. View inventory\n2. Add item\n3. Exit")
    c=input("Choose: ")
    if c=="1": view_items()
    elif c=="2": add_item()
    elif c=="3": sys.exit()
    else: print("Invalid option")
