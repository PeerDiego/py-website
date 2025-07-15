# This is a test scenario that requires transformation to async/await style for proper execution in the browser with Pyodide.
print("[TEST 1] Input statement")
user_input = input("Enter something: ")
print(f"You entered: {user_input}")

print("[TEST 2] Input statement in a function")
def input_func():
    bla = input("Enter something else: ")
    print(f"You entered: {bla}")
input_func()

print("[TEST 3] Function returning input() result")
def input_func_return():
    return input("Enter yet something else: ")
xyz = input_func_return()
print(f"You entered: {xyz}")

# sleep commands
import time
print("[TEST 4] Time.sleep scenario")
print("Sleeping for 2 seconds...")
time.sleep(2)
print("Awake now!")

# sleep command in a function
print("[TEST 5] Time.sleep in a function")
def sleep_func():
    print("Sleeping for 3 second in a function...")
    time.sleep(3)
    print("Function awake now!")
sleep_func()
print("Function call completed.")