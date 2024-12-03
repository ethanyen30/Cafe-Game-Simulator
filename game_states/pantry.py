from game_states.states import *

class Pantry(State):
    def __init__(self, pantry_file):
        super().__init__()
        self.pantry = {}
        self.initialize_pantry_defaults(pantry_file)

    def do(self, chef, action):
        pantry_re = re.compile(f"^((store {self.noun_re})|(get {self.noun_re})|(close)|(look))$")
        """
        Match group numbers:
            0: Whole match
            1: First match (don't worry about this)
            2: Whole 'store' part
                3: ingredient to store into pantry
                4: inside noun regex (don't worry about this)
            5: Whole 'get' part
                6: ingredient to get from pantry
                7: inside noun regex (don't worry about this)
            8: Whole 'close' part
            9: Whole 'look' part
        """
        matched = pantry_re.match(action)

        if not matched:
            print("idk what ur doing in the pantry")
            return

        # Store ingredient in pantry
        if matched.group(2) != None:
            ingredient = matched.group(3)
            self.store_pantry(chef, ingredient)

        # Get food from pantry
        elif matched.group(5) != None:
            ingredient = matched.group(6)
            self.get_pantry(chef, ingredient)

        # Leave pantry
        elif matched.group(8) != None:
            print("Leaving pantry")
            return "cafe"
        
        # Look at pantry
        elif matched.group(9) != None:
            self.look_pantry()
    
    """
    Here will be methods that correspond directly above matches
    """

    ################################
    #  PANTRY METHODS START HERE   #
    ################################
    def store_pantry(self, chef, ingredient):
        if dict_move_element(chef.inventory, self.pantry, self.pantry_size(), float('inf'), ingredient, 
                          1, "store", "inventory", "pantry") == "success":
            print(f"Storing {ingredient}")
    
    def get_pantry(self, chef, ingredient):
        if dict_move_element(self.pantry, chef.inventory, chef.inventory_size(), chef.max_inventory, ingredient, 
                             1, "get", "pantry", "inventory") == "success": 
            print(f"Getting {ingredient}")
        
    def look_pantry(self):
        print(f"\nPantry: (Max capacity = {float('inf')})")
        dict_printer(self.pantry, "Ingredient", "Count")

    """
    Here will be helper methods are just other methods that can be accessed with this class
    """

    ###############################
    #  HELPER METHODS START HERE  #
    ###############################
    def initialize_pantry_defaults(self, default_file):
        ingredient_re = re.compile(f"^{self.noun_re}$")
        with open(default_file) as f:
            for line in f:
                default = line.strip("\n")
                if ingredient_re.match(default) == None:
                    self.pantry = None
                    return
                self.pantry.update({default: 999})

    def pantry_size(self):
        return dict_size(self.pantry)