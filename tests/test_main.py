from main import greet

def test_greet():
    assert greet() == "Hello, world!"
    assert greet("Ada") == "Hello, Ada!"
