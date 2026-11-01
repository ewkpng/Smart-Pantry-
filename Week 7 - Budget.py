import sys

shopping_list=[]
budget={"limit":0.0,"spent":0.0}

def shopping_total():
    return sum(i["quantity"]*i["estimated_price"] for i in shopping_list)

def budget_page():
    while True:
        estimated=shopping_total()
        print("\n--- GROCERY BUDGET ---")
        print("Weekly budget:", "$"+format(budget["limit"],".2f") if budget["limit"] else "Not set")
        print("Amount spent: $"+format(budget["spent"],".2f"))
        if budget["limit"]:
            remaining=budget["limit"]-budget["spent"]
            projected=budget["spent"]+estimated
            print("Remaining: $"+format(remaining,".2f"))
            print("Projected after shopping list: $"+format(projected,".2f"))
            if projected>budget["limit"]: print("WARNING: Over budget by $"+format(projected-budget["limit"],".2f"))
        print("1. Set budget\n2. Add spending\n3. Reset spending\nB. Back")
        c=input("Choose: ").lower()
        if c=="1": budget["limit"]=float(input("Weekly budget: $"))
        elif c=="2": budget["spent"]+=float(input("Spending amount: $"))
        elif c=="3": budget["spent"]=0.0
        elif c=="b": return
        else: print("Invalid option")

def add_shopping():
    name=input("Item: ")
    qty=int(input("Quantity: "))
    price=float(input("Estimated price each: $"))
    shopping_list.append({"name":name,"quantity":qty,"estimated_price":price})

while True:
    print("\nSMART PANTRY\n1. Add shopping item\n2. Budget\n3. Exit")
    c=input("Choose: ")
    if c=="1": add_shopping()
    elif c=="2": budget_page()
    elif c=="3": sys.exit()
    else: print("Invalid option")
