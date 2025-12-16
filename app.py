import json
import os

filename = "purchases.json"

def welcome_screen():
    print("""===============================
GROCERY INVENTORY SYSTEM
===============================""")

def view_inventory():
    # prints the inventory
    print()
    for i, idx in enumerate(data['items'], 1):
        item = data["items"][idx]
        print(f"{i}) {item["name"]} - ${item["price"]} ({item["quantity"]} available)")
    print("0) Finish purchase")

def validate_choice(item_keys):
    # validates choice for what product they want
    while True:
        try:
            choice = int(input("Enter your choice: "))

            if choice < 0 or choice > len(data["items"]):
                print("Invalid choice.\nTry again.\n")
                continue

            if choice == 0:
                return 0
            
            if 1 <= choice <= len(item_keys):
                return choice

        except ValueError:
             print("Invalid.\nMust be numeric.\n")

def validate_quantity(item):
    # Check to make sure the # of item is in stock
    while True:
        try:
            quantity = int(input("Quantity: "))

            if quantity > item["quantity"]:
                print("Not enough items in stock.\n")
                continue

            if quantity <= 0:
                print("Quantity must be greater than 0.\n")
                continue

            return quantity

        except ValueError:
            print("Invalid.\nMust be numeric.\n")

def load_purchases(filename):
    # load purchases history
    if not os.path.exists(filename):
        print("No purchase history.")
        return []

    if os.path.getsize(filename) == 0:
        return []

    with open(filename, "r") as file:
        return json.load(file)

with open("inventory.json", "r") as file:
    data = json.load(file)

welcome_screen()
print()

item_keys = list(data["items"])
total = 0

def choices():
    # Options of what the user can do
    print("""1) View inventory
2) Make a purchase
3) View past purchases
4) Quit""")
    
    try:
        decision = int(input("Enter choice (1- 4): "))
        print()

        if decision > 4 or decision <= 0:
            print("Please enter a valid integer.\n")
            
        else:
            return decision

    except ValueError:
        print("Please enter a numeric value.")

def save_purchase(purchase, filename):
    # saves the purchases to purchases.json file
    purchases = load_purchases(filename)
    purchases.append(purchase)

    with open(filename, "w") as file:
        json.dump(purchases, file, indent = 4)

def make_purchase(data, total):
    # where the user makes purchases and is stored to later save into a json file
    items_bought = []
    total = 0
    while True:
        view_inventory()
        choice = validate_choice(item_keys)

        if choice == 0:
            name = input("Enter your name: ")
            

            purchase = {
                "buyer": name,
                "items": items_bought,
                "total_cost": round(total, 2)
            }

            save_purchase(purchase, filename)
            print(f"Total : ${round(total, 2)}")
            return


        item = data["items"][item_keys[choice - 1]]
        quantity = validate_quantity(item)

        item["quantity"] -= quantity
        subtotal = item["price"] * quantity
        total += subtotal

        items_bought.append({
            "item_name": item['name'],
            "quantity": quantity,
            "subtotal": round(subtotal, 2)
        })

def view_past_purchases(filename):
    # allows user to view past purchases
    purchases = load_purchases(filename)
    if not purchases:
        print("No past purchases found.\n")

    else:
        print("\nPast Purchases:")
        for i, purchase in enumerate(purchases, 1):
            print(f"{i} {purchase["buyer"]} - Total: ${purchase["total_cost"]}")

def conditions(choice):
    # conditions for the user
    if choice == 1:
        view_inventory()
    
    if choice == 2:
        make_purchase(data, total)

    if choice == 3:
        view_past_purchases(filename)
            
    if choice == 4:
        print("Have a good day.")
        exit()

#Everything put together
def main():
    while True:
        choice = choices()
        conditions(choice)
        print()

if __name__ == "__main__":
    main()