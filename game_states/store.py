from game_states.states import *

class Store(State):
    def __init__(self):
        super().__init__()
        self.cart = {}
        self.prices = {}
    
    def get_help(self):
        instructions = {
                        "price <ingredient>": "checks the price of an ingredient",
                        "take <ingredient>": "takes ingredient from the shelf",
                        "cart": "displays what you have in the cart",
                        "prices": "displays all ingredients and prices in the store",
                        "return <ingredient>": "returns the ingredient back onto the shelf",
                        "checkout": "checks out of the store and goes back to the cafe"
                        }
        super().get_help(self.__class__.__name__, instructions)

    def do(self, chef, action):
        store_re = re.compile(f"^((price {self.noun_re})|(take {self.noun_re})|"
                              f"(cart)|(checkout)|(prices)|(return {self.noun_re}))$")
        """
        Match group numbers:
            0: Whole match
            1: First match (don't worry about this)
            2: Whole 'price' part
                3: ingredient to check price for
                4: inside noun regex (don't worry about this)
            5: Whole 'take' part
                6: ingredient to take from store
                7: inside noun regex (don't worry about this)
            8: Whole 'cart' part
            9: Whole 'checkout' part
            10: Whole 'prices' part
            11: Whole 'return' part
                12: ingredient to return
                13: inside noun regex (don't worry about this)
        """
        matched = store_re.match(action)
        
        if not matched:
            print("idk what ur doing in the store")
            return

        # Check ingredient price
        if matched.group(2) != None:
            ingredient = matched.group(3)
            self.check_price(ingredient)

        # take ingredient and put into cart
        elif matched.group(5) != None:
            ingredient = matched.group(6)
            self.store_take(chef, ingredient)

        # List things in shopping cart
        elif matched.group(8) != None:
            self.check_cart()

        # Checkout and return to cafe
        elif matched.group(9) != None:
            if self.checkout(chef) == "fail":
                return "fail"
            return "cafe"
        
        # Check prices of everything
        elif matched.group(10) != None:
            self.all_prices()

        elif matched.group(11) != None:
            ingredient = matched.group(12)
            self.store_return(ingredient)

    """
    Here will be methods that correspond directly above matches
    """

    ################################
    #  STORE METHODS START HERE    #
    ################################
    
    # Adds or prints price of ingredient
    def check_price(self, ingredient):
        if not ingredient in self.prices:
            multiplier = len(ingredient)
            rand_price = random.randrange(50, 500) / 100
            self.prices.update({ingredient: rand_price})
        
        print(f"{ingredient}: {self.prices[ingredient]}$")

    def store_take(self, chef, ingredient):
        if not ingredient in self.prices:
            print(f"Check the price of {ingredient} first")
        else:
            chef_remaining_space = chef.max_inventory - chef.inventory_size()
            if self.cart_count() >= chef_remaining_space:
                print("No space in inventory to fit everything after buying")
                return
            
            # At this point, we haven't added the ingredient to the cart yet, so cart_price() returns
            # the current cart price, so we need to add the price of this ingredient to check if we can add it
            if dict_increment(self.cart, self.cart_price(False) + self.prices[ingredient], 
                              False, ingredient, None, None, None, chef.wallet) == "fail":
                print(f"You don't have money if you want to buy more {ingredient}s")
                return
            print(f"Took {ingredient}")
    
    def store_return(self, ingredient):
        if not ingredient in self.prices:
            print(f"Can't return {ingredient} because it's not in the store")
        else:
            if dict_decrement(self.cart, ingredient, True, "return", "in", "cart") == "fail":
                return
            print(f"Returned {ingredient}")

    def check_cart(self):
        print("\nCart:")
        self.cart_price(True)

    def checkout(self, chef):
        print("\nReceipt:")
        total = self.cart_price(True)

        for item in self.cart:
            for _ in range(self.cart[item]):
                dict_increment(chef.inventory, chef.inventory_size(), False, item)

        self.cart.clear()
        chef.withdraw(total)

    def all_prices(self):
        dict_printer(self.prices, "Ingredient", "Price")

    """
    Here will be helper methods are just other methods that can be accessed with this class
    """

    ###############################
    #  HELPER METHODS START HERE  #
    ###############################
    def max_ingredient_length(self):
        max = 1
        for item in self.prices:
            if len(item) > max:
                max = len(item)
        return max

    def cart_count(self):
        return dict_size(self.cart)

    # Returns total price that is in the cart
    # If printing mode is on, then it prints each item, its count and price
    # Then prints the total price
    def cart_price(self, printing):
        if printing:
            item_name_width = self.max_ingredient_length() + 5
            count_width = 10
            unit_price_width = 15
            total_width = 10
            header = f"{'Item':<{item_name_width}}" \
                     f"{'Count':<{count_width}}" \
                     f"{'Unit Price':<{unit_price_width}}" \
                     f"{'Total':<{total_width}}"
            print('-' * len(header))
            print(header)
            print('-' * len(header))
            
        total_price = 0
        for item in self.cart:
            count = self.cart[item]
            item_price = self.prices[item]
            total = count*item_price
            if printing:
                print(f"{item:<{item_name_width}}"
                      f"{count:<{count_width}}"
                      f"{item_price:<{unit_price_width}}"
                      f"{total:<{total_width}}")
            total_price += total
        if printing:
            print('-' * len(header))
            print(f"Total: {total_price:.2f}$\n")
        return total_price