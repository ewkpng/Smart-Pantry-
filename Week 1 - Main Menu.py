#setting up display page and what possible actions can be taken

#import sys just makes it possible to run sys exit to exit the program
import sys


#creating the view items page
def view_items():

    #setting up options
    print("\n--- VIEW ITEMS ---")
    print("You selected View Items")

    # allows the user to either go back to the main menu or exit the program
    while True:

        choice = input("\nEnter B to go back to menu or Q to exit: ").lower()

        # if b is entered it returns back to the main menu
        if choice == "b":
            return

        # if q is entered the whole code is shutoff and prints an exiting message
        elif choice == "q":
            print("Exiting program")
            sys.exit()

        else:
            print("Invalid option")


#creating the add item page
def add_item():

    print("\n--- ADD ITEM ---")
    print("You selected Add Item")

    # allows the user to either go back to the main menu or exit the program
    while True:

        choice = input("\nEnter B to go back to menu or Q to exit: ").lower()

        # if b is entered it returns back to the main menu
        if choice == "b":
            return

        # if q is entered the whole code is shutoff and prints an exiting message
        elif choice == "q":
            print("Exiting program")
            sys.exit()

        else:
            print("Invalid option")


#Creating the main page
while True:

    #creating the main page and having 3 options of what can be done
    print("\nMY PROGRAM")
    print("1. View items")
    print("2. Add item")
    print("3. Exit")

    #setting up the inputs
    choice = input("Choose an option: ")

    # if 1 is entered it will lead to viewing items
    if choice == "1":
        view_items()

    # if 2 is entered will lead to add item
    elif choice == "2":
        add_item()

    #if 3 is entered the whole code is shutoff and print an exiting message
    elif choice == "3":
        print("Exiting program")
        sys.exit()

    # ensures if an invalid number is sent it provides an invalid option
    # and resets to the main menu instead of breaking
    else:
        print("Invalid option")