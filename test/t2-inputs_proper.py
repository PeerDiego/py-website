# EXAMPLE PYTHON CODE FOR INPUT HANDLING IN PYODIDE
# This code won't run locally, it's been transformed and is meant to be run in the browser with Pyodide.
# Once transformed, this is what the python code should look like to run properly in the browser w/ Piodide
print("[TEST 1] Input statement")
user_input = await input("Enter something: ")
print(f"You entered: {user_input}")

print("[TEST 2] Input statement in a function")
async def input_func():
    bla = await input("Enter something else: ")
    print(f"You entered: {bla}")
await input_func()

print("[TEST 3] Function returning await input() result")
async def input_func_return():
    return await input("Enter yet something else: ")
xyz = await input_func_return()
print(f"You entered: {xyz}")

# sleep commands
import time
print("[TEST 4] Time.sleep scenario")
print("Sleeping for 2 seconds...")
await time.sleep(2)
print("Awake now!")

# sleep command in a function
print("[TEST 5] Time.sleep in a function")
async def sleep_func():
    print("Sleeping for 3 second in a function...")
    await time.sleep(3)
    print("Function awake now!")
await sleep_func()
print("Function call completed.")