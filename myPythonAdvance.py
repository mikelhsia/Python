#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
####################################################
# Advanced Python topic
####################################################

# Generators
# A generator "generates" values as they are requested instead of storing
# everything up front

# The following method (*NOT* a generator) will double all values and store it
# in `double_arr`. For large size of iterables, that might get huge!
def double_numbers(iterable):
    double_arr = []
    for i in iterable:
        double_arr.append(i + i)
    return double_arr


# Running the following would mean we'll double all values first and return all
# of them back to be checked by our condition
for value in double_numbers(range(1000000)):  # `test_non_generator`
    print value
    if value > 5:
        break


# ! Important !
# ############################
# We could instead use a generator to "generate" the doubled value as the item
# is being requested
def double_numbers_generator(iterable):
    for i in iterable:
        yield i + i


# ! Important !
# ############################
# Running the same code as before, but with a generator, now allows us to iterate
# over the values and doubling them one by one as they are being consumed by
# our logic. Hence as soon as we see a value > 5, we break out of the
# loop and don't need to double most of the values sent in (MUCH FASTER!)
for value in double_numbers_generator(xrange(1000000)):  # ! `test_generator` !
    print value
    if value > 5:
        break

# BTW: did you notice the use of `range` in `test_non_generator` and `xrange` in `test_generator`?
# Just as `double_numbers_generator` is the generator version of `double_numbers`
# We have `xrange` as the generator version of `range`
# `range` would return back and array with 1000000 values for us to use
# `xrange` would generate 1000000 values for us as we request / iterate over those items

# Just as you can create a list comprehension, you can create generator
# comprehensions as well.
values = (-x for x in [1, 2, 3, 4, 5])
for x in values:
    print(x)  # prints -1 -2 -3 -4 -5 to console/terminal

# You can also cast a generator comprehension directly to a list.
values = (-x for x in [1, 2, 3, 4, 5])
gen_to_list = list(values)
print(gen_to_list)  # => [-1, -2, -3, -4, -5]

# Decorators
# A decorator is a higher order function, which accepts and returns a function.
# Simple usage example – add_apples decorator will add 'Apple' element into
# fruits list returned by get_fruits target function.
def add_apples(func):
    def get_fruits():
        fruits = func()
        fruits.append('Apple')
        return fruits
    return get_fruits

@add_apples
def get_fruits():
    return ['Banana', 'Mango', 'Orange']

# Prints out the list of fruits with 'Apple' element in it:
# Banana, Mango, Orange, Apple
print ', '.join(get_fruits())

# in this example beg wraps say
# Beg will call say. If say_please is True then it will change the returned
# message
from functools import wraps


def beg(target_function):
    @wraps(target_function)
    def wrapper(*args, **kwargs):
        msg, say_please = target_function(*args, **kwargs)
        if say_please:
            return "{} {}".format(msg, "Please! I am poor :(")
        return msg

    return wrapper


@beg
def say(say_please=False):
    msg = "Can you buy me a beer?"
    return msg, say_please


print say()  # Can you buy me a beer?
print say(say_please=True)  # Can you buy me a beer? Please! I am poor :(

print "-------------"
import os
os.system('ls -la')

