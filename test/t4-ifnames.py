def outer_function():
    print("In outer function")
    
    if True:
        print("In nested if")
        if __name__ == "__main__":
            print("This should be unindented")
            print("This too!")
            if True:
                print("This nested block should also be unindented")
                print("And this!")
        elif __name__ == "__init__":
            print("This is in the nested elif")
            print("Should be commented out")
        else:
            print("This is in the nested else")
            print("Should also be commented out")

def another_function():
    print("Another function")

if __name__ == "__main__":
    print("Top level main block")
    print("Should be unindented")
    if True:
        print("Nested block in main")
        print("Also should be unindented")
elif __name__ == "__init__":
    print("This is in the top-level elif")
    print("Should be commented out")
    if True:
        print("Nested block in elif")
        print("Should also be commented out")
else:
    print("This is in the top-level else")
    print("Should also be commented out")
