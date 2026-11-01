#setting up display page and what possible actions can be taken



#import sys just makes it possible to run sys exit to exit the program

import sys



#Creating in app date tracker

from datetime import date

#import tkinter for the graphical user interface
import tkinter as tk
from tkinter import ttk, messagebox





#creating inventory

inventory = []



#stores messages that the user has cleared

cleared_messages = set()



#creates a different id for every item added

#this allows multiple groups of the same food to exist

next_item_id = 1



#shopping list stores items that need to be bought

shopping_list = []



#stores items that the household wants to keep regularly stocked

regular_items = {}



#stores permanent lunch and dinner responses until manually cleared

meal_responses = {}



#stores lunch and dinner update messages separately from the permanent board

meal_messages = []



#creates a different id for every meal message

next_meal_message_id = 1



#stores the weekly grocery budget and current spending

budget = {

    "limit": 0.0,

    "spent": 0.0

}





#------------------------------------------------

# BASIC INPUT FUNCTIONS

#------------------------------------------------



#allows the user to cancel an input with B or exit with Q

def cancelable_input(prompt):



    answer = input(prompt)



    if answer.lower() == "b":

        return None



    elif answer.lower() == "q":

        print("Exiting program")

        sys.exit()



    return answer





#reusable yes or no function

#returns True for yes, False for no and None for back

def yes_no(prompt):



    while True:



        answer = input(prompt).lower()



        if answer == "y":

            return True



        elif answer == "n":

            return False



        elif answer == "b":

            return None



        elif answer == "q":

            print("Exiting program")

            sys.exit()



        else:

            print("Please enter Y, N, B or Q.")





#asks for the food name

def get_food_name(prompt="Food name: "):



    while True:



        name = cancelable_input(prompt)



        if name is None:

            return None



        elif name.strip() == "":

            print("Food name cannot be empty.")



        else:

            return name.strip()





#asks for the quantity and makes sure it is a whole number

def get_quantity(prompt="Quantity: "):



    while True:



        quantity = cancelable_input(prompt)



        if quantity is None:

            return None



        try:



            quantity = int(quantity)



            if quantity < 0:

                print("Quantity cannot be negative.")



            else:

                return quantity



        except ValueError:

            print("Please enter a whole number for the quantity.")





#asks for the price and makes sure it is a number

def get_price(prompt="Price per item: $"):



    while True:



        price = cancelable_input(prompt)



        if price is None:

            return None



        try:



            price = float(price)



            if price < 0:

                print("Price cannot be negative.")



            else:

                return price



        except ValueError:

            print("Please enter a valid price.")


#asks for a weight and allows decimal values such as 0.5 kg
def get_weight(prompt="Weight in kg: "):

    while True:

        weight = cancelable_input(prompt)

        if weight is None:
            return None

        try:

            weight = float(weight)

            if weight < 0:
                print("Weight cannot be negative.")

            else:
                return weight

        except ValueError:
            print("Please enter a valid weight in kilograms.")


#asks whether the food is priced per item or by kilogram
def choose_price_type():

    while True:

        print("\nHow is this food priced?")
        print("1. Per item")
        print("2. Per kilogram")
        print("B. Cancel")
        print("Q. Exit")

        choice = input("Choose an option: ").lower()

        if choice == "1":
            return "item"

        elif choice == "2":
            return "kg"

        elif choice == "b":
            return None

        elif choice == "q":
            print("Exiting program")
            sys.exit()

        else:
            print("Invalid option.")





#------------------------------------------------

# DATE FUNCTIONS

#------------------------------------------------



#Creating the expiry date system

#the user can enter DD/MM or DD/MM/YYYY

def get_expiry_date():



    while True:



        expiry_input = cancelable_input(

            "Expiry date (DD/MM or DD/MM/YYYY): "

        )



        if expiry_input is None:

            return None



        try:



            parts = expiry_input.split("/")



            #if only the day and month are entered

            if len(parts) == 2:



                day = int(parts[0])

                month = int(parts[1])



                today = date.today()



                #uses the next matching date that has not already passed

                for year in range(today.year, today.year + 5):



                    try:



                        expiry = date(year, month, day)



                        if expiry >= today:

                            return expiry.isoformat()



                    except ValueError:

                        continue



                print("Invalid date.")



            #if the user enters their own year

            elif len(parts) == 3:



                day = int(parts[0])

                month = int(parts[1])

                year = int(parts[2])



                expiry = date(year, month, day)



                return expiry.isoformat()



            else:



                print(

                    "Please enter the date as DD/MM "

                    "or DD/MM/YYYY."

                )



        except ValueError:



            print("Invalid date. Please try again.")





#changes the saved expiry date into DD/MM/YYYY

def display_date(expiry):



    expiry_date = date.fromisoformat(expiry)



    return expiry_date.strftime("%d/%m/%Y")





#works out how many days are left until expiry

def days_until_expiry(expiry):



    expiry_date = date.fromisoformat(expiry)



    return (expiry_date - date.today()).days





#checks how long there is until an item expires

def check_expiry(expiry):



    days_left = days_until_expiry(expiry)



    if days_left < 0:

        return "EXPIRED"



    elif days_left == 0:

        return "EXPIRES TODAY"



    elif days_left == 1:

        return "USE SOON - 1 day left"



    elif days_left <= 3:

        return "USE SOON - " + str(days_left) + " days left"



    elif days_left <= 7:

        return "EXPIRING SOON - " + str(days_left) + " days left"



    else:

        return "OK - " + str(days_left) + " days left"





#------------------------------------------------

# CATEGORY FUNCTIONS

#------------------------------------------------



#allows food to be organised by storage area

def choose_category():



    while True:



        print("\nSelect food category:")

        print("1. Fridge / Fresh")

        print("2. Pantry")

        print("3. Frozen")

        print("B. Cancel")

        print("Q. Exit")



        choice = input("Choose a category: ").lower()



        if choice == "1":

            return "Fridge / Fresh"



        elif choice == "2":

            return "Pantry"



        elif choice == "3":

            return "Frozen"



        elif choice == "b":

            return None



        elif choice == "q":

            print("Exiting program")

            sys.exit()



        else:

            print("Invalid option.")





