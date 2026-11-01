#setting up display page and what possible actions can be taken



#import sys just makes it possible to run sys exit to exit the program

import sys



#Creating in app date tracker

from datetime import date





#creating inventory

inventory = []



#stores messages that the user has cleared

cleared_messages = set()



#creates a different id for every item added

#this allows multiple groups of the same food to exist

next_item_id = 1





#asks for the food name

def get_food_name(prompt="Food name: "):



    while True:



        name = input(prompt)



        #allows the user to go back

        if name.lower() == "b":

            return None



        #allows the user to exit

        elif name.lower() == "q":

            print("Exiting program")

            sys.exit()



        #stops a blank food name being entered

        elif name.strip() == "":

            print("Food name cannot be empty.")



        else:

            return name





#asks for the quantity and makes sure it is a number

def get_quantity(prompt="Quantity: "):



    while True:



        quantity = input(prompt)



        #allows the user to go back

        if quantity.lower() == "b":

            return None



        #allows the user to exit

        elif quantity.lower() == "q":

            print("Exiting program")

            sys.exit()



        try:



            quantity = int(quantity)



            #stops negative quantities

            if quantity < 0:

                print("Quantity cannot be negative.")



            else:

                return quantity



        except ValueError:



            print("Please enter a number for the quantity.")





#asks for the price and makes sure it is a number

def get_price(prompt="Price: $"):



    while True:



        price = input(prompt)



        #allows the user to go back

        if price.lower() == "b":

            return None



        #allows the user to exit

        elif price.lower() == "q":

            print("Exiting program")

            sys.exit()



        try:



            price = float(price)



            #stops negative prices

            if price < 0:

                print("Price cannot be negative.")



            else:

                return price



        except ValueError:



            print("Please enter a valid price.")





#Creating the expiry date system

#the user can enter DD/MM or DD/MM/YYYY

def get_expiry_date():



    while True:



        expiry_input = input(

            "Expiry date (DD/MM or DD/MM/YYYY): "

        )



        #allows the user to go back

        if expiry_input.lower() == "b":

            return None



        #allows the user to exit the program

        elif expiry_input.lower() == "q":

            print("Exiting program")

            sys.exit()



        try:



            #splits the date using /

            parts = expiry_input.split("/")



            #if only day and month are entered

            if len(parts) == 2:



                day = int(parts[0])

                month = int(parts[1])



                today = date.today()



                #checks future years until it finds

                #the next matching date

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





#works out how many days are left

def days_until_expiry(expiry):



    expiry_date = date.fromisoformat(expiry)



    today = date.today()



    return (expiry_date - today).days





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





#creates a unique message key for each food batch

def message_key(food):



    return (food["id"], food["expiry"])





#finds all expiry messages that have not been cleared

def current_messages():



    messages = []



    for food in inventory:



        days_left = days_until_expiry(food["expiry"])



        #creates an expiry message for anything within 7 days

        if days_left <= 7:



            #checks that the message has not been cleared

            if message_key(food) not in cleared_messages:



                messages.append(food)



    return messages





#counts how many unread expiry messages there are

def message_count():



    return len(current_messages())





#creating the view items page

def view_items():



    print("\n--- VIEW ITEMS ---")



    #checks if the inventory is empty

    if len(inventory) == 0:



        print("Your inventory is currently empty.")



    else:



        #goes through each food item in the inventory

        #the same food can appear more than once with different expiry dates

        for number, food in enumerate(inventory, start=1):



            print("\nItem", number)



            print("Food name:", food["name"])



            print("Quantity:", food["quantity"])



            print("Price: $" + format(food["price"], ".2f"))



            print(

                "Expiry date:",

                display_date(food["expiry"])

            )



            print(

                "Status:",

                check_expiry(food["expiry"])

            )





    #allows the user to go back to the menu or exit

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





#creating the add item page

