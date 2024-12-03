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