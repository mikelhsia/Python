"""
Chap 8
"""
"""
# purely functional
When you write code using a functional style, your functions are designed to have no side effects
Instead, they take the input and produce an output without keeping state or modifying anything not reflected in the return value
"""
def remove_last_item(mylist):
    """Removes the last item from a list"""
    # This modifies mylist
    mylist.pop(-1)

def butlast(mylist):
    """Pure version of the above function"""
    # This returns a copy of mylist
    return mylist[:-1]


"""
# Generators
"""
def mygenerator():
    yield 1
    yield 2
    yield 'a'


# A yield statement also has a less commonly used feature: it can return a value
# in the same way as a function call. This allows us to pass a value to a generator
# by calling its send() method.
def shorten(string_list):
    length = len(string_list[0])
    for s in string_list:
        length = yield s[:length]

mystringlist = ['loremipsum', 'dolorsit', 'ametfoobar']
shortstringlist = shorten(mystringlist)
result = []

try:
    s = next(shortstringlist)
    result.append(s)
    while True:
        number_of_vowels = len([v for v in filter(lambda letter: letter in 'aeiou', s)])
        # Truncate the next string depending
        # on the number of vowels in the previous one
        s = shortstringlist.send(number_of_vowels)
        result.append(s)
except StopIteration:
    pass


def consumer():
    r = 'here'
    while True:
        n1 = yield r
        if not n1:
            # print('[CONSUMER] n1 error then return')
            return
        print('[CONSUMER] Consuming %s...' % n1)
        r = '200 OK'+str(n1)

def produce(c):
    aa = c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r1 = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r1)
    c.close()

c = consumer()
produce(c)

import inspect

inspect.isgeneratorfunction(consumer)
inspect.getgeneratorstate(consumer)

x = [word.capitalize()
     for line in ("hello world?", "world!", "or not")
     for word in line.split()
     if not word.startswith("or")]

print(x)
# Functional Functions Functioning
map(lambda x: x + 'bzz!', ['I think', 'I\'m good'])
list(map(lambda x: x+ 'bzz!', ["I think", "I'm good"]))
a = (x + " bzz!" for x in ["I think", "I'm good"])
b = [x + " bzz!" for x in ["I think", "I'm good"]]

i = 0
mylist = [x for x in range(4)]
while i < len(mylist):
    print("Item %d: %s" % (i, mylist[i]))
    i += 1


for i, item in enumerate(mylist):
    print("Item %d: %s" % (i, item))


sorted([("a", 2), ("c", 1), ("d", 4)])
# Out[5]: [('a', 2), ('c', 1), ('d', 4)]
sorted([("a", 2), ("c", 1), ("d", 4)], key=lambda x : x[1])
# Out[6]: [('c', 1), ('a', 2), ('d', 4)]

mylist = [0, 1, 3, -1]
if all(map(lambda x: x>0, mylist)):
    print("All items are greater than 0")

if any(map(lambda x: x>0, mylist)):
    print("At least one item is greater than 0")

# As with the other functions described here, zip() returns an iterable in Python 3.
# Here we map a list of keys to a list of values to create a dictionary”
keys = ["foobar", "barzz", "ba!"]
list(zip(keys, map(len, keys)))
dict(zip(keys, map(len, keys)))


# Note that this may raise an IndexError if no items satisfy the condition, causing
# list(filter()) to return an empty list. # For simple cases, you can rely on next() to prevent IndexError
# from occurring, like so:
a = range(10)
next(x for x in a if x > 3)
# to prevent IndexError
next((x for x in a if x > 3), 'default')

# The functools package comes to the rescue with its partial() method, which provides us
# with a more flexible alternative to lambda. The functools.partial() method allows us to
# create a wrapper function with a twist: rather than changing the behavior of a function,
# it instead changes the arguments it receives, like so
from functools import partial
from first import first


def greater_than(number, min=0):
    return number > min


x = first([-1, 0, 1, 2], key=partial(greater_than, min=42))

# accumulate(iterable[, func]) returns a series of accumulated sums of items from iterables.
# chain(*iterables) iterates over multiple iterables, one after another, without building an intermediate list of all items.
# combinations(iterable, r) generates all combinations of length r from the given iterable.
# compress(data, selectors) applies a Boolean mask from selectors to data and returns only the values from data where the corresponding element of selectors is True.
# count(start, step) generates an endless sequence of values, starting with start and incrementing step at a time with each call.
# cycle(iterable) loops repeatedly over the values in iterable.
# repeat(elem[, n]) repeats an element n times.
# dropwhile(predicate, iterable) filters elements of an iterable starting from the beginning until predicate is False.
# groupby(iterable, keyfunc) creates an iterator that groups items by the result returned by the keyfunc() function.
# permutations(iterable[, r]) returns successive r-length permutations of the items in iterable.
# product(*iterables) returns an iterable of the Cartesian product of iterables without using a nested for loop.
# takewhile(predicate, iterable) returns elements of an iterable starting from the beginning until predicate is False.
