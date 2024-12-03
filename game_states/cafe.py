from game_states.states import *

class Cafe(State):
    def __init__(self, chef, max_counter, customer_names_file):
        super().__init__()
        self.counter = {}
        self.max_counter = max_counter

        self.customer_names_file = customer_names_file
        self.check_customer_file()
        self.customers = []
        self.completed = []
        self.available_foods = chef.available_foods()

        # Variables to keep track of while 'making'
        self.making = ""        # "" for not making anything; otherwise recipe/food name
        self.making_step = 1    # recipe step number
        self.used_ingredients = []

    # Action to be done
    def do(self, chef, action):
        restaurant_re = re.compile(f"^((make {self.noun_re})"
                                    f"|(serve {self.noun_re} to {self.noun_re})"
                                    f"|(orders)"
                                    f"|(lc)"
                                    f"|(set {self.noun_re})"
                                    f"|(clear {self.noun_re})"
                                    f"|(open pantry)"
                                    f"|(go to store)"
                                    f"|(completed))$")
        """
        Match group numbers:
            0: Whole match
            1: First match (don't worry about this)
            2: Whole 'make' part
                3: food to make
                4: inside noun regex (don't worry about this)
            5: Whole 'serve' part
                6: What to serve
                7: inside noun regex (don't worry about this)
                8: Who to serve to
                9: inside noun regex (don't worry about this)
            10: Whole 'orders' part
            11: Whole 'lc' part
            12: Whole 'set' part
                13: What to set on counter from inventory
                14: inside noun regex (don't worry about this)
            15: Whole 'clear' part
                16: What to clear from counter to inventory
                17: inside noun regex (don't worry about this)
            18: Whole 'open pantry' part
            19: Whole 'go to store' part
            20: Whole 'completed' part
        """
        matched = restaurant_re.match(action)

        # If not one of the main actions, check if it's a making action
        if not matched:

            # If not making then return
            if self.making == "":
                print("idk what ur doing in the cafe")
                return
            
            # If making
            else:
                making_re = re.compile(f"^(({self.verb_re} {self.noun_re})|(stop))$")
                """
                Match group numbers:
                    0: Whole match
                    1: First match (don't worry about this)
                    2: Whole step line
                        3: verb used
                        4: ingredient used
                        5: inside noun regex (don't worry about this)
                    6: Whole 'stop' part
                """
                matched = making_re.match(action)

                # If action is not a making action
                if not matched:
                    print(f"idk what ur doing while trying to make {self.making}")
                    return

                # Read step line from user
                if matched.group(2) != None:
                    verb = matched.group(3)
                    ingredient = matched.group(4)
                    self.make_step(chef, verb, ingredient)

                # Stop making
                elif matched.group(6) != None:
                    self.stop_making()
                
                return

        # Make food
        if matched.group(2) != None:
            food = matched.group(3)
            self.start_making(chef, food)

        # Serve food to customer
        elif matched.group(5) != None:
            food = matched.group(6)
            customer = matched.group(8)
            self.serve(chef, food, customer)

        # List orders
        elif matched.group(10) != None:
            self.list_orders()

        # List things on counter
        elif matched.group(11) != None:
            self.list_counter()
        
        # Set ingredients from inventory to counter
        elif matched.group(12) != None:
            ingredient = matched.group(13)
            self.set_counter(chef, ingredient)
        
        # Clear ingredients from counter to inventory
        elif matched.group(15) != None:
            ingredient = matched.group(16)
            self.clear_counter(chef, ingredient)

        # Open pantry
        elif matched.group(18) != None:
            print("Going to pantry")
            return "pantry"
            
        # Go to store
        elif matched.group(19) != None:
            print("Going to store")
            return "store"
        
        # List completed foods
        elif matched.group(20) != None:
            self.list_completed()


    """
    Here will be methods that correspond directly above matches
    """

    ################################
    #  MAKING METHODS START HERE   #
    ################################
    def start_making(self, chef, food):
        recipe = chef.get_recipe(food)
        if recipe == None:
            print(f"Can't make {food} because it's not in the recipe book")
            return
        
        print(f"Making {food}")
        self.making = food
        self.making_step = 1
        self.used_ingredients.clear()
                
    def make_step(self, chef, verb, ingredient):
        recipe = chef.get_recipe(self.making)
        whole_step = verb + " " + ingredient
        if whole_step == recipe['steps'][self.making_step - 1]:
            if self.use_counter(ingredient) == "success":
                print(f"finished '{verb}'ing {ingredient}")
                self.making_step += 1
            if self.making_step > len(recipe['steps']):
                self.completed.append(self.making)
                self.stop_making()
                print(f"{recipe['name']} is completed")
        else:
            print("wrong step")

    def stop_making(self):
        print(f"Stopped making {self.making}")
        self.making = ""
        self.making_step = 1
        self.used_ingredients.clear()
        
    
    ##################
    #  SERVE METHOD  #
    ##################
    def serve(self, chef, food, customer):
        if food in self.completed:
            customer_order = ""
            customer_index = -1
            for i, c in enumerate(self.customers):
                if c.name == customer:
                    customer_order = c.order
                    customer_index = i
                    break
            if customer_index == -1:
                print(f"{customer} is not in the cafe")
                return
            if food == customer_order:
                departure = round(time.time(), 1)
                self.completed.remove(food)
                earnings = self.customers[customer_index].tip(departure)
                self.customers.pop(customer_index)

                chef.customers_fed += 1
                chef.deposit(earnings)

                print(f"Served {food} to {customer}")
                print(f"{customer} gave you {earnings:.2f}$")

            else:
                print(f"{customer} didn't order {food}")
        else:
            print(f"You haven't made {food} yet.")

    ################################
    #  LISTING METHODS START HERE  #
    ################################
    def list_orders(self):
        print("Here are your orders:")
        for c in self.customers:
            print(f"- {c.name} ordered {c.order}")

    def list_completed(self):
        print("Here are the completed foods:")
        for completed in self.completed:
            print("- " + completed)

    def list_counter(self):
        print(f"\nCounter: (Max capacity = {self.max_counter})")
        dict_printer(self.counter, "Ingredient", "Count")
    
    ################################
    #  COUNTER METHODS START HERE  #
    ################################
    def set_counter(self, chef, ingredient):
        if dict_move_element(chef.inventory, self.counter, self.counter_size(), self.max_counter, ingredient, 
                          1, "set", "inventory", "counter") == "success":
                    
            # Print message if successful
            print(f"Setting {ingredient}")
        
    def clear_counter(self, chef, ingredient):
        if dict_move_element(self.counter, chef.inventory, chef.inventory_size(), chef.max_inventory, ingredient, 
                             1, "clear", "counter", "inventory") == "success":
            
            # Print message if successful
            print(f"Clearing {ingredient}")

    """
    Here will be helper methods are just other methods that can be accessed with this class
    """

    ###############################
    #  HELPER METHODS START HERE  #
    ###############################
    def counter_size(self):
        return dict_size(self.counter)
    
    def use_counter(self, ingredient):
        if ingredient not in self.used_ingredients:
            if dict_decrement(self.counter, ingredient, True, "use", "on", "counter") == "fail":
                return "fail"
            else:
                self.used_ingredients.append(ingredient)
                print(f"{ingredient} used")
        return "success"
    
    def check_customer_file(self):
        name_re = re.compile(f"^{self.noun_re}$")
        with open(self.customer_names_file) as f:
            for line in f:
                name = line.strip("\n")
                if name_re.match(name) == None:
                    self.customer_names_file = None
                    return
    
    # Adds and prints a new customer
    def new_customer(self):
        c = Customer()
        c.name_chooser(self.customer_names_file)
        c.order_chooser(self.available_foods)
        print(f"\n{c.name} has arrived and they want {c.order}")
        self.customers.append(c)
        print("~> ", end="")