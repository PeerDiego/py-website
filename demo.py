"""
MONDAY - Demo Version
A short text adventure demo featuring the opening sequence
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
    while True:
        choice = menu("-----MONDAY DEMO-----", [
            ("START DEMO", start_demo),
            ("ABOUT", about_demo),
            ("QUIT", quit_demo)
        ])
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
    exit()

def start_demo():
    print("\nYOU'RE IN BED, ASLEEP.")
    pause()
    print("IT'S 5:15 A.M.")
    pause()
    print("YOUR STEREO TURNS ON AND A LOCAL RADIO STATION")
    print("IS PLAYING A TERRIBLE SONG.")
    pause()
    print("WHAT A BAD WAY TO START A DAY!")
    pause()
    wakeup_menu()

def wakeup_menu():
    global snooze_count
    while True:
        choice = menu("  YOU WAKE UP   ", [
            ("SNOOZE", snooze),
            ("GET UP", get_up),
            ("SMASH STEREO", smash_stereo)
        ])
        if choice():
            break

def snooze():
    global snooze_count
    if snooze_count == 2:
        print("YOU'VE OVERSLEPT!")
        print("YOU MISS YOUR BUS AND TRY TO WALK TO SCHOOL.")
        print("OF COURSE YOU DON'T MAKE IT!")
        print("WHAT KIND OF GAME DO YOU THINK THIS IS?!?")
        game_over()
        return True
    print("ZZZZZ...")
    pause()
    snooze_count += 1
    print(f"(You've hit snooze {snooze_count} time(s))")
    return False

def smash_stereo():
    print("YOU GRAB YOUR BASEBALL BAT AND BEGIN DESTROYING YOUR STEREO.")
    print("IT IS NOW A PILE OF SPARE PARTS.")
    print("BUT YOU FORGOT ABOUT YOUR FRIEND'S CD.")
    print("AND HIS DAD IS A MOB KINGPIN!")
    print("OH CRAP!")
    game_over()
    return True

def get_up():
    print("YOU GET UP AND STRETCH.")
    print("AS YOU TAKE A DEEP BREATH, FOULNESS INVADES YOUR NOSTRILS.")
    print("THE FOULNESS COULD ONLY BE CAUSED BY ONE THING...")
    print("IT'S MONDAY!")
    pause()
    print("BUT YOU REALLY, REALLY GOTTA GO!")
    pause()
    bathroom_menu()
    return True

def bathroom_menu():
    choice = menu("   DO YOU GO?   ", [
        ("RELIEVE SELF", relieve_self), 
        ("HOLD IT IN", hold_it_in)
    ])
    choice()

def hold_it_in():
    global pants_wet
    print("YOU WET YOUR PANTS.")
    pants_wet = True
    pause()
    ed_mcmahon()

def relieve_self():
    print("AHHHHH...")
    pause()
    ed_mcmahon()

def ed_mcmahon():
    global has_money, pants_wet
    if not pants_wet:
        print("ED MCMAHON SHOWS UP AT YOUR DOOR!")
        print("HE SAYS YOU'VE WON 10 MILLION BUCKS!")
        print("WHOO-HOO!")
        print("YOU STUFF THE ENTIRE 10 MILLION BUCKS IN YOUR POCKET.")
        has_money = True
        pause()
        breakfast_demo()
    else:
        print("ED MCMAHON SHOWS UP AT YOUR DOOR!")
        print("HE SAYS YOU'VE WON 10 MILLION BUCKS!")
        print("BUT HE SEES YOUR PANTS AND IS DISGUSTED.")
        print("HE TAKES BACK THE MONEY AND LEAVES.")
        pause()
        game_over()

def breakfast_demo():
    print("Now you need to get ready for school...")
    print("But this is where the demo ends!")
    pause()
    print("\n" + "="*50)
    print("         DEMO COMPLETE!")
    print("="*50)
    print("\nIn the full game, you would continue with:")
    print("• Washing hands and eating breakfast")
    print("• Packing your school bag")
    print("• Catching the bus to school")
    print("• Navigating classes and social situations")
    print("• Making choices that affect your survival")
    print("• Discovering multiple endings")
    print("\nThe full game contains dozens of decision points")
    print("and hilariously unexpected death scenes!")
    pause()
    
    choice = menu("What would you like to do?", [
        ("PLAY AGAIN", start_demo),
        ("MAIN MENU", main_menu),
        ("QUIT", quit_demo)
    ])
    choice()

def game_over():
    print("\n" + "="*30)
    print("     GAME OVER")
    print("="*30)
    print("MONDAY HAS CLAIMED ANOTHER VICTIM!")
    print("TRY AGAIN!")
    pause()
    
    choice = menu("What now?", [
        ("TRY AGAIN", start_demo),
        ("MAIN MENU", main_menu),
        ("QUIT", quit_demo)
    ])
    choice()

if __name__ == "__main__":
    title_screen()