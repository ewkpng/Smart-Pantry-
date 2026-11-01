import sys

inventory=[]
shopping_list=[]
regular_items={}

def total_quantity(name):
    return sum(f["quantity"] for f in inventory if f["name"].lower()==name.lower())

def add_inventory():
    name=input("Food name: ")
    qty=int(input("Quantity: "))
    price=float(input("Price: $"))
    inventory.append({"name":name,"quantity":qty,"price":price})
    if input("Keep this regularly stocked? (Y/N): ").lower()=="y":
        minimum=int(input("Minimum quantity wanted: "))
        regular_items[name.lower()]={"name":name,"minimum":minimum,"estimated_price":price}

def recommendations():
    results=[]
    for key,setting in regular_items.items():
        current=total_quantity(setting["name"])
        if current <= setting["minimum"]:
            results.append((setting,current))
    print("\n--- SHOPPING RECOMMENDATIONS ---")
    for n,(setting,current) in enumerate(results,start=1):
        print(n,setting["name"],"Current:",current,"Minimum:",setting["minimum"])
    if not results: print("No recommendations.")
    return results

def view_inventory():
    for f in inventory: print(f["name"],f["quantity"])
    if not inventory: print("Inventory empty.")

while True:
    print("\nSMART PANTRY\n1. View inventory\n2. Add item\n3. Recommendations\n4. Exit")
    c=input("Choose: ")
    if c=="1": view_inventory()
    elif c=="2": add_inventory()
    elif c=="3": recommendations()
    elif c=="4": sys.exit()
    else: print("Invalid option")