def add_item():



    global next_item_id



    print("\n--- ADD ITEM ---")



    print("Enter B at any time to cancel and go back.")

    print("Enter Q at any time to exit Smart Pantry.")





    #asks the user for all food information

    name = get_food_name()



    if name is None:

        return





    quantity = get_quantity()



    if quantity is None:

        return





    price = get_price()



    if price is None:

        return





    expiry = get_expiry_date()



    if expiry is None:

        return





    #allows the item to be checked before it is added

    while True:



        print("\n--- CHECK ITEM ---")



        print("Food name:", name)



        print("Quantity:", quantity)



        print("Price: $" + format(price, ".2f"))



        print("Expiry:", display_date(expiry))





        print("\n1. Confirm and add item")



        print("2. Edit item information")



        print("B. Cancel item")



        print("Q. Exit program")





        confirm = input(

            "\nIs this item finished? "

        ).lower()





        #confirms and adds the item

        if confirm == "1":



            #each item gets its own id

            #this allows two Milk items to have different expiry dates

            food = {



                "id": next_item_id,



                "name": name,



                "quantity": quantity,



                "price": price,



                "expiry": expiry



            }





            inventory.append(food)



            next_item_id += 1





            print(

                "\n",

                name,

                "has been added to the inventory."

            )





            return





        #allows incorrect information to be changed

        elif confirm == "2":



            while True:



                print("\n--- EDIT ITEM ---")



                print("1. Food name")



                print("2. Quantity")



                print("3. Price")



                print("4. Expiry date")



                print("B. Return to check item")



                print("Q. Exit program")





                edit = input(

                    "What would you like to edit? "

                ).lower()





                #changes the food name

                if edit == "1":



                    new_name = get_food_name(

                        "New food name: "

                    )



                    if new_name is not None:



                        name = new_name





                #changes the quantity

                elif edit == "2":



                    new_quantity = get_quantity(

                        "New quantity: "

                    )



                    if new_quantity is not None:



                        quantity = new_quantity





                #changes the price

                elif edit == "3":



                    new_price = get_price(

                        "New price: $"

                    )



                    if new_price is not None:



                        price = new_price





                #changes the expiry date

                elif edit == "4":



                    new_expiry = get_expiry_date()



                    if new_expiry is not None:



                        expiry = new_expiry





                #returns to the item confirmation page

                elif edit == "b":



                    break





                #exits the whole program

                elif edit == "q":



                    print("Exiting program")



                    sys.exit()





                else:



                    print("Invalid option")





        #cancels the item completely

        elif confirm == "b":



            print("Item was not added.")



            return





        #exits Smart Pantry

        elif confirm == "q":



            print("Exiting program")



            sys.exit()





        else:



            print("Invalid option")





#Creating update items page

