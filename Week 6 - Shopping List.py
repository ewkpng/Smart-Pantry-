import sys

inventory=[]
shopping_list=[]

def add_to_shopping_list(name, quantity=1, price=0.0, source="Manual"):
    for item in shopping_list:
        if item["name"].lower()==name.lower():
            item["quantity"] += quantity
            return
    shopping_list.append({"name":name,"quantity":quantity,"estimated_price":price,"source":source})

def manage_shopping_list():
    while True:
        print("\n--- SHOPPING LIST ---")
        for n,item in enumerate(shopping_list,start=1):
            print(n,item["name"],"Qty:",item["quantity"])
        if not shopping_list: print("Shopping list is empty.")
        print("A. Add manually\nD. Delete\nB. Back")
        c=input("Choose: ").lower()
        if c=="a":
            name=input("Item name: ")
            qty=int(input("Quantity: "))
            price=float(input("Estimated price: $"))
            add_to_shopping_list(name,qty,price)
        elif c=="d" and shopping_list:
            try: shopping_list.pop(int(input("Item number: "))-1)
            except (ValueError,IndexError): print("Invalid item")
        elif c=="b": return
        else: print("Invalid option")

def add_inventory_item():
    name=input("Food name: ")
    qty=int(input("Quantity: "))
    price=float(input("Price: $"))
    inventory.append({"name":name,"quantity":qty,"price":price})

def inventory_page():
    for n,f in enumerate(inventory,start=1): print(n,f["name"],f["quantity"])
    if inventory and input("Add an inventory item to shopping list? (Y/N): ").lower()=="y":
        try:
            f=inventory[int(input("Item number: "))-1]
            add_to_shopping_list(f["name"],1,f["price"],"Inventory transfer")
        except (ValueError,IndexError): print("Invalid item")

while True:
    print("\nSMART PANTRY\n1. Inventory\n2. Add inventory item\n3. Shopping list\n4. Exit")
    c=input("Choose: ")
    if c=="1": inventory_page()
    elif c=="2": add_inventory_item()
    elif c=="3": manage_shopping_list()
    elif c=="4": sys.exit()
    else: print("Invalid option")
