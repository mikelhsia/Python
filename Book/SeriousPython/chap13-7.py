import contextlib

@contextlib.contextmanager
def MyContext():
    print("Do something first")
    yield 42
    print("Do something else")

with MyContext() as value:
    print(value)