#turns food names into a standard form for comparisons

def normalise_name(name):



    return name.strip().lower()


#creates a separate regular-item key for item-priced and kg-priced foods
def regular_key(name, price_type):

    return normalise_name(name) + "|" + price_type





#works out the total quantity of a food across all expiry batches

def total_inventory_quantity(name, price_type=None):

    total = 0
    key = normalise_name(name)

    for food in inventory:

        same_name = normalise_name(food["name"]) == key

        if price_type is None:
            same_type = True
        else:
            same_type = food["price_type"] == price_type

        if same_name and same_type:
            total += food["quantity"]

    return total





#------------------------------------------------

# REGULAR ITEM / RECOMMENDATION FUNCTIONS

#------------------------------------------------



#sets whether a food should always be kept in stock

def get_regular_setting(name, price, category, price_type):

    key = regular_key(name, price_type)

    #if the food is already a regular item, reuse the existing setting
    if key in regular_items:

        setting = regular_items[key]

        if price_type == "kg":
            minimum_text = str(setting["minimum"]) + " kg"
        else:
            minimum_text = str(setting["minimum"]) + " items"

        print(
            name,
            "is already a regular item with a minimum of",
            minimum_text
        )

        return True, setting["minimum"]

    regular = yes_no(
        "Should " + name + " be kept regularly stocked? (Y/N, B to cancel): "
    )

    if regular is None:
        return None, None

    if regular is False:
        return False, 0

    if price_type == "kg":
        minimum = get_weight(
            "Minimum weight you want to keep in stock (kg): "
        )
    else:
        minimum = get_quantity(
            "Minimum quantity you want to keep in stock: "
        )

    if minimum is None:
        return None, None

    return True, minimum





#creates shopping recommendations for regular items that are low

def shopping_recommendations():

    recommendations = []

    for key, setting in regular_items.items():

        current_quantity = total_inventory_quantity(
            setting["name"],
            setting["price_type"]
        )

        #creates a recommendation when the amount falls below the minimum
        if current_quantity < setting["minimum"]:

            recommendations.append({
                "key": key,
                "name": setting["name"],
                "current_quantity": current_quantity,
                "minimum": setting["minimum"],
                "estimated_price": setting["estimated_price"],
                "category": setting["category"],
                "price_type": setting["price_type"]
            })

    return recommendations





#------------------------------------------------

# SHOPPING LIST FUNCTIONS

#------------------------------------------------



#adds an item to the shopping list

#matching items are combined instead of duplicated

def add_to_shopping_list(
    name,
    quantity=1,
    estimated_price=0.0,
    source="Manual",
    price_type="item"
):

    key = normalise_name(name)

    for item in shopping_list:

        same_name = normalise_name(item["name"]) == key
        same_type = item["price_type"] == price_type

        #only combines matching foods that use the same pricing type
        if same_name and same_type:

            item["quantity"] += quantity

            if item["estimated_price"] == 0 and estimated_price > 0:
                item["estimated_price"] = estimated_price

            print(name, "has been updated on the shopping list.")
            return

    shopping_list.append({
        "name": name,
        "quantity": quantity,
        "estimated_price": estimated_price,
        "source": source,
        "price_type": price_type
    })

    print(name, "has been added to the shopping list.")





#calculates the estimated cost of the shopping list

def shopping_list_total():



    total = 0.0



    for item in shopping_list:

        total += item["quantity"] * item["estimated_price"]



    return total





#shopping list page

#------------------------------------------------
# VIEW SHOPPING LIST
#------------------------------------------------

#shows the whole shopping list without editing it
def view_shopping_list():

    print("\n--- FULL SHOPPING LIST ---")

    #checks if there is nothing on the shopping list
    if len(shopping_list) == 0:

        print("Your shopping list is currently empty.")

    else:

        #goes through every item currently on the shopping list
        for number, item in enumerate(shopping_list, start=1):

            print("\nItem", number)
            print("Food name:", item["name"])

            if item["price_type"] == "kg":

                print("Weight:", item["quantity"], "kg")
                print(
                    "Estimated price per kg: $"
                    + format(item["estimated_price"], ".2f")
                )

            else:

                print("Quantity:", item["quantity"])
                print(
                    "Estimated price each: $"
                    + format(item["estimated_price"], ".2f")
                )

            #works out the estimated total for this shopping item
            item_total = (
                item["quantity"]
                * item["estimated_price"]
            )

            print(
                "Estimated total: $"
                + format(item_total, ".2f")
            )

            print("Added from:", item["source"])

        #shows the estimated cost of the whole shopping list
        print(
            "\nEstimated shopping total: $"
            + format(shopping_list_total(), ".2f")
        )

    #allows the user to return to the main menu or exit
    while True:

        choice = input(
            "\nEnter B to go back to menu or Q to exit: "
        ).lower()

        if choice == "b":
            return

        elif choice == "q":
            print("Exiting program")
            sys.exit()

        else:
            print("Invalid option")


