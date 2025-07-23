# EXAMPLE PYTHON CODE FOR INPUT HANDLING IN PYODIDE
# This code won't run locally, it's been transformed and is meant to be run in the browser with Pyodide.
# Once transformed, this is what the python code should look like to run properly in the browser w/ Piodide
print("[TEST 1] Input statement")
user_input = await input("Enter something: ")
print(f"You entered: {user_input}")

print("[TEST 2] Await outside async function scenario")
async def input_func():
    bla = await input("Enter something else: ")
    print(f"You entered: {bla}")
await input_func()

print("[TEST 3] Await outside async function scenario returning input()")
async def input_func_return():
    return await input("Enter yet something else: ")
xyz = await input_func_return()
print(f"You entered: {xyz}")