# Smart Pantry
# Basic Tkinter version of the full project

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import date


#------------------------------------------------
# DATA
#------------------------------------------------

#stores every food batch
inventory = []

#stores shopping list items
shopping_list = []

#stores foods that should always stay stocked
regular_items = {}

#stores permanent lunch and dinner answers
meal_responses = {}

#stores meal update messages
meal_messages = []

#stores messages the user has cleared
cleared_messages = set()

#weekly budget information
budget = {
    "limit": 0.0,
    "spent": 0.0
}

#unique ids
next_item_id = 1
next_meal_message_id = 1

#tkinter globals
root = None
messages_button = None


#------------------------------------------------
# BASIC HELPERS
#------------------------------------------------

def normalise_name(name):
    return name.strip().lower()


def regular_key(name, price_type):
    return normalise_name(name) + "|" + price_type


def amount_text(amount, price_type):
    if price_type == "kg":
        return format(amount, ".2f").rstrip("0").rstrip(".") + " kg"
    return str(int(amount)) + " items"


def price_text(price, price_type):
    if price_type == "kg":
        return "$" + format(price, ".2f") + " / kg"
    return "$" + format(price, ".2f") + " each"


def find_food_by_id(food_id):
    for food in inventory:
        if food["id"] == food_id:
            return food
    return None


def update_message_button():
    if messages_button is not None:
        messages_button.config(
            text="Messages (" + str(message_count()) + ")"
        )


#------------------------------------------------
# DATE FUNCTIONS
#------------------------------------------------

def parse_expiry_date(expiry_input):
    parts = expiry_input.strip().split("/")

    if len(parts) == 2:
        day = int(parts[0])
        month = int(parts[1])
        today = date.today()

        #finds the next matching date that has not already passed
        for year in range(today.year, today.year + 5):
            try:
                expiry = date(year, month, day)
                if expiry >= today:
                    return expiry.isoformat()
            except ValueError:
                continue

        raise ValueError

    elif len(parts) == 3:
        day = int(parts[0])
        month = int(parts[1])
        year = int(parts[2])
        expiry = date(year, month, day)
        return expiry.isoformat()

    raise ValueError


def ask_expiry(parent=None, current=None):
    while True:
        prompt = "Expiry date (DD/MM or DD/MM/YYYY):"

        if current is not None:
            prompt += "\nCurrent: " + display_date(current)

        entered = simpledialog.askstring(
            "Expiry Date",
            prompt,
            parent=parent
        )

        if entered is None:
            return None

        try:
            return parse_expiry_date(entered)
        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Please enter a valid date such as 15/10 or 15/10/2026.",
                parent=parent
            )


def display_date(expiry):
    expiry_date = date.fromisoformat(expiry)
    return expiry_date.strftime("%d/%m/%Y")


def days_until_expiry(expiry):
    expiry_date = date.fromisoformat(expiry)
    return (expiry_date - date.today()).days


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
# SIMPLE TKINTER INPUT FUNCTIONS
#------------------------------------------------

def ask_food_name(parent=None, title="Food Name", current=None):
    while True:
        prompt = "Enter the food name:"

        if current:
            prompt += "\nCurrent: " + current

        name = simpledialog.askstring(title, prompt, parent=parent)

        if name is None:
            return None

        name = name.strip()

        if name == "":
            messagebox.showerror(
                "Invalid Name",
                "Food name cannot be empty.",
                parent=parent
            )
        else:
            return name


def ask_price_type(parent=None, current=None):
    while True:
        prompt = (
            "Enter 1 for price per item\n"
            "Enter 2 for price per kilogram"
        )

        if current is not None:
            prompt += "\n\nCurrent: " + (
                "Per kilogram" if current == "kg" else "Per item"
            )

        choice = simpledialog.askstring(
            "Pricing Type",
            prompt,
            parent=parent
        )

        if choice is None:
            return None

        choice = choice.strip().lower()

        if choice in ("1", "item", "per item"):
            return "item"
        elif choice in ("2", "kg", "kilogram", "per kilogram"):
            return "kg"
        else:
            messagebox.showerror(
                "Invalid Option",
                "Please enter 1 or 2.",
                parent=parent
            )


def ask_amount(price_type, parent=None, current=None, title="Amount"):
    if price_type == "kg":
        prompt = "Enter the weight in kilograms:"
        if current is not None:
            prompt += "\nCurrent: " + amount_text(current, "kg")

        return simpledialog.askfloat(
            title,
            prompt,
            minvalue=0,
            parent=parent
        )

    prompt = "Enter the quantity:"
    if current is not None:
        prompt += "\nCurrent: " + str(int(current))

    return simpledialog.askinteger(
        title,
        prompt,
        minvalue=0,
        parent=parent
    )


