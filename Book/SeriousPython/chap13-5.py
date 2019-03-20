import contextlib

@contextlib.contextmanager
def MyContext():
    print("Do something first")
    yield
    print("Do something else")

with MyContext():
    print("Hello World")