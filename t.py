import time
import re
#from states import *
import random
import math
import threading
from customer import Customer
from game_states.cafe import Cafe
from chef import Chef

chef = Chef("nathan", 20, 20, "defaults/recipes.txt")
c = Cafe(chef, 20, "defaults/customer_names.txt")

start = time.time()

def add_customer_interval(interval, end):
    used = []
    while len(used) <= end:
        elapsed = math.floor(time.time() - start)
        if elapsed not in used:
            if elapsed % interval == 0:
                c.new_customer()
                used.append(elapsed)

def aci():
    for _ in range(5):
        c.new_customer()
        time.sleep(2)

#thread = threading.Thread(target=add_customer_interval(2, 2))
thread = threading.Thread(target=aci)
thread.start()

print("done?")
time.sleep(2)
print("two seconds")