def ask_price(price_type, parent=None, current=None):
    if price_type == "kg":
        prompt = "Enter the price per kilogram: $"
    else:
        prompt = "Enter the price per item: $"

    if current is not None:
        prompt += "\nCurrent: $" + format(current, ".2f")

    return simpledialog.askfloat(
        "Price",
        prompt,
        minvalue=0,
        parent=parent
    )


def ask_category(parent=None, current=None):
    categories = {
        "1": "Fridge / Fresh",
        "2": "Pantry",
        "3": "Frozen"
    }

    while True:
        prompt = (
            "1. Fridge / Fresh\n"
            "2. Pantry\n"
            "3. Frozen"
        )

        if current is not None:
            prompt += "\n\nCurrent: " + current

        choice = simpledialog.askstring(
            "Food Category",
            prompt,
            parent=parent
        )

        if choice is None:
            return None

        choice = choice.strip()

        if choice in categories:
            return categories[choice]

        messagebox.showerror(
            "Invalid Category",
            "Please enter 1, 2 or 3.",
            parent=parent
        )


def ask_regular_setting(name, price, category, price_type, parent=None):
    key = regular_key(name, price_type)

    #uses the existing regular setting when the food is already registered
    if key in regular_items:
        setting = regular_items[key]
        return True, setting["minimum"]

    regular = messagebox.askyesno(
        "Regular Item",
        "Should " + name + " be kept regularly stocked?",
        parent=parent
    )

    if regular is False:
        return False, 0

    minimum = ask_amount(
        price_type,
        parent=parent,
        title="Minimum Stock"
    )

    if minimum is None:
        return None, None

    return True, minimum


#------------------------------------------------
# INVENTORY / REGULAR ITEM LOGIC
#------------------------------------------------

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


def shopping_recommendations():
    recommendations = []

    for key, setting in regular_items.items():
        current_quantity = total_inventory_quantity(
            setting["name"],
            setting["price_type"]
        )

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
# SHOPPING LIST LOGIC
#------------------------------------------------

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

        if same_name and same_type:
            item["quantity"] += quantity

            if item["estimated_price"] == 0 and estimated_price > 0:
                item["estimated_price"] = estimated_price

            return

    shopping_list.append({
        "name": name,
        "quantity": quantity,
        "estimated_price": estimated_price,
        "source": source,
        "price_type": price_type
    })


def shopping_list_total():
    total = 0.0

    for item in shopping_list:
        total += item["quantity"] * item["estimated_price"]

    return total


#------------------------------------------------
# MEAL MESSAGE LOGIC
#------------------------------------------------

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


def clear_meal_messages_for_person(person):
    for message in meal_messages:
        if message["person"] == person:
            cleared_messages.add(("meal", message["id"]))


def clear_all_meal_messages():
    for message in meal_messages:
        cleared_messages.add(("meal", message["id"]))


#------------------------------------------------
# MESSAGE LOGIC
#------------------------------------------------

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


def food_message_text(food):
    days_left = days_until_expiry(food["expiry"])

    if days_left < 0:
        return "WARNING: " + food["name"] + " has expired."
    elif days_left == 0:
        return "WARNING: " + food["name"] + " expires today."
    elif days_left == 1:
        return "URGENT: " + food["name"] + " expires in 1 day."
    elif days_left <= 3:
        return (
            "URGENT: " + food["name"]
            + " expires in " + str(days_left) + " days."
        )
    else:
        return (
            "REMINDER: " + food["name"]
            + " expires in " + str(days_left) + " days."
        )


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

    #meal update messages
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

        text = (
            recommendation["name"]
            + " is low. Current amount: "
            + amount_text(
                recommendation["current_quantity"],
                recommendation["price_type"]
            )
            + ". Minimum wanted: "
            + amount_text(
                recommendation["minimum"],
                recommendation["price_type"]
            )
            + "."
        )

        if key not in cleared_messages:
            groups["Shopping Recommendations"].append({
                "key": key,
                "text": text
            })

    return groups


def message_count():
    groups = get_message_groups()

    return (
        len(groups["Food Alerts"])
        + len(groups["Household / Meals"])
        + len(groups["Shopping Recommendations"])
    )


#------------------------------------------------
# ADD ITEM - TKINTER
#------------------------------------------------