def shopping_list_page():

    while True:

        print("\n--- SHOPPING LIST ---")

        if len(shopping_list) == 0:
            print("Your shopping list is currently empty.")

        else:

            for number, item in enumerate(shopping_list, start=1):

                if item["price_type"] == "kg":
                    amount_text = str(item["quantity"]) + " kg"
                    price_text = "Price per kg: $" + format(
                        item["estimated_price"], ".2f"
                    )
                else:
                    amount_text = str(item["quantity"]) + " items"
                    price_text = "Price each: $" + format(
                        item["estimated_price"], ".2f"
                    )

                print(
                    str(number) + ".",
                    item["name"],
                    "-", amount_text,
                    "-", price_text
                )

            print(
                "\nEstimated shopping list total: $"
                + format(shopping_list_total(), ".2f")
            )

        print("\nA. Add item manually")
        print("R. View shopping recommendations")
        print("D. Delete shopping list item")
        print("B. Back to main menu")
        print("Q. Exit")

        choice = input("\nChoose an option: ").lower()

        #manually adds an item
        if choice == "a":

            name = get_food_name("Shopping item name: ")

            if name is None:
                continue

            price_type = choose_price_type()

            if price_type is None:
                continue

            if price_type == "kg":

                quantity = get_weight("Weight to buy in kg: ")

                if quantity is None:
                    continue

                estimated_price = get_price(
                    "Estimated price per kg: $"
                )

            else:

                quantity = get_quantity("Quantity to buy: ")

                if quantity is None:
                    continue

                estimated_price = get_price(
                    "Estimated price per item: $"
                )

            if estimated_price is None:
                continue

            add_to_shopping_list(
                name,
                quantity,
                estimated_price,
                "Manual",
                price_type
            )

        #shows recommendations based on regular items
        elif choice == "r":

            recommendations = shopping_recommendations()

            if len(recommendations) == 0:

                print("There are currently no shopping recommendations.")
                continue

            print("\n--- SHOPPING RECOMMENDATIONS ---")

            for number, item in enumerate(recommendations, start=1):

                if item["price_type"] == "kg":
                    current_text = str(item["current_quantity"]) + " kg"
                    minimum_text = str(item["minimum"]) + " kg"
                else:
                    current_text = str(item["current_quantity"]) + " items"
                    minimum_text = str(item["minimum"]) + " items"

                print(
                    str(number) + ".",
                    item["name"],
                    "- Current:", current_text,
                    "- Minimum wanted:", minimum_text
                )

            print("\nEnter a number to add that recommendation.")
            print("B. Back")

            recommendation_choice = input("Choose an option: ").lower()

            if recommendation_choice == "b":
                continue

            try:

                position = int(recommendation_choice) - 1

                if position < 0 or position >= len(recommendations):
                    print("Invalid recommendation number.")
                    continue

                selected = recommendations[position]

                amount_needed = (
                    selected["minimum"]
                    - selected["current_quantity"]
                )

                #whole-item recommendations cannot be below one item
                if selected["price_type"] == "item":
                    amount_needed = max(1, int(amount_needed))
                else:
                    amount_needed = round(amount_needed, 2)

                add_to_shopping_list(
                    selected["name"],
                    amount_needed,
                    selected["estimated_price"],
                    "Recommendation",
                    selected["price_type"]
                )

            except ValueError:

                print("Invalid option.")

        #deletes something from the shopping list
        elif choice == "d":

            if len(shopping_list) == 0:
                print("Shopping list is empty.")
                continue

            delete_choice = input(
                "Enter the shopping list item number to delete: "
            )

            try:

                position = int(delete_choice) - 1

                if position < 0 or position >= len(shopping_list):
                    print("Invalid item number.")
                    continue

                selected = shopping_list[position]

                confirmed = yes_no(
                    "Delete "
                    + selected["name"]
                    + " from the shopping list? (Y/N): "
                )

                if confirmed is True:

                    shopping_list.pop(position)
                    print("Shopping list item deleted.")

                elif confirmed is False:
                    print("Delete cancelled.")

            except ValueError:
                print("Please enter a valid item number.")

        elif choice == "b":
            return

        elif choice == "q":
            print("Exiting program")
            sys.exit()

        else:
            print("Invalid option.")





#------------------------------------------------

# VIEW INVENTORY

#------------------------------------------------



#creating the view items page

def view_items():

    print("\n--- VIEW ITEMS ---")

    if len(inventory) == 0:

        print("Your inventory is currently empty.")

    else:

        #splits the inventory into the three food categories
        for category in ["Fridge / Fresh", "Pantry", "Frozen"]:

            foods_in_category = [
                food
                for food in inventory
                if food["category"] == category
            ]

            if len(foods_in_category) > 0:

                print("\n---", category.upper(), "---")

                for food in foods_in_category:

                    print("\nFood name:", food["name"])
                    print("Batch ID:", food["id"])

                    if food["price_type"] == "kg":

                        print("Weight:", food["quantity"], "kg")
                        print(
                            "Price per kg: $"
                            + format(food["price"], ".2f")
                        )

                    else:

                        print("Quantity:", food["quantity"])
                        print(
                            "Price each: $"
                            + format(food["price"], ".2f")
                        )

                    print(
                        "Total value: $"
                        + format(
                            food["quantity"] * food["price"],
                            ".2f"
                        )
                    )
                    print(
                        "Expiry date:",
                        display_date(food["expiry"])
                    )
                    print(
                        "Status:",
                        check_expiry(food["expiry"])
                    )

    while True:

        choice = input(
            "\nEnter B to go back to menu or Q to exit: "
        ).lower()

        if choice == "b":
            return

        elif choice == "q":
            print("Exiting program")
            sys.exit()

        else:
            print("Invalid option")





#------------------------------------------------

# ADD ITEM

#------------------------------------------------



#creating the add item page

