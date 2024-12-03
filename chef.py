from utils import *
from game_states.recipe import Recipe

class Chef:
    def __init__(self, name, starting_money, max_inventory, recipe_file):
        self.name = name
        self.inventory = {}
        self.max_inventory = max_inventory
        self.wallet = starting_money
        self.customers_fed = 0
        self.recipes = Recipe(recipe_file)
        
    def list_inventory(self):
        print(f"\nInventory: (Max capacity = {self.max_inventory})")
        dict_printer(self.inventory, "Ingredient", "Count")

    def inventory_size(self):
        return dict_size(self.inventory)

    def deposit(self, amount):
        self.wallet += amount

    def withdraw(self, amount):
        if self.wallet - amount < 0:
            print(f"You don't have enough money to withdraw {amount:.2f}$")
            self.inventory.clear()
            return "fail"
        else:
            self.wallet -= amount
            return "success"

    def list_recipes(self, state):
        self.recipes.open_recipe(state)

    def see_wallet(self):
        print(f"{self.name} has {self.wallet:.2f}$")

    def get_stats(self):
        print(f"Customers served: {self.customers_fed}")
        print(f"Money: {self.wallet:.2f}$")

    def chef_action(self, action, state):
        # Actions that chef can do at any time
        if action == "ls":
            self.list_inventory()
            return "success"
        elif action == "recipes":
            self.list_recipes(state)
            return "recipe"
        elif action == "wallet":
            self.see_wallet()
            return "success"
        else:
            return "fail"

    def get_recipe(self, food):
        return self.recipes.get_recipe(food)
    
    def available_foods(self):
        return self.recipes.get_available_foods()
        