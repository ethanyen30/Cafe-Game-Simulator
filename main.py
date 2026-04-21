from driver import Driver
import subprocess

subprocess.run('cls', shell=True)
starting_money=15
max_inventory=5
max_counter=10,
recipe_file="defaults/recipes.txt"
customer_names_file="defaults/customer_names.txt"
pantry_file="defaults/pantry.txt"
launch_file="defaults/launch_screen.txt"
customer_interval=45
max_customers=5
mode="timed"

print("Version: Default")
print("\tUser Defaults:")
print("\t\tA. Starting Money: 15")
print("\t\tB. Max Inventory: 5")
print("\t\tC. Max Counter: 10")
print("\tFile Defaults:")
print("\t\tD. Recipe File: 'defaults/recipes.txt'")
print("\t\tE. Customer Names Files: 'defaults/customer_names.txt'")
print("\t\tF. Pantry File: 'defaults/pantry.txt'")
print("\t\tG. Launch Screen File: 'defaults/launch_screen.txt'")
print("\tGame Defaults:")
print("\t\tH. Customer Interval: 45")
print("\t\tI. Max Customers: 5")
print("\t\tJ. Mode: timed")

print()
print("Options:")
print("1. Continue")
print("2. Change Defaults")
print()
while True:
    option = input("Select an option: ")
    if option == "1":
        break
    elif option == "2":
        while True:
            default = input("Select a default to change (type 'save' to save changes): ")
            if default == "A":
                sm = input("Choose Starting Money: ")
                starting_money = int(sm)
            elif default == "B":
                mi = input("Choose Max Inventory: ")
                max_inventory = int(mi)
            elif default == "C":
                mc = input("Choose Max Counter: ")
                max_counter = int(mc)
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
                customer_interval = int(ci)
            elif default == "I":
                mc = input("Choose Max Customers: ")
                max_customers = int(mc)
            elif default == "J":
                m = input("Choose Mode ('timed' or 'testing' (which is untimed)): ")
                mode = m
            elif default == "save":
                break

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