def add_item():

    global next_item_id

    print("\n--- ADD ITEM ---")
    print("Enter B at any time to cancel and go back.")
    print("Enter Q at any time to exit Smart Pantry.")

    name = get_food_name()

    if name is None:
        print("Adding item cancelled.")
        return

    #asks whether this food is priced per item or per kilogram
    price_type = choose_price_type()

    if price_type is None:
        print("Adding item cancelled.")
        return

    if price_type == "kg":

        quantity = get_weight("Weight in kg: ")

        if quantity is None:
            print("Adding item cancelled.")
            return

        price = get_price("Price per kg: $")

    else:

        quantity = get_quantity("Quantity: ")

        if quantity is None:
            print("Adding item cancelled.")
            return

        price = get_price("Price per item: $")

    if price is None:
        print("Adding item cancelled.")
        return

    expiry = get_expiry_date()

    if expiry is None:
        print("Adding item cancelled.")
        return

    category = choose_category()

    if category is None:
        print("Adding item cancelled.")
        return

    regular, minimum = get_regular_setting(
        name,
        price,
        category,
        price_type
    )

    if regular is None:
        print("Adding item cancelled.")
        return

    #checks the item before anything is actually added
    while True:

        print("\n--- CHECK ITEM ---")
        print("Food name:", name)

        if price_type == "kg":
            print("Weight:", quantity, "kg")
            print("Price per kg: $" + format(price, ".2f"))
        else:
            print("Quantity:", quantity)
            print("Price per item: $" + format(price, ".2f"))

        print(
            "Total cost: $"
            + format(quantity * price, ".2f")
        )
        print("Expiry:", display_date(expiry))
        print("Category:", category)

        if regular:
            print("Regular item: Yes")

            if price_type == "kg":
                print("Minimum wanted:", minimum, "kg")
            else:
                print("Minimum wanted:", minimum, "items")

        else:
            print("Regular item: No")

        print("\n1. Confirm and add item")
        print("2. Edit item information")
        print("B. Cancel item")
        print("Q. Exit program")

        confirm = input("\nIs this item finished? ").lower()

        #confirms and adds the item
        if confirm == "1":

            food = {
                "id": next_item_id,
                "name": name,
                "quantity": quantity,
                "price": price,
                "price_type": price_type,
                "expiry": expiry,
                "category": category
            }

            inventory.append(food)

            #if it is a regular item save the recommendation settings
            if regular:

                regular_items[regular_key(name, price_type)] = {
                    "name": name,
                    "minimum": minimum,
                    "estimated_price": price,
                    "category": category,
                    "price_type": price_type
                }

            #quantity x price works for both items and kilograms
            budget["spent"] += quantity * price

            next_item_id += 1

            print(
                "\n" + name
                + " has been added to the inventory."
            )

            return

        #allows information to be edited before confirmation
        elif confirm == "2":

            while True:

                print("\n--- EDIT ITEM ---")
                print("1. Food name")

                if price_type == "kg":
                    print("2. Weight")
                    print("3. Price per kg")
                else:
                    print("2. Quantity")
                    print("3. Price per item")

                print("4. Expiry date")
                print("5. Category")
                print("6. Regular item setting")
                print("7. Pricing type")
                print("B. Return to check item")
                print("Q. Exit program")

                edit = input(
                    "What would you like to edit? "
                ).lower()

                if edit == "1":

                    new_name = get_food_name(
                        "New food name: "
                    )

                    if new_name is not None:

                        name = new_name

                        regular, minimum = get_regular_setting(
                            name,
                            price,
                            category,
                            price_type
                        )

                        if regular is None:
                            regular = False
                            minimum = 0

                elif edit == "2":

                    if price_type == "kg":
                        new_quantity = get_weight(
                            "New weight in kg: "
                        )
                    else:
                        new_quantity = get_quantity(
                            "New quantity: "
                        )

                    if new_quantity is not None:
                        quantity = new_quantity

                elif edit == "3":

                    if price_type == "kg":
                        new_price = get_price(
                            "New price per kg: $"
                        )
                    else:
                        new_price = get_price(
                            "New price per item: $"
                        )

                    if new_price is not None:
                        price = new_price

                elif edit == "4":

                    new_expiry = get_expiry_date()

                    if new_expiry is not None:
                        expiry = new_expiry

                elif edit == "5":

                    new_category = choose_category()

                    if new_category is not None:
                        category = new_category

                elif edit == "6":

                    new_regular, new_minimum = get_regular_setting(
                        name,
                        price,
                        category,
                        price_type
                    )

                    if new_regular is not None:
                        regular = new_regular
                        minimum = new_minimum

                elif edit == "7":

                    new_price_type = choose_price_type()

                    if (
                        new_price_type is not None
                        and new_price_type != price_type
                    ):

                        #asks for new amount and price because the unit changed
                        if new_price_type == "kg":
                            new_quantity = get_weight(
                                "Weight in kg: "
                            )
                            new_price = get_price(
                                "Price per kg: $"
                            )
                        else:
                            new_quantity = get_quantity(
                                "Quantity: "
                            )
                            new_price = get_price(
                                "Price per item: $"
                            )

                        if (
                            new_quantity is not None
                            and new_price is not None
                        ):
                            price_type = new_price_type
                            quantity = new_quantity
                            price = new_price

                            #the regular setting also needs to match the new unit
                            regular, minimum = get_regular_setting(
                                name,
                                price,
                                category,
                                price_type
                            )

                            if regular is None:
                                regular = False
                                minimum = 0

                elif edit == "b":
                    break

                elif edit == "q":
                    print("Exiting program")
                    sys.exit()

                else:
                    print("Invalid option.")

        elif confirm == "b":

            print("Item was not added.")
            return

        elif confirm == "q":

            print("Exiting program")
            sys.exit()

        else:
            print("Invalid option.")





#------------------------------------------------

# UPDATE ITEMS

#------------------------------------------------



#Creating update items page

