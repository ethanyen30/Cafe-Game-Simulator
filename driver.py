from cafegame import CafeGame
import subprocess
from threading import Thread
import math
import time

class Driver:
    def __init__(self, player_name=None, starting_money=15, max_inventory=5, max_counter=10,
                 recipe_file="defaults/recipes.txt", 
                 customer_names_file="defaults/customer_names.txt", 
                 pantry_file="defaults/pantry.txt",
                 customer_interval=45, max_customers=5):
        subprocess.run('cls', shell=True)
        if player_name == None:
            player_name = input("Choose player name: ")
        self.game = CafeGame(player_name, starting_money, max_inventory, max_counter,
                             recipe_file, customer_names_file, pantry_file)
        self.max_customers = max_customers
        self.launch_screen()
        self.running = True
        self.thread = Thread(target=self.customer_thread_function, args=(customer_interval, self.max_customers), daemon=True)
    
    def start(self):
        if not self.game.check_file_formats():
            return
        
        self.thread.start()

        while self.running:
            if self.game.chef.customers_fed == self.max_customers:
                self.running = False
                continue
            action = input("~> ")
            if action == "":
                continue
            if action == "exit":
                self.running = False
                continue
            self.game.input_action(action)
        self.end_message()

    def launch_screen(self):
        print(f"Hi {self.game.chef.name}")
        print("You are playing a text-based restaurant simulator game")
        print("...")
        print("Press enter to start")
        input()
        subprocess.run('cls', shell=True)
        
    def end_message(self):
        print("You have left the game. Here are your stats:")
        self.game.chef.get_stats()

    def customer_thread_function(self, interval, end):
        used = []
        while len(used) < end and self.running:
            elapsed = math.floor(time.time() - self.game.start_time)
            if elapsed not in used:
                if elapsed % interval == 0:
                    self.game.cafe.new_customer()
                    used.append(elapsed)
            time.sleep(1)

game = Driver()
game.start()