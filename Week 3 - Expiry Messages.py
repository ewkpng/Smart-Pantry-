#setting up display page and what possible actions can be taken

#import sys just makes it possible to run sys exit to exit the program
import sys

#Creating in app date tracker
from datetime import date


#creating inventory
inventory = []


#Creating the automatic expiry date system
def get_expiry_date():

    while True:

        #only asks the user for the day and month
        expiry_input = input("Expiry date (DD/MM): ")

        #allows the user to go back to the main menu
        if expiry_input.lower() == "b":
            return "back"

        #allows the user to exit the program
        elif expiry_input.lower() == "q":
            print("Exiting program")
            sys.exit()

        try:

            #splits the date into the day and month
            day, month = map(int, expiry_input.split("/"))

            #gets todays date
            today = date.today()

            #checks the current year and future years
            for year in range(today.year, today.year + 5):

                try:

                    expiry = date(year, month, day)

                    #uses the first date that has not already passed
                    if expiry >= today:
                        return expiry.isoformat()

                except ValueError:
                    continue

            print("Invalid date")

        except ValueError:
            print("Invalid date. Please enter it as DD/MM")


#checks how long there is until an item expires
def check_expiry(expiry):

    #changes the saved expiry back into a date
    expiry_date = date.fromisoformat(expiry)

    #gets todays date
    today = date.today()

    #calculates how many days are left
    days_left = (expiry_date - today).days

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


#changes the saved date into a nicer looking date
def display_date(expiry):

    expiry_date = date.fromisoformat(expiry)

    return expiry_date.strftime("%d/%m/%Y")


#counts how many expiry messages there currently are
def message_count():

    count = 0

    for food in inventory:

        expiry_date = date.fromisoformat(food["expiry"])

        days_left = (expiry_date - date.today()).days

        #anything expiring within 7 days creates a message
        if days_left <= 7:
            count += 1

    return count


#creating the view items page
def view_items():

    print("\n--- VIEW ITEMS ---")

    #checks if the inventory is empty
    if len(inventory) == 0:

        print("Your inventory is currently empty.")

    else:

        #goes through each food item in the inventory
        for number, food in enumerate(inventory, start=1):

            print("\nItem", number)

            print("Food name:", food["name"])

            print("Quantity:", food["quantity"])

            print("Price: $" + food["price"])

            print("Expiry date:", display_date(food["expiry"]))

            #shows the expiry status
            print("Status:", check_expiry(food["expiry"]))


    #allows the user to go back to the menu or exit
    while True:

        choice = input("\nEnter B to go back to menu or Q to exit: ").lower()

        if choice == "b":

            return

        elif choice == "q":

            print("Exiting program")

            sys.exit()

        else:

            print("Invalid option")


#creating the add item page
def add_item():

    print("\n--- ADD ITEM ---")

    while True:

        choice = input(
            "\nEnter A to add an item, B to go back, or Q to exit: "
        ).upper()

        #if a is entered the user can add a food item
        if choice == "A":

            #asks the user to enter the food name
            name = input("Food name: ")

            #asks the user to enter the quantity
            quantity = input("Quantity: ")

            #asks the user to enter the price
            price = input("Price: $")

            #gets the expiry date using the automatic date tracker
            expiry = get_expiry_date()

            #returns to the main menu if b was entered
            if expiry == "back":
                return


            #stores all the information about one food item together
            food = {

                "name": name,

                "quantity": quantity,

                "price": price,

                "expiry": expiry

            }


            #adds the food item into the inventory
            inventory.append(food)


            #confirms that the item has been added
            print(name, "has been added to the inventory")


        #if b is entered it returns back to the main menu
        elif choice == "B":

            return


        #if q is entered the whole program is closed
        elif choice == "Q":

            print("Exiting program")

            sys.exit()


        #anything else is invalid
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


        #only displays the names of the food items
        for number, food in enumerate(inventory, start=1):

            print(number, food["name"])


        print("\nB. Back to menu")
        print("Q. Exit program")

        choice = input("\nSelect an item: ")


        #returns to main menu
        if choice.lower() == "b":

            return


        #exits the program
        elif choice.lower() == "q":

            print("Exiting program")

            sys.exit()


        try:

            #changes the number selected into the correct inventory position
            item_number = int(choice) - 1


            #checks if the selected item actually exists
            if item_number < 0 or item_number >= len(inventory):

                print("Invalid item number")

                continue


            #gets the selected food
            food = inventory[item_number]


            print("\n---", food["name"], "---")

            print("Current quantity:", food["quantity"])

            print("\n1. Update quantity")

            print("2. Delete item")

            print("B. Back")


            action = input("Choose an option: ")


            #allows the quantity to be changed
            if action == "1":

                new_quantity = input("Enter new quantity: ")

                food["quantity"] = new_quantity

                print(
                    food["name"],
                    "quantity has been updated to",
                    new_quantity
                )


            #allows the item to be deleted
            elif action == "2":

                confirm = input(
                    "Are you sure you want to delete "
                    + food["name"]
                    + "? (Y/N): "
                ).lower()


                if confirm == "y":

                    inventory.pop(item_number)

                    print(food["name"], "has been deleted")


            #goes back to the item list
            elif action.lower() == "b":

                continue


            else:

                print("Invalid option")


        except ValueError:

            print("Please enter a valid item number")


#creating the messages page
def view_messages():

    print("\n--- MESSAGES ---")

    message_found = False


    #checks every item in the inventory
    for food in inventory:

        expiry_date = date.fromisoformat(food["expiry"])

        days_left = (expiry_date - date.today()).days


        #creates messages for expired food
        if days_left < 0:

            print(
                "\nWARNING:",
                food["name"],
                "has expired"
            )

            message_found = True


        #creates a message if the food expires today
        elif days_left == 0:

            print(
                "\nWARNING:",
                food["name"],
                "expires today"
            )

            message_found = True


        #creates a message if there are 3 days or less
        elif days_left <= 3:

            print(
                "\nURGENT:",
                food["name"],
                "expires in",
                days_left,
                "day(s)"
            )

            message_found = True


        #creates a message if the food expires within 7 days
        elif days_left <= 7:

            print(
                "\nREMINDER:",
                food["name"],
                "expires in",
                days_left,
                "days"
            )

            message_found = True


    #if there are no expiry messages
    if message_found == False:

        print("You currently have no expiry messages.")


    #allows the user to return to the menu or exit
    while True:

        choice = input("\nEnter B to go back to menu or Q to exit: ").lower()

        if choice == "b":

            return

        elif choice == "q":

            print("Exiting program")

            sys.exit()

        else:

            print("Invalid option")


#Creating the main page
while True:

    #creating the main page and having options of what can be done
    print("\nSMART PANTRY")

    print("1. View items")

    print("2. Add item")

    print("3. Update items")

    #shows how many expiry messages are waiting
    print("4. Messages (" + str(message_count()) + ")")

    print("5. Exit")


    #setting up the inputs
    choice = input("Choose an option: ")


    # if 1 is entered it will lead to viewing items
    if choice == "1":

        view_items()


    # if 2 is entered will lead to add item
    elif choice == "2":

        add_item()


    #if 3 is entered will lead to a new page to edit the item
    elif choice == "3":

        update_item()


    #if 4 is entered it will show expiry messages
    elif choice == "4":

        view_messages()


    #if 5 is entered the whole code is shutoff and print an exiting message
    elif choice == "5":

        print("Exiting program")

        sys.exit()


    # ensures if an invalid number is sent it provides an invalid option
    # and resets to the main menu instead of breaking
    else:

        print("Invalid option")