def update_item():

    while True:

        print("\n--- UPDATE ITEMS ---")

        if len(inventory) == 0:

            print("Your inventory is currently empty.")
            return

        #shows names with expiry dates so identical foods can be told apart
        for number, food in enumerate(inventory, start=1):

            if food["price_type"] == "kg":
                amount_text = str(food["quantity"]) + " kg"
            else:
                amount_text = str(food["quantity"]) + " items"

            print(
                str(number) + ".",
                food["name"],
                "-", amount_text,
                "- expires",
                display_date(food["expiry"])
            )

        print("\nB. Back to menu")
        print("Q. Exit program")

        choice = input("\nSelect an item: ")

        if choice.lower() == "b":
            return

        elif choice.lower() == "q":
            print("Exiting program")
            sys.exit()

        try:

            item_number = int(choice) - 1

            if item_number < 0 or item_number >= len(inventory):

                print("Invalid item number.")
                continue

            food = inventory[item_number]

            while True:

                print("\n---", food["name"], "---")
                print(
                    "Expiry:",
                    display_date(food["expiry"])
                )

                if food["price_type"] == "kg":
                    print("Current weight:", food["quantity"], "kg")
                    print(
                        "Price per kg: $"
                        + format(food["price"], ".2f")
                    )
                    print("\n1. Update weight")
                else:
                    print("Current quantity:", food["quantity"])
                    print(
                        "Price per item: $"
                        + format(food["price"], ".2f")
                    )
                    print("\n1. Update quantity")

                print("2. Delete item")
                print("3. Add to shopping list")
                print("B. Back to item list")
                print("Q. Exit program")

                action = input(
                    "\nChoose an option: "
                ).lower()

                #updates quantity or weight with confirmation
                if action == "1":

                    if food["price_type"] == "kg":
                        new_quantity = get_weight(
                            "Enter new weight in kg: "
                        )
                        old_text = str(food["quantity"]) + " kg"

                        if new_quantity is not None:
                            new_text = str(new_quantity) + " kg"
                    else:
                        new_quantity = get_quantity(
                            "Enter new quantity: "
                        )
                        old_text = str(food["quantity"])

                        if new_quantity is not None:
                            new_text = str(new_quantity)

                    if new_quantity is None:
                        continue

                    confirmed = yes_no(
                        "Confirm change from "
                        + old_text
                        + " to "
                        + new_text
                        + "? (Y/N): "
                    )

                    if confirmed is True:

                        food["quantity"] = new_quantity

                        if food["price_type"] == "kg":
                            print(
                                food["name"],
                                "weight has been updated to",
                                str(new_quantity) + " kg"
                            )
                        else:
                            print(
                                food["name"],
                                "quantity has been updated to",
                                new_quantity
                            )

                        #if a regular item is low ask if it should be added to shopping
                        key = regular_key(
                            food["name"],
                            food["price_type"]
                        )

                        if key in regular_items:

                            setting = regular_items[key]

                            if (
                                total_inventory_quantity(
                                    food["name"],
                                    food["price_type"]
                                )
                                < setting["minimum"]
                            ):

                                add_now = yes_no(
                                    food["name"]
                                    + " is running low. "
                                    + "Add it to the shopping list? (Y/N): "
                                )

                                if add_now is True:

                                    if food["price_type"] == "kg":
                                        amount_needed = round(
                                            setting["minimum"]
                                            - total_inventory_quantity(
                                                food["name"],
                                                food["price_type"]
                                            ),
                                            2
                                        )
                                    else:
                                        amount_needed = max(
                                            1,
                                            int(
                                                setting["minimum"]
                                                - total_inventory_quantity(
                                                    food["name"],
                                                    food["price_type"]
                                                )
                                            )
                                        )

                                    add_to_shopping_list(
                                        food["name"],
                                        amount_needed,
                                        setting["estimated_price"],
                                        "Low stock",
                                        food["price_type"]
                                    )

                    elif confirmed is False:
                        print("Change cancelled.")

                #deletes the selected batch
                elif action == "2":

                    confirmed = yes_no(
                        "Are you sure you want to delete "
                        + food["name"]
                        + " expiring "
                        + display_date(food["expiry"])
                        + "? (Y/N): "
                    )

                    if confirmed is True:

                        inventory.pop(item_number)

                        print(
                            food["name"],
                            "has been deleted."
                        )

                        break

                    elif confirmed is False:
                        print("Delete cancelled.")

                #fast transfer to shopping list
                elif action == "3":

                    if food["price_type"] == "kg":
                        amount = get_weight(
                            "How many kg should be added to the shopping list? "
                        )
                    else:
                        amount = get_quantity(
                            "How many should be added to the shopping list? "
                        )

                    if amount is None:
                        continue

                    add_to_shopping_list(
                        food["name"],
                        amount,
                        food["price"],
                        "Inventory transfer",
                        food["price_type"]
                    )

                elif action == "b":
                    break

                elif action == "q":
                    print("Exiting program")
                    sys.exit()

                else:
                    print("Invalid option.")

        except ValueError:
            print("Please enter a valid item number.")





#------------------------------------------------

# LUNCH / DINNER PLAN FUNCTIONS

#------------------------------------------------



#creates a message when a lunch or dinner answer changes
def add_meal_message(person, meal, coming):

    global next_meal_message_id

    if coming is True:
        text = person + " is coming home for " + meal + "."

    else:
        text = person + " is not coming home for " + meal + "."

    meal_messages.append({
        "id": next_meal_message_id,
        "person": person,
        "meal": meal,
        "text": text
    })

    next_meal_message_id += 1



#clears meal messages connected to one person without changing other messages
def clear_meal_messages_for_person(person):

    for message in meal_messages:

        if message["person"] == person:
            cleared_messages.add(("meal", message["id"]))



#clears all current meal messages without changing the permanent board
def clear_all_meal_messages():

    for message in meal_messages:
        cleared_messages.add(("meal", message["id"]))



