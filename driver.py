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
                 launch_file="defaults/launch_screen.txt",
                 customer_interval=45, max_customers=5,
                 mode="timed"):
        subprocess.run('cls', shell=True)
        if player_name == None:
            player_name = input("Choose player name: ")
        self.game = CafeGame(player_name, starting_money, max_inventory, max_counter,
                             recipe_file, customer_names_file, pantry_file)
        self.max_customers = max_customers
        self.running = True
        self.modes = ["testing", "timed"]
        self.selected_mode = mode
        self.thread = Thread(target=self.customer_thread_function, args=(customer_interval, self.max_customers), daemon=True)
        self.launch_screen(launch_file)

    def start(self):
        if not self.game.check_file_formats():
            return
        if self.selected_mode not in self.modes:
            print(f"'{self.selected_mode}' is not an available mode")
            print(f"Choose from: {self.modes}")
            return
        
        if self.selected_mode == "timed":
            self.game.start_timer()
            self.thread.start()
        self.game.cafe.new_customer()

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
            ret = self.game.input_action(action)
            if self.selected_mode == "testing" and ret == "served":
                self.game.cafe.new_customer()
            
        self.end_message()

    def launch_screen(self, launch_file):
        print(f"Hi {self.game.chef.name}")

        with open(launch_file) as f:
            for line in f:
                print(line, end="")
        input()
        subprocess.run('cls', shell=True)
        
    def end_message(self):
        print("You have left the game. Here are your stats:")
        self.game.chef.get_stats()

    def customer_thread_function(self, interval, end):
        total_customers = 0
        while total_customers < end and self.running:
            elapsed = math.floor(time.time() - self.game.start_time)
            if elapsed % interval == 0 and elapsed != 0:
                self.game.cafe.new_customer()
                total_customers += 1
            time.sleep(1)

game = Driver()
game.start()