def open_add_item():
    global next_item_id

    name = ask_food_name(root)
    if name is None:
        return

    price_type = ask_price_type(root)
    if price_type is None:
        return

    quantity = ask_amount(price_type, root)
    if quantity is None:
        return

    price = ask_price(price_type, root)
    if price is None:
        return

    expiry = ask_expiry(root)
    if expiry is None:
        return

    category = ask_category(root)
    if category is None:
        return

    regular, minimum = ask_regular_setting(
        name,
        price,
        category,
        price_type,
        root
    )

    if regular is None:
        return

    draft = {
        "name": name,
        "price_type": price_type,
        "quantity": quantity,
        "price": price,
        "expiry": expiry,
        "category": category,
        "regular": regular,
        "minimum": minimum
    }

    while True:
        regular_text = "No"

        if draft["regular"]:
            regular_text = (
                "Yes - minimum "
                + amount_text(draft["minimum"], draft["price_type"])
            )

        summary = (
            "Food: " + draft["name"] + "\n"
            "Amount: " + amount_text(
                draft["quantity"],
                draft["price_type"]
            ) + "\n"
            "Price: " + price_text(
                draft["price"],
                draft["price_type"]
            ) + "\n"
            "Expiry: " + display_date(draft["expiry"]) + "\n"
            "Category: " + draft["category"] + "\n"
            "Regular item: " + regular_text + "\n\n"
            "Yes = Add item\n"
            "No = Edit item\n"
            "Cancel = Cancel item"
        )

        result = messagebox.askyesnocancel(
            "Check Item",
            summary,
            parent=root
        )

        if result is True:
            food = {
                "id": next_item_id,
                "name": draft["name"],
                "quantity": draft["quantity"],
                "price": draft["price"],
                "price_type": draft["price_type"],
                "expiry": draft["expiry"],
                "category": draft["category"]
            }

            inventory.append(food)

            if draft["regular"]:
                key = regular_key(
                    draft["name"],
                    draft["price_type"]
                )

                regular_items[key] = {
                    "name": draft["name"],
                    "minimum": draft["minimum"],
                    "estimated_price": draft["price"],
                    "category": draft["category"],
                    "price_type": draft["price_type"]
                }

            #adding an item is treated as a grocery purchase
            budget["spent"] += draft["quantity"] * draft["price"]

            next_item_id += 1

            messagebox.showinfo(
                "Item Added",
                draft["name"] + " has been added to the inventory.",
                parent=root
            )

            update_message_button()
            return

        elif result is None:
            return

        #No means edit the item before adding it
        edit_choice = simpledialog.askinteger(
            "Edit Item",
            "1. Food name\n"
            "2. Pricing type\n"
            "3. Quantity / weight\n"
            "4. Price\n"
            "5. Expiry date\n"
            "6. Category\n"
            "7. Regular item setting\n\n"
            "Choose what to edit:",
            minvalue=1,
            maxvalue=7,
            parent=root
        )

        if edit_choice is None:
            continue

        if edit_choice == 1:
            new_name = ask_food_name(
                root,
                title="Edit Food Name",
                current=draft["name"]
            )
            if new_name is not None:
                draft["name"] = new_name

        elif edit_choice == 2:
            new_type = ask_price_type(root, draft["price_type"])
            if new_type is not None and new_type != draft["price_type"]:
                draft["price_type"] = new_type

                new_amount = ask_amount(new_type, root)
                if new_amount is not None:
                    draft["quantity"] = new_amount

                new_price = ask_price(new_type, root)
                if new_price is not None:
                    draft["price"] = new_price

                if draft["regular"]:
                    new_minimum = ask_amount(
                        new_type,
                        root,
                        title="Minimum Stock"
                    )
                    if new_minimum is not None:
                        draft["minimum"] = new_minimum

        elif edit_choice == 3:
            new_amount = ask_amount(
                draft["price_type"],
                root,
                draft["quantity"]
            )
            if new_amount is not None:
                draft["quantity"] = new_amount

        elif edit_choice == 4:
            new_price = ask_price(
                draft["price_type"],
                root,
                draft["price"]
            )
            if new_price is not None:
                draft["price"] = new_price

        elif edit_choice == 5:
            new_expiry = ask_expiry(root, draft["expiry"])
            if new_expiry is not None:
                draft["expiry"] = new_expiry

        elif edit_choice == 6:
            new_category = ask_category(root, draft["category"])
            if new_category is not None:
                draft["category"] = new_category

        elif edit_choice == 7:
            #this edit deliberately asks again instead of reusing an old setting
            regular = messagebox.askyesno(
                "Regular Item",
                "Should " + draft["name"] + " be kept regularly stocked?",
                parent=root
            )

            draft["regular"] = regular

            if regular:
                minimum = ask_amount(
                    draft["price_type"],
                    root,
                    title="Minimum Stock"
                )
                if minimum is not None:
                    draft["minimum"] = minimum
            else:
                draft["minimum"] = 0