def update_item():



    while True:



        print("\n--- UPDATE ITEMS ---")





        #checks if the inventory is empty

        if len(inventory) == 0:



            print("Your inventory is currently empty.")



            return





        #shows the food name and expiry date

        #this makes different batches of the same food easy to identify

        for number, food in enumerate(inventory, start=1):



            print(

                str(number) + ".",

                food["name"],

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





            #checks that the selected number exists

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



                print(

                    "Current quantity:",

                    food["quantity"]

                )





                print("\n1. Update quantity")



                print("2. Delete item")



                print("B. Back to item list")



                print("Q. Exit program")





                action = input(

                    "\nChoose an option: "

                ).lower()





                #updates the quantity

                if action == "1":



                    new_quantity = get_quantity(

                        "Enter new quantity: "

                    )





                    if new_quantity is None:



                        continue





                    #confirmation before changing quantity

                    confirm_change = input(

                        "Confirm quantity change from "

                        + str(food["quantity"])

                        + " to "

                        + str(new_quantity)

                        + "? (Y/N): "

                    ).lower()





                    if confirm_change == "y":



                        food["quantity"] = new_quantity



                        print(

                            food["name"],

                            "quantity has been updated to",

                            new_quantity

                        )





                    elif confirm_change == "n":



                        print(

                            "Quantity change cancelled."

                        )





                    else:



                        print(

                            "Invalid option. "

                            "Quantity was not changed."

                        )





                #deletes the item

                elif action == "2":



                    #asks for confirmation before deleting

                    confirm_delete = input(

                        "Are you sure you want to delete "

                        + food["name"]

                        + " expiring "

                        + display_date(food["expiry"])

                        + "? (Y/N): "

                    ).lower()





                    if confirm_delete == "y":



                        #removes any cleared message connected to the item

                        cleared_messages.discard(

                            message_key(food)

                        )



                        inventory.pop(item_number)



                        print(

                            food["name"],

                            "has been deleted."

                        )



                        break





                    elif confirm_delete == "n":



                        print(

                            "Delete cancelled."

                        )





                    else:



                        print("Invalid option.")





                #returns to item list

                elif action == "b":



                    break





                #exits program

                elif action == "q":



                    print("Exiting program")



                    sys.exit()





                else:



                    print("Invalid option")





        except ValueError:



            print(

                "Please enter a valid item number."

            )





#creates the message shown for each food

def create_message(food):



    days_left = days_until_expiry(food["expiry"])





    if days_left < 0:



        return (

            "WARNING: "

            + food["name"]

            + " has expired"

        )





    elif days_left == 0:



        return (

            "WARNING: "

            + food["name"]

            + " expires today"

        )





    elif days_left == 1:



        return (

            "URGENT: "

            + food["name"]

            + " expires in 1 day"

        )





    elif days_left <= 3:



        return (

            "URGENT: "

            + food["name"]

            + " expires in "

            + str(days_left)

            + " days"

        )





    else:



        return (

            "REMINDER: "

            + food["name"]

            + " expires in "

            + str(days_left)

            + " days"

        )





#creating the messages page

def view_messages():



    while True:



        print("\n--- MESSAGES ---")





        messages = current_messages()





        #checks whether there are any active messages

        if len(messages) == 0:



            print(

                "You currently have no expiry messages."

            )





            choice = input(

                "\nEnter B to go back or Q to exit: "

            ).lower()





            if choice == "b":



                return





            elif choice == "q":



                print("Exiting program")



                sys.exit()





            else:



                print("Invalid option")





        else:



            #numbers each message

            for number, food in enumerate(

                messages,

start=1

            ):



                print(

                    "\n" + str(number) + ".",

                    create_message(food)

                )





            print(

                "\nEnter a message number to clear that message"

            )



            print("C. Clear all messages")



            print("B. Back to menu")



            print("Q. Exit program")





            choice = input(

                "\nChoose an option: "

            ).lower()





            #returns to main menu

            if choice == "b":



                return





            #exits Smart Pantry

            elif choice == "q":



                print("Exiting program")



                sys.exit()





            #clears every current message

            elif choice == "c":



                confirm_clear = input(

                    "Clear all current messages? (Y/N): "

                ).lower()





                if confirm_clear == "y":



                    for food in messages:



                        cleared_messages.add(

                            message_key(food)

                        )





                    print(

                        "All current messages have been cleared."

                    )





                else:



                    print(

                        "Messages were not cleared."

                    )





            else:



                try:



                    message_number = int(choice) - 1





                    #checks if the chosen message exists

                    if (

                        message_number < 0

                        or

                        message_number >= len(messages)

                    ):



                        print(

                            "Invalid message number."

                        )



                        continue





                    selected_food = messages[

                        message_number

                    ]





                    #asks before clearing one message

                    confirm_clear = input(

                        "Clear the message for "

                        + selected_food["name"]

                        + "? (Y/N): "

                    ).lower()





                    if confirm_clear == "y":



                        cleared_messages.add(

                            message_key(selected_food)

                        )



                        print(

                            "Message cleared."

                        )





                    else:



                        print(

                            "Message was not cleared."

                        )





                except ValueError:



                    print("Invalid option.")





#Creating the main page

while True:



    print("\nSMART PANTRY")



    print("1. View items")



    print("2. Add item")



    print("3. Update items")



    #shows the number of messages that have not been cleared

    print(

        "4. Messages ("

        + str(message_count())

        + ")"

    )



    print("5. Exit")





    choice = input("Choose an option: ")





    #leads to viewing items

    if choice == "1":



        view_items()





    #leads to adding an item

    elif choice == "2":



        add_item()





    #leads to updating an item

    elif choice == "3":



        update_item()





    #leads to expiry messages

    elif choice == "4":



        view_messages()





    #exits the program

    elif choice == "5":



        print("Exiting program")



        sys.exit()





    #handles invalid menu choices

    else:



        print("Invalid option")