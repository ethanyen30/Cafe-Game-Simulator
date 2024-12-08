import time

from chef import Chef
from game_states.cafe import Cafe
from game_states.pantry import Pantry
from game_states.store import Store

class CafeGame:
    def __init__(self, chef_name, starting_money, max_inventory, max_counter, 
                 recipe_file, customer_names_file, pantry_file):
        self.chef = Chef(chef_name, starting_money, max_inventory, recipe_file)
        self.cafe = Cafe(self.chef, max_counter, customer_names_file)
        self.pantry = Pantry(pantry_file)
        self.store = Store()
        
        self.state = self.cafe

        self.start_time = 0
    
    def check_file_formats(self):
        invalid = False
        # If recipe is empty then return
        if self.chef.recipes.recipes == None:
            print("Invalid recipe file")
            invalid = True
        if self.pantry.pantry == None:
            print("Invalid pantry file")
            invalid = True
        if self.cafe.customer_names_file == None:
            print("Invalid customer names file")
            invalid = True
        if invalid:
            return False
        else:
            return True
        
    def start_timer(self):
        self.start_time = time.time()

    def input_action(self, action):

        # Help action
        if action == "help":
            self.state.get_help()
            return

        # Actions that chef can do at any time
        ret_chef = self.chef.chef_action(action, self.state.__class__.__name__)
        if ret_chef == "success":
            return
        elif ret_chef == "recipe":
            self.state = self.chef.recipes
        else:
            ret_state = self.state.do(self.chef, action)
            match ret_state:
                case "cafe":
                    self.state = self.cafe
                case "pantry":
                    self.state = self.pantry
                case "store":
                    self.state = self.store
                case "served":
                    return "served"
                case _:
                    pass
