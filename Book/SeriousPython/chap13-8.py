import contextlib

@contextlib.contextmanager
def MyContext():
    print("Do something first")
    try:
        yield 42
    finally:
        print("Do something else")


with MyContext() as value:
    print("About to raise")
    raise ValueError("Let's try this")
    print(value)