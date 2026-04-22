from driver import Driver
import subprocess

subprocess.run('cls', shell=True)

# Default settings
starting_money=15
max_inventory=5
max_counter=10
recipe_file="defaults/recipes.txt"
customer_names_file="defaults/customer_names.txt"
pantry_file="defaults/pantry.txt"
launch_file="defaults/launch_screen.txt"
customer_interval=45
max_customers=5
mode="timed"

def print_settings(
    starting_money,
    max_inventory,
    max_counter,
    recipe_file,
    customer_names_file,
    pantry_file,
    launch_file,
    customer_interval,
    max_customers,
    mode
):
    print("Settings")
    print("\tUser:")
    print(f"\t\tA. Starting Money: {starting_money}")
    print(f"\t\tB. Max Inventory: {max_inventory}")
    print(f"\t\tC. Max Counter: {max_counter}")
    print("\tFiles:")
    print(f"\t\tD. Recipe File: {recipe_file}")
    print(f"\t\tE. Customer Names File: {customer_names_file}")
    print(f"\t\tF. Pantry File: {pantry_file}")
    print(f"\t\tG. Launch Screen File: {launch_file}")
    print("\tGame:")
    print(f"\t\tH. Customer Interval: {customer_interval}")
    print(f"\t\tI. Max Customers: {max_customers}")
    print(f"\t\tJ. Mode: {mode}")

print_settings(
    starting_money,
    max_inventory,
    max_counter,
    recipe_file,
    customer_names_file,
    pantry_file,
    launch_file,
    customer_interval,
    max_customers,
    mode
)

while True:
    print()
    print("Options:")
    print("1. Continue")
    print("2. Change Settings")
    print()
    option = input("Select an option: ")
    if option == "1":
        break
    elif option == "2":
        while True:
            default = input("Select a default to change (type 'save' to save changes): ")
            if default == "A":
                sm = input("Choose Starting Money: ")
                if sm.isdigit():
                    starting_money = int(sm)
                else:
                    print("Please enter a valid integer for Starting Money.")
                    continue
            elif default == "B":
                mi = input("Choose Max Inventory: ")
                if mi.isdigit():
                    max_inventory = int(mi)
                else:
                    print("Please enter a valid integer for Max Inventory.")
                    continue
            elif default == "C":
                mc = input("Choose Max Counter: ")
                if mc.isdigit():
                    max_counter = int(mc)
                else:
                    print("Please enter a valid integer for Max Counter.")
                    continue
            elif default == "D":
                rf = input("Choose Recipe File (path to file): ")
                recipe_file = rf
            elif default == "E":
                cnf = input("Choose Customer Names File (path to file): ")
                customer_names_file = cnf
            elif default == "F":
                pf = input("Choose Pantry File (path to file): ")
                pantry_file = pf
            elif default == "G":
                lf = input("Choose Launch Screen File (path to file): ")
                launch_file = lf
            elif default == "H":
                ci = input("Choose Customer Interval: ")
                if ci.isdigit():
                    customer_interval = int(ci)
                else:
                    print("Please enter a valid integer for Customer Interval.")
                    continue
            elif default == "I":
                mc = input("Choose Max Customers: ")
                if mc.isdigit():
                    max_customers = int(mc)
                else:
                    print("Please enter a valid integer for Max Customers.")
                    continue
            elif default == "J":
                m = input("Choose Mode ('timed' or 'testing' (which is untimed)): ")
                if m not in ["timed", "testing"]:
                    print("Please enter a valid mode.")
                    continue
                mode = m
            elif default == "save":
                break
        print_settings(
            starting_money,
            max_inventory,
            max_counter,
            recipe_file,
            customer_names_file,
            pantry_file,
            launch_file,
            customer_interval,
            max_customers,
            mode
        )

game = Driver(
    starting_money=starting_money,
    max_inventory=max_inventory,
    max_counter=max_counter,
    recipe_file=recipe_file,
    customer_names_file=customer_names_file,
    pantry_file=pantry_file,
    launch_file=launch_file,
    customer_interval=customer_interval,
    max_customers=max_customers,
    mode=mode
)
game.start()