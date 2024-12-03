from game_states.states import *

class Customer:
    def __init__(self, name="", order=""):
        self.name = name
        self.order = order
        self.arrival = round(time.time(), 1)

    def __eq__(self, value):
        return self.name == value.name and self.order == value.order

    def name_chooser(self, customer_names_file):
        with open(customer_names_file) as f:
            names = f.read().split()
        self.name = random.choice(names)

    def order_chooser(self, available_foods):
        self.order = random.choice(available_foods)
    
    def tip(self, departure):
        time_to_serve = round(departure - self.arrival, 1)
        print(f"It took you {time_to_serve}s to serve to {self.name}")
        multiplier = round(60/time_to_serve,1)
        return (random.randint(500, 1500) / 100)*multiplier