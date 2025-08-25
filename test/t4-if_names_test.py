t = {"block": 0}
expected_uncommented_code_blocks = 6
def block():
    t["block"] += 1
    print("Block count:", t["block"])
    if t["block"] == expected_uncommented_code_blocks:
        print("TEST SUCCESS")
    elif t["block"] > expected_uncommented_code_blocks:
        print("TEST FAILURE. Too many code blocks executed.")


def outer_function():
    print("In outer function")
    block()
    if True:
        print("In nested if")
        block()
        if __name__ == "__main__":
            print("This should be unindented")
            print("This too!")
            block()
            if True:
                print("This nested block should also be unindented")
                print("And this should be the last line!")
                block()
        elif __name__ == "__init__":
            print("This is in the nested elif")
            print("Should be commented out")
            block()
        else:
            print("This is in the nested else")
            print("Should also be commented out")
            block()
            another_function()

def another_function():
    print("Another function")
    block()

if __name__ == "__main__":
    print("Top level main block")
    print("Should be unindented")
    block()
    if True:
        print("Nested block in main")
        print("Also should be unindented")
        block()
        outer_function()
elif __name__ == "__init__":
    print("This is in the top-level elif")
    print("Should be commented out")
    another_function()
    block()
    if True:
        print("Nested block in elif")
        print("Should also be commented out")
        block()
else:
    print("This is in the top-level else")
    print("Should also be commented out")
    block()