#shows a permanent household list for lunch and dinner
#responses stay until changed, removed or reset for the next day
def meal_plan_page():

    while True:

        print("\n--- LUNCH / DINNER PLANS ---")

        #shows the household meal board
        if len(meal_responses) == 0:

            print("No household members have been added yet.")

        else:

            print(
                "\n"
                + "Name".ljust(20)
                + "Lunch".ljust(12)
                + "Dinner"
            )

            print("-" * 42)

            for name, meals in meal_responses.items():

                if meals["lunch"] is True:
                    lunch_status = "YES"

                elif meals["lunch"] is False:
                    lunch_status = "NO"

                else:
                    lunch_status = "Not set"

                if meals["dinner"] is True:
                    dinner_status = "YES"

                elif meals["dinner"] is False:
                    dinner_status = "NO"

                else:
                    dinner_status = "Not set"

                print(
                    name.ljust(20)
                    + lunch_status.ljust(12)
                    + dinner_status
                )

        print("\n1. Add / update person")
        print("2. Remove one person")
        print("3. Reset for next day")
        print("B. Back to main menu")
        print("Q. Exit")

        choice = input("\nChoose an option: ").lower()

        #adds a new person or changes an existing response
        if choice == "1":

            person = cancelable_input("Person's name: ")

            if person is None:
                continue

            person = person.strip()

            #creates a new person if they are not already on the board
            if person not in meal_responses:

                meal_responses[person] = {
                    "lunch": None,
                    "dinner": None
                }

            while True:

                print("\n---", person.upper(), "---")
                print("1. Update Lunch")
                print("2. Update Dinner")
                print("3. Update Both")
                print("B. Back")
                print("Q. Exit")

                meal_choice = input("Choose an option: ").lower()

                #changes lunch only
                if meal_choice == "1":

                    old_lunch = meal_responses[person]["lunch"]

                    lunch = yes_no(
                        "Coming home for lunch? (Y/N, B to cancel): "
                    )

                    if lunch is not None:

                        meal_responses[person]["lunch"] = lunch

                        #only creates a new message if the answer actually changed
                        if old_lunch != lunch:
                            add_meal_message(person, "lunch", lunch)

                        print(person, "lunch response updated.")

                    break

                #changes dinner only
                elif meal_choice == "2":

                    old_dinner = meal_responses[person]["dinner"]

                    dinner = yes_no(
                        "Coming home for dinner? (Y/N, B to cancel): "
                    )

                    if dinner is not None:

                        meal_responses[person]["dinner"] = dinner

                        #only creates a new message if the answer actually changed
                        if old_dinner != dinner:
                            add_meal_message(person, "dinner", dinner)

                        print(person, "dinner response updated.")

                    break

                #changes both lunch and dinner
                elif meal_choice == "3":

                    old_lunch = meal_responses[person]["lunch"]
                    old_dinner = meal_responses[person]["dinner"]

                    lunch = yes_no(
                        "Coming home for lunch? (Y/N, B to cancel): "
                    )

                    if lunch is None:
                        break

                    dinner = yes_no(
                        "Coming home for dinner? (Y/N, B to cancel): "
                    )

                    if dinner is None:
                        break

                    meal_responses[person]["lunch"] = lunch
                    meal_responses[person]["dinner"] = dinner

                    if old_lunch != lunch:
                        add_meal_message(person, "lunch", lunch)

                    if old_dinner != dinner:
                        add_meal_message(person, "dinner", dinner)

                    print(person, "meal responses updated.")
                    break

                elif meal_choice == "b":
                    break

                elif meal_choice == "q":
                    print("Exiting program")
                    sys.exit()

                else:
                    print("Invalid option.")

        #removes a person completely from the permanent meal board
        elif choice == "2":

            if len(meal_responses) == 0:

                print("There are no household members to remove.")
                continue

            names = list(meal_responses.keys())

            print("\n--- REMOVE PERSON ---")

            for number, name in enumerate(names, start=1):
                print(str(number) + ".", name)

            remove_choice = input(
                "Choose a person to remove, or B to go back: "
            )

            if remove_choice.lower() == "b":
                continue

            elif remove_choice.lower() == "q":
                print("Exiting program")
                sys.exit()

            try:

                position = int(remove_choice) - 1

                if position < 0 or position >= len(names):

                    print("Invalid person number.")
                    continue

                selected_name = names[position]

                confirmed = yes_no(
                    "Remove "
                    + selected_name
                    + " from the meal board? (Y/N): "
                )

                if confirmed is True:

                    #removes old meal messages for that person
                    #but does not create a new removal message
                    clear_meal_messages_for_person(selected_name)

                    del meal_responses[selected_name]
                    print(selected_name, "has been removed.")

                elif confirmed is False:

                    print("Remove cancelled.")

            except ValueError:

                print("Please enter a valid number.")

        #keeps household names but resets lunch and dinner for the next day
        elif choice == "3":

            if len(meal_responses) == 0:

                print("There are no meal responses to reset.")
                continue

            confirmed = yes_no(
                "Reset all lunch and dinner answers for the next day? (Y/N): "
            )

            if confirmed is True:

                for person in meal_responses:
                    meal_responses[person]["lunch"] = None
                    meal_responses[person]["dinner"] = None

                #removes the previous meal update messages
                #so yesterday's meal messages do not remain active
                clear_all_meal_messages()

                print(
                    "Meal board reset. Household names have been kept."
                )

            elif confirmed is False:

                print("Reset cancelled.")

        elif choice == "b":
            return

        elif choice == "q":
            print("Exiting program")
            sys.exit()

        else:
            print("Invalid option.")



#------------------------------------------------

# MESSAGE FUNCTIONS

#------------------------------------------------



#creates a level for expiry alerts

def food_alert_level(days_left):



    if days_left < 0:

        return "expired"



    elif days_left == 0:

        return "today"



    elif days_left <= 3:

        return "urgent"



    elif days_left <= 7:

        return "reminder"



    return None





#creates the food alert text

def food_message_text(food):



    days_left = days_until_expiry(food["expiry"])



    if days_left < 0:



        return (

            "WARNING: "

            + food["name"]

            + " has expired."

        )



    elif days_left == 0:



        return (

            "WARNING: "

            + food["name"]

            + " expires today."

        )



    elif days_left == 1:



        return (

            "URGENT: "

            + food["name"]

            + " expires in 1 day."

        )



    elif days_left <= 3:



        return (

            "URGENT: "

            + food["name"]

            + " expires in "

            + str(days_left)

            + " days."

        )



    else:



        return (

            "REMINDER: "

            + food["name"]

            + " expires in "

            + str(days_left)

            + " days."

        )





#builds the food, meal and shopping message categories
def get_message_groups():

    groups = {
        "Food Alerts": [],
        "Household / Meals": [],
        "Shopping Recommendations": []
    }

    #food expiry messages
    for food in inventory:

        days_left = days_until_expiry(food["expiry"])
        level = food_alert_level(days_left)

        if level is not None:

            key = (
                "food",
                food["id"],
                food["expiry"],
                level
            )

            if key not in cleared_messages:

                groups["Food Alerts"].append({
                    "key": key,
                    "text": food_message_text(food)
                })

    #lunch and dinner update messages
    #these can be cleared without changing the permanent meal board
    for message in meal_messages:

        key = ("meal", message["id"])

        if key not in cleared_messages:

            groups["Household / Meals"].append({
                "key": key,
                "text": message["text"]
            })

    #shopping recommendation messages
    for recommendation in shopping_recommendations():

        key = (
            "shopping",
            recommendation["key"],
            recommendation["current_quantity"],
            recommendation["minimum"]
        )

        if recommendation["price_type"] == "kg":
            current_text = (
                str(recommendation["current_quantity"])
                + " kg"
            )
            minimum_text = (
                str(recommendation["minimum"])
                + " kg"
            )
        else:
            current_text = (
                str(recommendation["current_quantity"])
                + " items"
            )
            minimum_text = (
                str(recommendation["minimum"])
                + " items"
            )

        text = (
            recommendation["name"]
            + " is low. Current amount: "
            + current_text
            + ". Minimum wanted: "
            + minimum_text
            + "."
        )

        if key not in cleared_messages:

            groups["Shopping Recommendations"].append({
                "key": key,
                "text": text
            })

    return groups



