import time
from utils import *
from game_states.recipe import Recipe

class Chef:
    def __init__(self, name, starting_money, max_inventory, recipe_file):
        self.name = name
        self.inventory = {}
        self.max_inventory = max_inventory
        self.wallet = starting_money
        self.customers_fed = 0
        self.servings = []
        self.recipes = Recipe(recipe_file)
        self.start_time = time.time()
        
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
        customer_width = 13
        order_width = 15
        time_width = 10
        earnings_width = 13
        print("Game History:")
        header = f"{"Customer":<{customer_width}}" + \
                 f"{"Orders":<{order_width}}" + \
                 f"{"Time":<{time_width}}" + \
                 f"{"Earnings":<{earnings_width}}"
        print("-" * len(header))
        print(header)
        print("-" * len(header))
        for serving in self.servings:    
            print(f"{serving['Customer name']:<{customer_width}}" + \
                  f"{serving['Food ordered']:<{order_width}}" + \
                  f"{str(serving['Cooking time']) + "s":<{time_width}}" + \
                  f"{str(round(serving['Earnings'], 2)) + "$":<{earnings_width}}")
        print("-" * len(header))
        print(f"Customers served: {len(self.servings)}")
        print(f"Money: {self.wallet:.2f}$")
        print(f"Money earned: {self.wallet-15:.2f}$")
        print(f"Time played: {round(time.time() - self.start_time, 1)} seconds")

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
        