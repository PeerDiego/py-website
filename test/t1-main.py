# Simple Interactive Python Program
# This program will run in the browser and interact with users through the chat interface

print("🎉 Welcome to the Interactive Python Chat!")

import time

# Simple interaction test
name = input("What's your name? ")
print(f"Hello, {name.title()}! Nice to meet you! 👋")
time.sleep(3)

age = input("How old are you? ")
try:
    age_int = int(age)
    if age_int < 13:
        print("You're a kid! Enjoy your childhood.")
    elif 13 <= age_int < 20:
        print("You're a teenager! Exciting times ahead.")
    elif 20 <= age_int < 65:
        print("You're an adult! Keep striving for your goals.")
    else:
        print("You're a senior! Wisdom comes with age.")
except ValueError:
    print("That doesn't seem to be a valid age.")

print("This demonstrates Python input/output in the browser.")
print("END")