#counts every uncleared message
def message_count():

    groups = get_message_groups()

    return (
        len(groups["Food Alerts"])
        + len(groups["Household / Meals"])
        + len(groups["Shopping Recommendations"])
    )



#opens one message category

def open_message_category(category):



    while True:



        groups = get_message_groups()

        messages = groups[category]



        print("\n---", category.upper(), "---")



        if len(messages) == 0:



            print("There are currently no messages in this category.")



            input("\nPress Enter to return.")

            return



        for number, message in enumerate(messages, start=1):



            print(

                str(number) + ".",

                message["text"]

            )



        print("\nEnter a message number to clear it")

        print("C. Clear all messages in this category")

        print("B. Back")

        print("Q. Exit")



        choice = input("\nChoose an option: ").lower()



        if choice == "c":



            confirmed = yes_no(

                "Clear all messages in this category? (Y/N): "

            )



            if confirmed is True:



                for message in messages:

                    cleared_messages.add(message["key"])



                print("Category messages cleared.")



        elif choice == "b":

            return



        elif choice == "q":

            print("Exiting program")

            sys.exit()



        else:



            try:



                position = int(choice) - 1



                if position < 0 or position >= len(messages):

                    print("Invalid message number.")

                    continue



                selected = messages[position]



                confirmed = yes_no(

                    "Clear this message? (Y/N): "

                )



                if confirmed is True:



                    cleared_messages.add(

                        selected["key"]

                    )



                    print("Message cleared.")



            except ValueError:



                print("Invalid option.")





#main messages page with three categories
def view_messages():

    while True:

        groups = get_message_groups()

        print("\n--- MESSAGES ---")
        print(
            "1. Food Alerts ("
            + str(len(groups["Food Alerts"]))
            + ")"
        )
        print(
            "2. Household / Meals ("
            + str(len(groups["Household / Meals"]))
            + ")"
        )
        print(
            "3. Shopping Recommendations ("
            + str(len(groups["Shopping Recommendations"]))
            + ")"
        )
        print("C. Clear all current messages")
        print("B. Back to main menu")
        print("Q. Exit")

        choice = input("\nChoose an option: ").lower()

        if choice == "1":

            open_message_category("Food Alerts")

        elif choice == "2":

            open_message_category("Household / Meals")

        elif choice == "3":

            open_message_category(
                "Shopping Recommendations"
            )

        elif choice == "c":

            all_messages = (
                groups["Food Alerts"]
                + groups["Household / Meals"]
                + groups["Shopping Recommendations"]
            )

            if len(all_messages) == 0:

                print("There are no messages to clear.")

            else:

                confirmed = yes_no(
                    "Clear all current messages? (Y/N): "
                )

                if confirmed is True:

                    for message in all_messages:
                        cleared_messages.add(
                            message["key"]
                        )

                    print("All current messages cleared.")

        elif choice == "b":

            return

        elif choice == "q":

            print("Exiting program")
            sys.exit()

        else:

            print("Invalid option.")



#------------------------------------------------

# BUDGET FUNCTIONS

#------------------------------------------------



#budget tracking page

def budget_page():



    while True:



        remaining = budget["limit"] - budget["spent"]

        estimated_shopping = shopping_list_total()



        print("\n--- GROCERY BUDGET ---")



        if budget["limit"] == 0:

            print("Weekly budget: Not set")

        else:

            print(

                "Weekly budget: $"

                + format(budget["limit"], ".2f")

            )



        print(

            "Amount spent: $"

            + format(budget["spent"], ".2f")

        )



        if budget["limit"] > 0:



            print(

                "Remaining: $"

                + format(remaining, ".2f")

            )



        print(

            "Shopping list estimated cost: $"

            + format(estimated_shopping, ".2f")

        )



        if budget["limit"] > 0:



            projected = (

                budget["spent"]

                + estimated_shopping

            )



            print(

                "Projected spending after shopping list: $"

                + format(projected, ".2f")

            )



            if projected > budget["limit"]:



                print(

                    "WARNING: Shopping list may put you $"

                    + format(

                        projected - budget["limit"],

                        ".2f"

                    )

                    + " over budget."

                )



        print("\n1. Set weekly budget")

        print("2. Add manual grocery spending")

        print("3. Reset weekly spending")

        print("B. Back to main menu")

        print("Q. Exit")



        choice = input("\nChoose an option: ").lower()



        if choice == "1":



            new_budget = get_price(

                "Enter weekly grocery budget: $"

            )



            if new_budget is not None:



                confirmed = yes_no(

                    "Set weekly budget to $"

                    + format(new_budget, ".2f")

                    + "? (Y/N): "

                )



                if confirmed is True:

                    budget["limit"] = new_budget

                    print("Weekly budget updated.")



        elif choice == "2":



            amount = get_price(

                "Enter grocery spending amount: $"

            )



            if amount is not None:



                confirmed = yes_no(

                    "Add $"

                    + format(amount, ".2f")

                    + " to spending? (Y/N): "

                )



                if confirmed is True:

                    budget["spent"] += amount

                    print("Spending updated.")



        elif choice == "3":



            confirmed = yes_no(

                "Reset weekly spending to $0.00? (Y/N): "

            )



            if confirmed is True:

                budget["spent"] = 0.0

                print("Weekly spending reset.")



        elif choice == "b":



            return



        elif choice == "q":



            print("Exiting program")

            sys.exit()



        else:



            print("Invalid option.")






#------------------------------------------------
# TKINTER VIEW INVENTORY
#------------------------------------------------

