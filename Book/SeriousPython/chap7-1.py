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
