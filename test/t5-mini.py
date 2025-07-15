"""
MONDAY - Demo Template Version
...of a short text adventure demo featuring the opening sequence
"""

import time
import sys

def pause(prompt="Press Enter to continue..."):
    input(f"\n{prompt}")
    # Move cursor up and clear the line
    sys.stdout.write("\033[F")
    sys.stdout.write(" " * len(prompt) + "\r")
    sys.stdout.flush()

def wait(s=2.0):
    time.sleep(s)
    print()

def menu(title, options):
    print(f"\n{title}")
    for i, (label, _) in enumerate(options, 1):
        print(f"  {i}. {label}")
    while True:
        try:
            choice = int(input("Choose: "))
            if 1 <= choice <= len(options):
                return options[choice-1][1]
        except ValueError:
            pass
        print("Invalid choice. Try again.")

# Demo game state
state = {
    "running": True,
}
snooze_count = 0
pants_wet = False
has_money = False

def title_screen():
    print("\n" + "="*50)
    print("    A MODERN ADVENTURE OF EPIC PROPORTIONS")
    wait()
    print("\n    {}{}{}{}{}{}{}{}{}{}{}")
    print("   {{{{{{{{ MONDAY }}}}}}}}")
    print("    {}{}{}{}{}{}{}{}{}{}{}")
    print("\n       DEMO VERSION")
    print("="*50)
    pause()
    main_menu()

def main_menu():
    while state["running"]:
        choice = menu("-----MONDAY DEMO-----", [
            ("START DEMO", start_demo),
            ("ABOUT", about_demo),
            ("QUIT", quit_demo)
        ])
        if choice == about_demo:
            await choice()
            # unfortunately there seems no way simple enough to programmatically convert
            # this to async/await in Pyodide, so we just prepend `await` for select functions
        else:
            choice()

def about_demo():
    print("\nThis is a demo of MONDAY, a text adventure game.")
    print("You play as a high school student trying to survive")
    print("the worst day of the week... MONDAY!")
    print("\nThe full game features many more choices, locations,")
    print("and hilariously absurd death scenes.")
    pause()

def quit_demo():
    print("\nThanks for trying the MONDAY demo!")
    print("Remember: Monday has claimed another victim!")
    state["running"] = False
    return

def start_demo():
    print("\nDemo would start.")
    quit_demo()  # For now, just quit after starting

if __name__ == "__main__": # need to remove this line for Pyodide compatibility
    title_screen()