#opens the inventory inside a tkinter window
def open_inventory():

    inventory_window = tk.Toplevel(root)
    inventory_window.title("View Inventory")
    inventory_window.geometry("950x520")
    inventory_window.minsize(850, 450)

    title_label = tk.Label(
        inventory_window,
        text="VIEW INVENTORY",
        font=("Arial", 20, "bold")
    )
    title_label.pack(pady=(20, 10))

    #shows a message if the inventory is empty
    if len(inventory) == 0:

        empty_label = tk.Label(
            inventory_window,
            text="Your inventory is currently empty.",
            font=("Arial", 12)
        )
        empty_label.pack(pady=60)

    else:

        table_frame = tk.Frame(inventory_window)
        table_frame.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True
        )

        #columns shown in the inventory table
        columns = (
            "category",
            "name",
            "amount",
            "price",
            "expiry",
            "status"
        )

        inventory_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        inventory_table.heading("category", text="Category")
        inventory_table.heading("name", text="Food")
        inventory_table.heading("amount", text="Quantity / Weight")
        inventory_table.heading("price", text="Price")
        inventory_table.heading("expiry", text="Expiry")
        inventory_table.heading("status", text="Status")

        inventory_table.column("category", width=130, anchor="center")
        inventory_table.column("name", width=150, anchor="center")
        inventory_table.column("amount", width=130, anchor="center")
        inventory_table.column("price", width=135, anchor="center")
        inventory_table.column("expiry", width=110, anchor="center")
        inventory_table.column("status", width=210, anchor="center")

        #adds every saved food item to the tkinter table
        for food in inventory:

            #shows kg items differently from items priced individually
            if food.get("price_type", "item") == "kg":

                amount_text = (
                    format(food["quantity"], ".2f").rstrip("0").rstrip(".")
                    + " kg"
                )

                price_text = (
                    "$"
                    + format(food["price"], ".2f")
                    + " / kg"
                )

            else:

                amount_text = str(food["quantity"])

                price_text = (
                    "$"
                    + format(food["price"], ".2f")
                    + " each"
                )

            inventory_table.insert(
                "",
                "end",
                values=(
                    food["category"],
                    food["name"],
                    amount_text,
                    price_text,
                    display_date(food["expiry"]),
                    check_expiry(food["expiry"])
                )
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=inventory_table.yview
        )

        inventory_table.configure(
            yscrollcommand=scrollbar.set
        )

        inventory_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

    back_button = tk.Button(
        inventory_window,
        text="Back",
        font=("Arial", 11),
        width=16,
        command=inventory_window.destroy
    )
    back_button.pack(pady=(10, 20))


#------------------------------------------------
# TEMPORARY TERMINAL BUTTON SUPPORT
#------------------------------------------------

#the other pages still use the terminal for now
#this lets the tkinter main menu open the existing functions
#until each page is converted into tkinter
def run_terminal_page(page_function, page_name):

    messagebox.showinfo(
        page_name,
        page_name
        + " is still using the VS Code terminal for now.\n\n"
        + "Follow the prompts in the terminal, then the main window will return."
    )

    root.withdraw()

    try:
        page_function()
    finally:
        root.deiconify()
        root.lift()
        update_message_button()


#updates the message button so its number stays current
def update_message_button():

    if "messages_button" in globals():
        messages_button.config(
            text="Messages (" + str(message_count()) + ")"
        )


#asks before closing the whole program
def exit_program():

    confirmed = messagebox.askyesno(
        "Exit Smart Pantry",
        "Are you sure you want to exit?"
    )

    if confirmed:
        root.destroy()


#------------------------------------------------
# TKINTER MAIN WINDOW
#------------------------------------------------

root = tk.Tk()
root.title("Smart Pantry")
root.geometry("520x700")
root.resizable(False, False)

#uses the same confirmation when the window X button is pressed
root.protocol("WM_DELETE_WINDOW", exit_program)

#page title
title_label = tk.Label(
    root,
    text="SMART PANTRY",
    font=("Arial", 24, "bold")
)
title_label.pack(pady=(30, 5))

subtitle_label = tk.Label(
    root,
    text="Household Food Management",
    font=("Arial", 12)
)
subtitle_label.pack(pady=(0, 25))

#holds all of the menu buttons
menu_frame = tk.Frame(root)
menu_frame.pack(
    padx=55,
    fill="both",
    expand=True
)

#view inventory is now a full tkinter page
view_inventory_button = tk.Button(
    menu_frame,
    text="View Inventory",
    font=("Arial", 12),
    height=2,
    command=open_inventory
)
view_inventory_button.pack(fill="x", pady=5)

#the remaining pages still use their original terminal functions
add_item_button = tk.Button(
    menu_frame,
    text="Add Item",
    font=("Arial", 12),
    height=2,
    command=lambda: run_terminal_page(add_item, "Add Item")
)
add_item_button.pack(fill="x", pady=5)

update_items_button = tk.Button(
    menu_frame,
    text="Update Items",
    font=("Arial", 12),
    height=2,
    command=lambda: run_terminal_page(update_item, "Update Items")
)
update_items_button.pack(fill="x", pady=5)

view_shopping_button = tk.Button(
    menu_frame,
    text="View Shopping List",
    font=("Arial", 12),
    height=2,
    command=lambda: run_terminal_page(
        view_shopping_list,
        "View Shopping List"
    )
)
view_shopping_button.pack(fill="x", pady=5)

manage_shopping_button = tk.Button(
    menu_frame,
    text="Manage Shopping List",
    font=("Arial", 12),
    height=2,
    command=lambda: run_terminal_page(
        shopping_list_page,
        "Manage Shopping List"
    )
)
manage_shopping_button.pack(fill="x", pady=5)

meal_plan_button = tk.Button(
    menu_frame,
    text="Lunch / Dinner Plans",
    font=("Arial", 12),
    height=2,
    command=lambda: run_terminal_page(
        meal_plan_page,
        "Lunch / Dinner Plans"
    )
)
meal_plan_button.pack(fill="x", pady=5)

messages_button = tk.Button(
    menu_frame,
    text="Messages (" + str(message_count()) + ")",
    font=("Arial", 12),
    height=2,
    command=lambda: run_terminal_page(
        view_messages,
        "Messages"
    )
)
messages_button.pack(fill="x", pady=5)

budget_button = tk.Button(
    menu_frame,
    text="Budget",
    font=("Arial", 12),
    height=2,
    command=lambda: run_terminal_page(
        budget_page,
        "Budget"
    )
)
budget_button.pack(fill="x", pady=5)

exit_button = tk.Button(
    menu_frame,
    text="Exit",
    font=("Arial", 12),
    height=2,
    command=exit_program
)
exit_button.pack(fill="x", pady=(20, 5))

#starts the tkinter graphical interface
root.mainloop()
