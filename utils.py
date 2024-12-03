"""
Here are utility functions that are used in some classes. All of these are
related to dicts
"""

# Given a dict and the type of the key (noun), print the dict
def dict_printer(d, key_title, value_title):
    if len(d) == 0:
        print("None")
        return
    
    max_length = 0
    for k in d:
        if len(k) > max_length:
            max_length = len(k)
    key_width = max_length + len(key_title)

    max_length = 0
    for v in d.values():
        if len(str(v)) > max_length:
            max_length = len(str(v))
    value_width = max_length + len(value_title)

    header = f"{key_title:<{key_width}}{value_title:<{value_width}}"
    print("-"*len(header))
    print(header)
    print("-"*len(header))
    for key in d:
        print(f"{key:<{key_width}}{d[key]:<{value_width}}")
    print()

# Given a dict, return its size based on values
def dict_size(d):
    count = 0
    for item in d:
        count += d[item]
    return count

# Add an element to a dict, being careful about capacity
def dict_increment(d, dsize, printing, to_add, verb=None, preposition=None, place=None, capacity=None):
    if capacity != None:
        if dsize >= capacity:
            if printing:
                print(f"Can't {verb} {to_add} because you don't have space {preposition} the {place}")
            return "fail"
    
    amount = d.get(to_add)
    if amount == None:
        d.update({to_add: 1})
    else:
        d[to_add] += 1

# Removing an element from a dict
def dict_decrement(d, to_remove, printing, verb=None, preposition=None, place=None):
    amount = d.get(to_remove)
    if amount == None:
        if printing:
            print(f"Can't {verb} {to_remove} because it's not {preposition} the {place}")
        return "fail"
    elif amount == 1:
        d.pop(to_remove)
    else:
        d[to_remove] -= 1

# Moves element from d1 to d2
# Need to check
#   - if d1 has to_move
#   - if d2 has space for to_move
#   - if so then move
#   - if both not true then don't move
def dict_move_element(d1, d2, d2_size, d2_capacity, to_move, to_move_size, verb=None, origin=None, destination=None):
    if to_move in d1:
        if d2_size + to_move_size <= d2_capacity:
            dict_decrement(d1, to_move, False)
            dict_increment(d2, d2_size, False, to_move)
            return "success"
        else:
            print(f"Can't {verb} {to_move} because the {destination} has no space")
    else:
        print(f"Can't {verb} {to_move} because the {origin} doesn't contain it")
    return "fail"