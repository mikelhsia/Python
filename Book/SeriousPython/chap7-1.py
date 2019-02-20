# Writing Class Decorators
import uuid

_functions = {}

def register(f):
    global _functions
    _functions[f.__name__] = f
    return f

@register
def foo():
    return 'bar'


##########################################################################################
def check_is_admin(f):
    def wrapper(*args, **kwargs):
        if kwargs.get('username') != 'admin':
            raise Exception('This user is not allowed to get or put food')

def check_user_is_not(username):
    def user_check_decorator(f):
        def wrapper(*args, **kwargs):
            if kwargs.get('username') == username:
                raise Exception('This user is not allowed to get food')
            return f(*args, **kwargs)
        return wrapper
    return user_check_decorator

class Store(object):
    @check_user_is_not('admin')
    @check_user_is_not('user123')
    def get_food(self, username, food):
        return self.storage.get(food)

    @check_is_admin
    def put_food(self, username, food):
        return self.storage.put(food)


##########################################################################################
# Stacking decorators =
# Stores.get_food = check_user_is_not("user123")(Stores.get_food)
# Stores.get_food = check_user_is_not("admin")(Stores.get_food)
# In the example above, the program will check for admin first and then for user123.
class Stores(object):
    @check_user_is_not('admin')
    @check_user_is_not('user123')
    def get_food(self, username, food):
        return self.storage.get(food)

def set_class_name_and_id(klass):
    klass.name = str(klass)
    klass.random_id = uuid.uuid4()
    return klass

@set_class_name_and_id
class SomeClass(object):
    '''
    When the class is loaded and defined, it will set the name and random_id attributes, like so:
    SomeClass.name
    SomeClass.random_id
    '''
    pass

##########################################################################################
# Class decorators wrapping a function that's storing a state.
# The following example wraps the print() function to check how many times it has been called
class CountCalls(object):
    def __init__(self, f):
        self.f = f
        self.called = 0

    def __call__(self, *args, **kwargs):
        self.called += 1
        return self.f(*args, **kwargs)


@CountCalls
def print_hello():
    print("Hello~")

# >> print_hello.called
# 0
# >> print_hello()
# hello
# >> print_hello.called
# 1

##########################################################################################
"""
As mentioned, a decorator replaces the original function with a new one built 
on the fly. However, this new function lacks many of the attributes of the original 
function, such as its docstring and its name.
"""
def is_admin(f):
    def wrapper(*args, **kwargs):
        if kwargs.get('username') != 'admin':
            raise Exception("This user is not allowed to get food")
        return f(*args, **kwargs)
    return wrapper

def foobar(username="someone"):
    """
    Do crazy stuff.
    """
    pass

@is_admin
def foobar(username="someone"):
    """Do crazy stuff."""
    pass


# Retrieving Original Attributes with the update_wrapper Decorator
# Fortunately, the functools module in the Python Standard Library solves this problem with the update_
# wrapper() function, which copies the attributes from the original function that were lost to the wrapper itself.
WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__qualname__', '__doc__', '__annotations__')
WRAPPER_UPDATES = ('__dict__',)
def update_wrapper(wrapper, wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES):
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, attr, value)

    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))

    # Issue #17482: set __wrapped__ last so we don't inadvertently copy it
    # from the wrapped function when updating __dict__
    wrapper.__wrapped__ = wrapped
    # Return the wrapper so this can be used as a decorator via partial()
    return wrapper

# wraps: A Decorator for Decorators
import functools
def check_is_admin(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if kwargs.get('username') != 'admin':
            raise Exception("This user is not allowed to get food")
        return f(*args, **kwargs)
    return wrapper()

class Store(object):
    @check_is_admin
    def get_food(self, username, food):
        """Get food from storage"""
        return self.storage.get(food)

##########################################################################################
# Extracting Relevant Information with inspect
# Build a smarter version of decorator that can look at the decorated function's arguments
# and pull out what it needs
import functools
import inspect

def check_is_admin(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        func_args = inspect.getcallargs(f, *args, *kwargs)
        # returns a dictionary containing the names and values of the arguments as key-value pairs.
        # In our example, this function returns {'username': 'admin','type': 'chocolate'}.
        # That means that our decorator does not have to check whether the username parameter
        # is a positional or a keyword argument; all the decorator has to do is look for
        # username in the dictionary.
        if func_args.get('username') != 'admin':
            raise Exception("This user is not allowed to get food")
        return f(*args, **kwargs)
    return wrapper

@check_is_admin
def get_food(username, type='chocolate'):
    return type + " nom nom nom!"


##########################################################################################
# Static methods
# Class methods
# Abstract methods
class Pizza(object):
    cheese = 1
    vegetables = 2
    radius = 42

    def __init__(self, ingre=""):
        self.ingre = ingre

    @classmethod
    def from_fridge(cls, fridge):
        return cls(fridge.get_cheese() + fridge.get_vegetables())

    @classmethod
    def get_radius(cls):
        return cls.radius

    @staticmethod
    def mix_ingredients(x, y):
        return x + y

    def cook(self):
        return self.mix_ingredients(self.cheese, self.vegetables)

import abc

class BasePizza(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_radius(self):
        """
        Method that should do something
        :return:
        """

class SpecificPizza(BasePizza):
    def get_radius(self):
        print("Now you can see")


##########################################################################################
# Mixing Static, Class, Abstract methods
import abc


class BasePizza(object, metaclass=abc.ABCMeta):
    ingredients = ['cheese']

    @abc.abstractmethod
    def get_ingredients(self):
        """Returns the ingredient list."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_ingredients_list(cls):
        """Return the ingredient list"""
        return cls.ingredients

class Calzone(BasePizza):
    def get_ingredients(self, with_egg=False):
        egg = Egg() if with_egg else None
        return self.ingredients + [egg]


class DietPizza(BasePizza):
    @staticmethod
    def get_ingredients():
        return None

    # def get_ingredients(self):
    #     return 123

##########################################################################################
# Putting implementations in Abstract Methods
# You can put code in the abstract method, and in the subclass, you can use super() to call it
import abc


class BasePizza(object, metaclass=abc.ABCMeta):
    default_ingredients = ['cheese']

    @classmethod
    @abc.abstractmethod
    def get_ingredients(cls):
        """Returns the default ingredient list."""
        return cls.default_ingredients


class DietPizza(BasePizza):
    def get_ingredients(self):
        return [Egg()] + super(DietPizza, self).get_ingredients()