#------------------------------------------------
# VIEW INVENTORY - TKINTER
#------------------------------------------------

def open_inventory():
    window = tk.Toplevel(root)
    window.title("View Inventory")
    window.geometry("950x500")

    tk.Label(
        window,
        text="VIEW INVENTORY",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    frame = tk.Frame(window)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = (
        "category",
        "name",
        "amount",
        "price",
        "expiry",
        "status"
    )

    tree = ttk.Treeview(frame, columns=columns, show="headings")

    headings = {
        "category": "Category",
        "name": "Food",
        "amount": "Quantity / Weight",
        "price": "Price",
        "expiry": "Expiry",
        "status": "Status"
    }

    for column in columns:
        tree.heading(column, text=headings[column])
        tree.column(column, width=140, anchor="center")

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for food in inventory:
        tree.insert(
            "",
            "end",
            values=(
                food["category"],
                food["name"],
                amount_text(food["quantity"], food["price_type"]),
                price_text(food["price"], food["price_type"]),
                display_date(food["expiry"]),
                check_expiry(food["expiry"])
            )
        )

    if len(inventory) == 0:
        tree.insert("", "end", values=("", "Inventory is empty", "", "", "", ""))

    tk.Button(window, text="Back", command=window.destroy).pack(pady=10)


#------------------------------------------------
# UPDATE INVENTORY - TKINTER
#------------------------------------------------

def open_update_items():
    window = tk.Toplevel(root)
    window.title("Update Items")
    window.geometry("850x500")

    tk.Label(
        window,
        text="UPDATE ITEMS",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    frame = tk.Frame(window)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("name", "amount", "expiry", "category")
    tree = ttk.Treeview(frame, columns=columns, show="headings")

    tree.heading("name", text="Food")
    tree.heading("amount", text="Quantity / Weight")
    tree.heading("expiry", text="Expiry")
    tree.heading("category", text="Category")

    for column in columns:
        tree.column(column, width=180, anchor="center")

    tree.pack(fill="both", expand=True)

    def refresh():
        for row in tree.get_children():
            tree.delete(row)

        for food in inventory:
            tree.insert(
                "",
                "end",
                iid=str(food["id"]),
                values=(
                    food["name"],
                    amount_text(food["quantity"], food["price_type"]),
                    display_date(food["expiry"]),
                    food["category"]
                )
            )

    def selected_food():
        selected = tree.selection()

        if len(selected) == 0:
            messagebox.showinfo(
                "Select Item",
                "Please select an item first.",
                parent=window
            )
            return None

        return find_food_by_id(int(selected[0]))

    def update_amount():
        food = selected_food()
        if food is None:
            return

        new_amount = ask_amount(
            food["price_type"],
            window,
            food["quantity"],
            title="Update Amount"
        )

        if new_amount is None:
            return

        confirmed = messagebox.askyesno(
            "Confirm Change",
            "Change " + food["name"] + " from "
            + amount_text(food["quantity"], food["price_type"])
            + " to "
            + amount_text(new_amount, food["price_type"])
            + "?",
            parent=window
        )

        if confirmed:
            food["quantity"] = new_amount
            refresh()
            update_message_button()

            key = regular_key(food["name"], food["price_type"])

            if key in regular_items:
                setting = regular_items[key]
                current = total_inventory_quantity(
                    food["name"],
                    food["price_type"]
                )

                if current < setting["minimum"]:
                    add_now = messagebox.askyesno(
                        "Low Stock",
                        food["name"]
                        + " is below its minimum stock level.\n"
                        + "Add the missing amount to the shopping list?",
                        parent=window
                    )

                    if add_now:
                        needed = setting["minimum"] - current
                        add_to_shopping_list(
                            food["name"],
                            needed,
                            setting["estimated_price"],
                            "Low stock",
                            food["price_type"]
                        )

    def delete_item():
        food = selected_food()
        if food is None:
            return

        confirmed = messagebox.askyesno(
            "Delete Item",
            "Delete " + food["name"]
            + " expiring " + display_date(food["expiry"]) + "?",
            parent=window
        )

        if confirmed:
            inventory.remove(food)
            refresh()
            update_message_button()

    def send_to_shopping():
        food = selected_food()
        if food is None:
            return

        amount = ask_amount(
            food["price_type"],
            window,
            title="Add to Shopping List"
        )

        if amount is None:
            return

        add_to_shopping_list(
            food["name"],
            amount,
            food["price"],
            "Inventory transfer",
            food["price_type"]
        )

        messagebox.showinfo(
            "Shopping List",
            food["name"] + " was added to the shopping list.",
            parent=window
        )

    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Update Amount", command=update_amount).pack(side="left", padx=4)
    tk.Button(button_frame, text="Delete Item", command=delete_item).pack(side="left", padx=4)
    tk.Button(button_frame, text="Add to Shopping List", command=send_to_shopping).pack(side="left", padx=4)
    tk.Button(button_frame, text="Back", command=window.destroy).pack(side="left", padx=4)

    refresh()


#------------------------------------------------
# VIEW SHOPPING LIST - TKINTER
#------------------------------------------------

def build_shopping_tree(parent):
    columns = ("name", "amount", "price", "total", "source")
    tree = ttk.Treeview(parent, columns=columns, show="headings")

    tree.heading("name", text="Food")
    tree.heading("amount", text="Quantity / Weight")
    tree.heading("price", text="Estimated Price")
    tree.heading("total", text="Estimated Total")
    tree.heading("source", text="Added From")

    for column in columns:
        tree.column(column, width=150, anchor="center")

    return tree


def fill_shopping_tree(tree):
    for row in tree.get_children():
        tree.delete(row)

    for number, item in enumerate(shopping_list):
        total = item["quantity"] * item["estimated_price"]

        tree.insert(
            "",
            "end",
            iid=str(number),
            values=(
                item["name"],
                amount_text(item["quantity"], item["price_type"]),
                price_text(item["estimated_price"], item["price_type"]),
                "$" + format(total, ".2f"),
                item["source"]
            )
        )


def open_view_shopping_list():
    window = tk.Toplevel(root)
    window.title("View Shopping List")
    window.geometry("850x480")

    tk.Label(
        window,
        text="FULL SHOPPING LIST",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    tree = build_shopping_tree(window)
    tree.pack(fill="both", expand=True, padx=10, pady=10)
    fill_shopping_tree(tree)

    total_label = tk.Label(
        window,
        text="Estimated total: $" + format(shopping_list_total(), ".2f"),
        font=("Arial", 12, "bold")
    )
    total_label.pack(pady=5)

    tk.Button(window, text="Back", command=window.destroy).pack(pady=10)


#------------------------------------------------
# MANAGE SHOPPING LIST - TKINTER
#------------------------------------------------

def open_manage_shopping_list():
    window = tk.Toplevel(root)
    window.title("Manage Shopping List")
    window.geometry("900x540")

    tk.Label(
        window,
        text="MANAGE SHOPPING LIST",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    tree = build_shopping_tree(window)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    total_label = tk.Label(window, font=("Arial", 12, "bold"))
    total_label.pack(pady=5)

    def refresh():
        fill_shopping_tree(tree)
        total_label.config(
            text="Estimated total: $" + format(shopping_list_total(), ".2f")
        )

    def add_manual():
        name = ask_food_name(window, title="Shopping Item")
        if name is None:
            return

        price_type = ask_price_type(window)
        if price_type is None:
            return

        amount = ask_amount(price_type, window, title="Amount to Buy")
        if amount is None:
            return

        price = ask_price(price_type, window)
        if price is None:
            return

        add_to_shopping_list(
            name,
            amount,
            price,
            "Manual",
            price_type
        )

        refresh()

    def delete_selected():
        selected = tree.selection()

        if len(selected) == 0:
            messagebox.showinfo(
                "Select Item",
                "Please select a shopping list item first.",
                parent=window
            )
            return

        position = int(selected[0])
        item = shopping_list[position]

        confirmed = messagebox.askyesno(
            "Delete Shopping Item",
            "Delete " + item["name"] + " from the shopping list?",
            parent=window
        )

        if confirmed:
            shopping_list.pop(position)
            refresh()

    def open_recommendations():
        recommendations = shopping_recommendations()

        if len(recommendations) == 0:
            messagebox.showinfo(
                "Recommendations",
                "There are currently no shopping recommendations.",
                parent=window
            )
            return

        rec_window = tk.Toplevel(window)
        rec_window.title("Shopping Recommendations")
        rec_window.geometry("700x400")

        columns = ("name", "current", "minimum", "price")
        rec_tree = ttk.Treeview(
            rec_window,
            columns=columns,
            show="headings"
        )

        rec_tree.heading("name", text="Food")
        rec_tree.heading("current", text="Current")
        rec_tree.heading("minimum", text="Minimum")
        rec_tree.heading("price", text="Estimated Price")

        for column in columns:
            rec_tree.column(column, width=160, anchor="center")

        for number, recommendation in enumerate(recommendations):
            rec_tree.insert(
                "",
                "end",
                iid=str(number),
                values=(
                    recommendation["name"],
                    amount_text(
                        recommendation["current_quantity"],
                        recommendation["price_type"]
                    ),
                    amount_text(
                        recommendation["minimum"],
                        recommendation["price_type"]
                    ),
                    price_text(
                        recommendation["estimated_price"],
                        recommendation["price_type"]
                    )
                )
            )

        rec_tree.pack(fill="both", expand=True, padx=10, pady=10)

        def add_selected_recommendation():
            selected = rec_tree.selection()

            if len(selected) == 0:
                messagebox.showinfo(
                    "Select Recommendation",
                    "Please select a recommendation first.",
                    parent=rec_window
                )
                return

            recommendation = recommendations[int(selected[0])]
            needed = (
                recommendation["minimum"]
                - recommendation["current_quantity"]
            )

            if needed <= 0:
                needed = 1

            add_to_shopping_list(
                recommendation["name"],
                needed,
                recommendation["estimated_price"],
                "Recommendation",
                recommendation["price_type"]
            )

            messagebox.showinfo(
                "Added",
                recommendation["name"] + " was added to the shopping list.",
                parent=rec_window
            )

            refresh()
            rec_window.destroy()

        tk.Button(
            rec_window,
            text="Add Selected",
            command=add_selected_recommendation
        ).pack(side="left", padx=10, pady=10)

        tk.Button(
            rec_window,
            text="Back",
            command=rec_window.destroy
        ).pack(side="right", padx=10, pady=10)

    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Add Manually", command=add_manual).pack(side="left", padx=4)
    tk.Button(button_frame, text="Recommendations", command=open_recommendations).pack(side="left", padx=4)
    tk.Button(button_frame, text="Delete Selected", command=delete_selected).pack(side="left", padx=4)
    tk.Button(button_frame, text="Back", command=window.destroy).pack(side="left", padx=4)

    refresh()


#------------------------------------------------
# LUNCH / DINNER PLANS - TKINTER
#------------------------------------------------

def meal_status(value):
    if value is True:
        return "YES"
    elif value is False:
        return "NO"
    return "Not set"


def open_meal_plans():
    window = tk.Toplevel(root)
    window.title("Lunch / Dinner Plans")
    window.geometry("650x480")

    tk.Label(
        window,
        text="LUNCH / DINNER PLANS",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    columns = ("name", "lunch", "dinner")
    tree = ttk.Treeview(window, columns=columns, show="headings")

    tree.heading("name", text="Name")
    tree.heading("lunch", text="Lunch")
    tree.heading("dinner", text="Dinner")

    tree.column("name", width=220, anchor="center")
    tree.column("lunch", width=140, anchor="center")
    tree.column("dinner", width=140, anchor="center")

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh():
        for row in tree.get_children():
            tree.delete(row)

        for name, meals in meal_responses.items():
            tree.insert(
                "",
                "end",
                iid=name,
                values=(
                    name,
                    meal_status(meals["lunch"]),
                    meal_status(meals["dinner"])
                )
            )

    def add_or_update():
        selected = tree.selection()
        current_name = selected[0] if len(selected) > 0 else None

        person = simpledialog.askstring(
            "Household Member",
            "Enter the person's name:",
            initialvalue=current_name,
            parent=window
        )

        if person is None:
            return

        person = person.strip()

        if person == "":
            messagebox.showerror(
                "Invalid Name",
                "Name cannot be empty.",
                parent=window
            )
            return

        if person not in meal_responses:
            meal_responses[person] = {
                "lunch": None,
                "dinner": None
            }

        old_lunch = meal_responses[person]["lunch"]
        old_dinner = meal_responses[person]["dinner"]

        lunch = messagebox.askyesnocancel(
            "Lunch",
            "Is " + person + " coming home for lunch?\n\n"
            "Yes = coming\nNo = not coming\nCancel = leave unchanged",
            parent=window
        )

        dinner = messagebox.askyesnocancel(
            "Dinner",
            "Is " + person + " coming home for dinner?\n\n"
            "Yes = coming\nNo = not coming\nCancel = leave unchanged",
            parent=window
        )

        if lunch is not None:
            meal_responses[person]["lunch"] = lunch

            if old_lunch != lunch:
                add_meal_message(person, "lunch", lunch)

        if dinner is not None:
            meal_responses[person]["dinner"] = dinner

            if old_dinner != dinner:
                add_meal_message(person, "dinner", dinner)

        refresh()
        update_message_button()

    def remove_person():
        selected = tree.selection()

        if len(selected) == 0:
            messagebox.showinfo(
                "Select Person",
                "Please select a person first.",
                parent=window
            )
            return

        person = selected[0]

        confirmed = messagebox.askyesno(
            "Remove Person",
            "Remove " + person + " from the meal board?",
            parent=window
        )

        if confirmed:
            clear_meal_messages_for_person(person)
            del meal_responses[person]
            refresh()
            update_message_button()

    def reset_next_day():
        if len(meal_responses) == 0:
            messagebox.showinfo(
                "Meal Plans",
                "There are no people to reset.",
                parent=window
            )
            return

        confirmed = messagebox.askyesno(
            "Reset for Next Day",
            "Keep all names but reset Lunch and Dinner to Not set?",
            parent=window
        )

        if confirmed:
            for person in meal_responses:
                meal_responses[person]["lunch"] = None
                meal_responses[person]["dinner"] = None

            clear_all_meal_messages()
            refresh()
            update_message_button()

    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Add / Update Person", command=add_or_update).pack(side="left", padx=4)
    tk.Button(button_frame, text="Remove Person", command=remove_person).pack(side="left", padx=4)
    tk.Button(button_frame, text="Reset Next Day", command=reset_next_day).pack(side="left", padx=4)
    tk.Button(button_frame, text="Back", command=window.destroy).pack(side="left", padx=4)

    refresh()


#------------------------------------------------
# MESSAGES - TKINTER
#------------------------------------------------

def open_messages():
    window = tk.Toplevel(root)
    window.title("Messages")
    window.geometry("760x500")

    tk.Label(
        window,
        text="MESSAGES",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    categories = [
        "Food Alerts",
        "Household / Meals",
        "Shopping Recommendations"
    ]

    category_var = tk.StringVar(value=categories[0])

    category_box = ttk.Combobox(
        window,
        textvariable=category_var,
        values=categories,
        state="readonly",
        width=30
    )
    category_box.pack(pady=5)

    listbox = tk.Listbox(window, width=100, height=16)
    listbox.pack(fill="both", expand=True, padx=10, pady=10)

    current_messages = []

    def refresh(*args):
        nonlocal current_messages

        groups = get_message_groups()
        current_messages = groups[category_var.get()]

        listbox.delete(0, tk.END)

        if len(current_messages) == 0:
            listbox.insert(tk.END, "No messages in this category.")
        else:
            for message in current_messages:
                listbox.insert(tk.END, message["text"])

        update_message_button()

    def clear_selected():
        if len(current_messages) == 0:
            return

        selected = listbox.curselection()

        if len(selected) == 0:
            messagebox.showinfo(
                "Select Message",
                "Please select a message first.",
                parent=window
            )
            return

        message = current_messages[selected[0]]
        cleared_messages.add(message["key"])
        refresh()

    def clear_category():
        if len(current_messages) == 0:
            return

        confirmed = messagebox.askyesno(
            "Clear Category",
            "Clear every message in " + category_var.get() + "?",
            parent=window
        )

        if confirmed:
            for message in current_messages:
                cleared_messages.add(message["key"])
            refresh()

    def clear_all():
        groups = get_message_groups()
        all_messages = []

        for category in categories:
            all_messages.extend(groups[category])

        if len(all_messages) == 0:
            return

        confirmed = messagebox.askyesno(
            "Clear All Messages",
            "Clear all current messages?",
            parent=window
        )

        if confirmed:
            for message in all_messages:
                cleared_messages.add(message["key"])
            refresh()

    category_box.bind("<<ComboboxSelected>>", refresh)

    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Clear Selected", command=clear_selected).pack(side="left", padx=4)
    tk.Button(button_frame, text="Clear Category", command=clear_category).pack(side="left", padx=4)
    tk.Button(button_frame, text="Clear All", command=clear_all).pack(side="left", padx=4)
    tk.Button(button_frame, text="Back", command=window.destroy).pack(side="left", padx=4)

    refresh()


#------------------------------------------------
# BUDGET - TKINTER
#------------------------------------------------

def open_budget():
    window = tk.Toplevel(root)
    window.title("Budget")
    window.geometry("500x430")

    tk.Label(
        window,
        text="GROCERY BUDGET",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    budget_label = tk.Label(window, font=("Arial", 12))
    budget_label.pack(pady=5)

    spent_label = tk.Label(window, font=("Arial", 12))
    spent_label.pack(pady=5)

    remaining_label = tk.Label(window, font=("Arial", 12))
    remaining_label.pack(pady=5)

    shopping_label = tk.Label(window, font=("Arial", 12))
    shopping_label.pack(pady=5)

    projected_label = tk.Label(window, font=("Arial", 12))
    projected_label.pack(pady=5)

    warning_label = tk.Label(window, font=("Arial", 11, "bold"))
    warning_label.pack(pady=10)

    def refresh():
        estimated_shopping = shopping_list_total()

        if budget["limit"] == 0:
            budget_label.config(text="Weekly budget: Not set")
            remaining_label.config(text="Remaining: Not available")
            projected_label.config(text="Projected spending: Not available")
            warning_label.config(text="")
        else:
            remaining = budget["limit"] - budget["spent"]
            projected = budget["spent"] + estimated_shopping

            budget_label.config(
                text="Weekly budget: $" + format(budget["limit"], ".2f")
            )
            remaining_label.config(
                text="Remaining: $" + format(remaining, ".2f")
            )
            projected_label.config(
                text="Projected spending after shopping list: $"
                + format(projected, ".2f")
            )

            if projected > budget["limit"]:
                warning_label.config(
                    text="WARNING: Projected spending is $"
                    + format(projected - budget["limit"], ".2f")
                    + " over budget."
                )
            else:
                warning_label.config(text="")

        spent_label.config(
            text="Amount spent: $" + format(budget["spent"], ".2f")
        )

        shopping_label.config(
            text="Shopping list estimated cost: $"
            + format(estimated_shopping, ".2f")
        )

    def set_budget():
        amount = simpledialog.askfloat(
            "Set Budget",
            "Enter weekly grocery budget: $",
            minvalue=0,
            parent=window
        )

        if amount is not None:
            budget["limit"] = amount
            refresh()

    def add_spending():
        amount = simpledialog.askfloat(
            "Add Spending",
            "Enter grocery spending amount: $",
            minvalue=0,
            parent=window
        )

        if amount is not None:
            budget["spent"] += amount
            refresh()

    def reset_spending():
        confirmed = messagebox.askyesno(
            "Reset Spending",
            "Reset weekly spending to $0.00?",
            parent=window
        )

        if confirmed:
            budget["spent"] = 0.0
            refresh()

    button_frame = tk.Frame(window)
    button_frame.pack(pady=15)

    tk.Button(button_frame, text="Set Budget", command=set_budget).pack(side="left", padx=4)
    tk.Button(button_frame, text="Add Spending", command=add_spending).pack(side="left", padx=4)
    tk.Button(button_frame, text="Reset Spending", command=reset_spending).pack(side="left", padx=4)

    tk.Button(window, text="Back", command=window.destroy).pack(pady=10)

    refresh()


#------------------------------------------------
# MAIN WINDOW
#------------------------------------------------

def exit_program():
    confirmed = messagebox.askyesno(
        "Exit Smart Pantry",
        "Are you sure you want to exit?",
        parent=root
    )

    if confirmed:
        root.destroy()


def build_main_window():
    global root, messages_button

    root = tk.Tk()
    root.title("Smart Pantry")
    root.geometry("500x650")
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", exit_program)

    tk.Label(
        root,
        text="SMART PANTRY",
        font=("Arial", 22, "bold")
    ).pack(pady=(25, 5))

    tk.Label(
        root,
        text="Household Food Management",
        font=("Arial", 11)
    ).pack(pady=(0, 20))

    menu = tk.Frame(root)
    menu.pack(fill="both", expand=True, padx=55)

    buttons = [
        ("View Inventory", open_inventory),
        ("Add Item", open_add_item),
        ("Update Items", open_update_items),
        ("View Shopping List", open_view_shopping_list),
        ("Manage Shopping List", open_manage_shopping_list),
        ("Lunch / Dinner Plans", open_meal_plans)
    ]

    for text, command in buttons:
        tk.Button(
            menu,
            text=text,
            height=2,
            command=command
        ).pack(fill="x", pady=4)

    messages_button = tk.Button(
        menu,
        text="Messages (" + str(message_count()) + ")",
        height=2,
        command=open_messages
    )
    messages_button.pack(fill="x", pady=4)

    tk.Button(
        menu,
        text="Budget",
        height=2,
        command=open_budget
    ).pack(fill="x", pady=4)

    tk.Button(
        menu,
        text="Exit",
        height=2,
        command=exit_program
    ).pack(fill="x", pady=(15, 4))

    root.mainloop()


if __name__ == "__main__":
    build_main_window()
