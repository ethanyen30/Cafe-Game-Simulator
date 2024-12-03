from game_states.states import *

class Recipe(State):
    def __init__(self, recipe_file):
        super().__init__()
        self.recipes = self.load_recipe(recipe_file)
        self.count = len(self.recipes)

        # Current recipe (1 indexed)
        self.curr = 1

        self.prev_state = "cafe"

    # Actions to be done
    def do(self, _, action):
        if action == "flip":
            self.flip()

        elif action == "back":
            self.back()

        elif action == "close":
            print("Closing recipe book")
            return self.prev_state
        else:
            print("idk what ur doing in the recipe book")
            return
    
    """
    Here will be methods that correspond directly above matches
    """

    ################################
    #  RECIPE METHODS START HERE   #
    ################################
    def flip(self):
        if self.curr == self.count:
            self.curr = 1
        else:
            self.curr += 1
        self.open_recipe(self.prev_state)

    def back(self):
        if self.curr == 1:
            self.curr = self.count
        else:
            self.curr -= 1
        self.open_recipe(self.prev_state)

    """
    Here will be helper methods are just other methods that can be accessed with this class
    """

    ###############################
    #  HELPER METHODS START HERE  #
    ###############################

    # Load the recipe file. Used in constructor
    def load_recipe(self, file):
        name_re = re.compile(f"^name: {self.noun_re}$")
        ingredients_re = re.compile(f"^ingredients: (({self.noun_re}, )*{self.noun_re})$")
        steps_re = re.compile(rf"^(\d)\. ({self.verb_re} {self.noun_re})$")

        recipes = []
        recipe_count = 1

        with open(file) as f:
            finished = False
            while not finished:
                recipe = {}
                recipe.update({"number": recipe_count})
                name = f.readline().strip()
                name_matched = name_re.match(name)
                if not name_matched:
                    return None
                else:
                    name = name_matched.group(1)
                    recipe.update({"name": name})
                
                ingredients = f.readline().strip()
                ingredients_matched = ingredients_re.match(ingredients)
                if not ingredients_matched:
                    return None
                else:
                    ingredients = ingredients_matched.group(1).split(", ")
                    recipe.update({"ingredients": ingredients})
                
                used_ingredients = []
                for ing in ingredients:
                    used_ingredients.append(ing)
                    
                steps_start = f.readline().strip()
                if steps_start != "steps:":
                    return None
                else:
                    step_list = []
                    step = f.readline()
                    step_number = 1
                    
                    while step != "\n":
                        if step == "":
                            finished = True
                            break
                        
                        step = step.strip()
                        step_matched = steps_re.match(step)
                        if not step_matched:
                            return None
                        else:
                            number = step_matched.group(1)
                            if number != str(step_number):
                                return None
                            
                            step = step_matched.group(2)
                            step_list.append(step)

                            ingredient = step_matched.group(4)
                            if ingredient in used_ingredients:
                                used_ingredients.remove(ingredient)

                            step = f.readline()
                            step_number += 1

                    if used_ingredients != []:
                        return None
                    if step_list == []:
                        return None
                    recipe.update({"steps": step_list})
                
                recipes.append(recipe)
                recipe_count += 1
            
            return recipes

    # Prints the recipe book nicely
    def open_recipe(self, state):
        if state == "Recipe":
            print("You're already reading the recipe book")
            return
        else:
            self.prev_state = state.lower()

        if self.recipes == []:
            print("Empty Recipe Book")
        else:
            print()
            recipe = self.recipes[self.curr - 1]
            print(f"Recipe number {recipe['number']}:")

            print(f"\tName: {recipe['name']}")

            print(f"\tIngredients: {', '.join(recipe['ingredients'])}")

            print("\tSteps:")
            step_count = 1
            for step in recipe['steps']:
                print(f"\t\t{step_count}. {step}")
                step_count += 1
            
            print()
            print("'flip' to go to next recipe")
            print("'back' to go to prev recipe")
            print("'close' to close the book")
        print()

    # Returns the recipe dict given the name of the recipe
    def get_recipe(self, name):
        for recipe in self.recipes:
            if recipe['name'] == name:
                return recipe
        return None
    
    # Returns available foods
    def get_available_foods(self):
        af = []
        for r in self.recipes:
            af.append(r['name'])
        return af