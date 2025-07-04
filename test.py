"""
Test file for monday.py: Contains at least one instance of each unique Python command used in the game.
"""

import sys
import os
import time
import base64
import hashlib

print("[TEST 1] Print statement")
print("Hello, world!")

print("[TEST 2] Input statement")
user_input = input("Enter something: ")
# TODO: address current behavior
# when empty input is given, the browser shows "(empty input)"
# I want to ensure the game continues when the user is promprted to press Enter to continue...

print("[TEST 3] Variable assignment")
x = 42

print("[TEST 4] List usage")
lst = [1, 2, 3]
lst.append(4)

print("[TEST 5] Function definition and call")
def foo(a):
    return a * 2
result = foo(5)

print("[TEST 6] If/else")
if result > 5:
    print("Result is greater than 5")
else:
    print("Result is not greater than 5")

print("[TEST 7] While loop")
count = 0
while count < 2:
    print(f"Count: {count}")
    count += 1

print("[TEST 8] For loop")
for i in range(2):
    print(f"For loop: {i}")

print("[TEST 9] Try/except")
try:
    y = int("not a number")
except ValueError:
    print("Caught ValueError")

print("[TEST 10] Import and use a module")
print(os.name)

print("[TEST 11] Use sys.stdout.write and sys.stdout.flush")
sys.stdout.write("Flush this line\n") # writes to console.log()
sys.stdout.flush()

print("[TEST 12] Use time.sleep")
print("Sleeping...")
time.sleep(1) 
# TODO: address unexpected behavior in browser
# the wait is observed in the browser console, not in the Python output
# all subsequent python output to webpage between TEST 2 (input) and TEST 12 (time.sleep) is not displayed until after the sleep completes

print("[TEST 13] Use base64 and hashlib")
key = hashlib.sha256(b"secret").digest()
encoded = base64.urlsafe_b64encode(key)
print(f"Encoded key: {encoded}")

print("[TEST 14] Use global statement")
global_var = 0
def set_global():
    global global_var
    global_var = 1
set_global()
print(f"Global var: {global_var}")
# TODO: address unexpected behavior
# global variable is not update-able from within the funciton
# when printed, it remains unchanged at 0

print("[TEST 15] Use exit() (commented out)")
# exit()
# TODO: address unexpected behavior
# exit() crashes browser environment
# figure out how to override it and hook it into the "Program finished. Click "Run Python Program" to start again." scenario

print("[TEST 16] Use open/read/write file")
with open("testfile.txt", "w") as f:
    f.write("test")
with open("testfile.txt", "r") as f:
    print(f.read())

print("[TEST 17] Use class definition")
class Dummy:
    def __init__(self, val):
        self.val = val
    def get_val(self):
        return self.val
d = Dummy(7)
print(d.get_val())

print("[TEST 18] Use list comprehension")
squares = [i*i for i in range(3)]
print(squares)

print("[TEST 19] Use f-string")
name = "Monday"
print(f"Welcome to {name}!")

print("[TEST 20] Use pass statement")
def do_nothing():
    pass
do_nothing()

print("[TEST 21] Use break and continue in a loop")
for i in range(5):
    if i == 2:
        continue
    if i == 4:
        break
    print(f"Loop with break/continue: {i}")

print("[TEST 22] Use None")
none_var = None
if none_var is None:
    print("none_var is None")

print("[TEST 23] Use tuple")
my_tuple = (1, 2, 3)
print(my_tuple)

print("[TEST 24] Use dictionary")
d = {'a': 1, 'b': 2}
print(d['a'])

print("[TEST 25] Use enumerate")
for idx, val in enumerate(['a', 'b']):
    print(idx, val)

print("[TEST 26] Use lambda")
add = lambda a, b: a + b
print(add(2, 3))

print("[TEST 27] Use set")
my_set = {1, 2, 3}
print(my_set)

print("[TEST 28] Use assert")
assert 1 + 1 == 2

print("[TEST 29] Use isinstance")
print(isinstance(5, int))

print("[TEST 30] Use hasattr")
print(hasattr(d, 'a'))

print("[TEST 31] Use dir")
print(dir(d))

print("[TEST 32] Use sorted")
print(sorted([3, 1, 2]))

print("[TEST 33] Use reversed")
print(list(reversed([1, 2, 3])))

print("[TEST 34] Use min/max")
print(min([1, 2, 3]), max([1, 2, 3]))

print("[TEST 35] Use sum")
print(sum([1, 2, 3]))

print("[TEST 36] Use map/filter")
print(list(map(str, [1, 2, 3])))
print(list(filter(lambda x: x > 1, [1, 2, 3])))

print("[TEST 37] Use zip")
for a, b in zip([1, 2], ['a', 'b']):
    print(a, b)

print("[TEST 38] Use del")
x = [1, 2, 3]
del x[0]
print(x)

print("[TEST 39] Use raise")
try:
    raise Exception("Test exception")
except Exception as e:
    print(e)

print("[TEST 40] Use not, and, or")
if not False and (True or False):
    print("Logic works!")

print("[TEST 41] Use slice")
s = 'abcdef'
print(s[1:4])

print("[TEST 42] Use bytes")
b = b'abc'
print(b)

print("[TEST 43] Use chr/ord")
print(chr(65), ord('A'))

print("[TEST 44] Use any/all")
print(any([False, True]), all([True, True]))

print("[TEST 45] Use format")
print("{} {}".format('Hello', 'World'))

print("[TEST 46] Use repr")
print(repr('test'))

print("[TEST 47] Use len")
print(len([1, 2, 3]))

print("[TEST 48] Use round")
print(round(3.14159, 2))

print("[TEST 49] Use abs")
print(abs(-5))

print("[TEST 50] Use pow")
print(pow(2, 3))

print("[TEST 51] Use id")
print(id(x))

print("[TEST 52] Use hex")
print(hex(255))

print("[TEST 53] Use bin")
print(bin(7))

print("[TEST 54] Use oct")
print(oct(8))

print("[TEST 55] Use help (commented out)")
# help(print)
