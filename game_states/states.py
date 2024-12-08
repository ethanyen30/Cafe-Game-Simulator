import re
import random
import time

from utils import *
from customer import Customer

class State:

    def __init__(self):
        """
        Regular expression for ingredients and food:
            - can be one word or more (ex. brown sugar, ex. tea)
            - all lowercase
            - only one space allowed in between if multiple words
            - no leading or trailing whitespace
        """
        self.noun_re = "(([a-z]+ )*[a-z]+)"

        """
        Regular expression for cooking verbs
            - just one word
            - all lower case
            - no leading or trailing whitespace
        """
        self.verb_re = "([a-z]+)"

    def do(self, chef, action, state):
        pass

    def get_help(self, state_name=None, instructions=None):
        print("\nHelp arrived:")
        print("- Any words left of the colon are commands you can type")
        print("- Anything in <> are variables so either ingredients, food, or customers\n")
        print("Remember as the chef, you can always do:")
        print("\tls:      lists inventory")
        print("\trecipes: view recipe book")
        print("\twallet:  see how much money you have\n")

        print(f"Here's what you can do in the {state_name}")
        dict_printer(instructions, "Commands", "Description")