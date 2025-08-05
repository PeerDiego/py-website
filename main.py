"""
MONDAY - Demo Version
A short text adventure demo featuring the opening sequence meant as an example program for this project.
"""

import time
import sys

def pause(prompt="Press Enter to continue..."):
    input(prompt)

def wait(s=2.0):
    time.sleep(s)
    # print()

def menu(title, options):
    menu_text = f"\n{title}"
    for i, (label, _) in enumerate(options, 1):
        menu_text += f"\n  {i}. {label}"
    print(menu_text, "\n\n")
    while True:
        try:
            choice = int(input("Choose: "))
            if 1 <= choice <= len(options):
                return options[choice-1][1]
        except ValueError:
            pass
        print("Invalid choice. Try again.")

# Play count tracking functions
def get_demo_stats():
    """Get the demo statistics data from storage, or empty dict if none exists"""
    return load_data("monday_demo_stats") or {}

def get_play_count():
    """Get the number of times the demo has been played"""
    play_data = get_demo_stats()
    return play_data.get("play_count", 0)

def get_completion_count():
    """Get the number of times the demo has been completed"""
    play_data = get_demo_stats()
    return play_data.get("completion_count", 0)

def increment_play_count():
    """Increment and save the play count"""
    play_data = get_demo_stats()
    play_data["play_count"] = play_data.get("play_count", 0) + 1
    save_data(play_data, "monday_demo_stats")
    return play_data["play_count"]

def increment_completion_count():
    """Increment and save the completion count"""
    play_data = get_demo_stats()
    play_data["completion_count"] = play_data.get("completion_count", 0) + 1
    save_data(play_data, "monday_demo_stats")
    return play_data["completion_count"]

def clear_play_count():
    """Clear the play count and completion count (reset stats)"""
    clear_data("monday_demo_stats")
    print("Demo statistics cleared!")

# Demo game state
# This allows us to maintain state across different functions without needing to declare them as global.
# This is a workaround for the limitations of Pyodide's handling of global variables.
state = {
    "running": True,
    "snooze_count": 0,
    "pants_wet": False,
    "has_money": False,
}

def title_screen():
    print("="*40)
    print("A MODERN ADVENTURE OF EPIC PROPORTIONS")
    wait()
    print("         {}{}{}{}{}{}{}{}{}{}{}")
    print("       {{{{{{{{ MONDAY }}}}}}}}")
    print("        {}{}{}{}{}{}{}{}{}{}{}")
    print("\n              DEMO VERSION")
    print(" ", "="*34)
    pause()
    main_menu()

def main_menu():
    while state["running"]:
        choice = menu("-----MONDAY DEMO-----", [
            ("START DEMO", start_demo),
            ("ABOUT", about_demo),
            ("CLEAR STATS", clear_stats),
            ("QUIT", quit_demo)
        ])
        # unfortunately there seems no way simple enough to programmatically convert
        # this to async/await in Pyodide, so we just prepend `await` for select functions
        # y'know what, let's just make everything async for consistency...
        await choice()

def clear_stats():
    play_count = get_play_count()
    completion_count = get_completion_count()
    
    if play_count > 0 or completion_count > 0:
        print(f"\nYour current statistics:")
        print(f"  • Played: {play_count} time(s)")
        print(f"  • Completed: {completion_count} time(s)")
        
        confirm = input("Are you sure you want to clear your statistics? (y/n): ")
        if confirm.lower() in ['y', 'yes']:
            clear_play_count()
        else:
            print("Statistics kept.")
    else:
        print("\nNo statistics to clear!")
    pause()

def about_demo():
    play_count = get_play_count()
    completion_count = get_completion_count()
    
    print("\nThis is a demo of MONDAY, a text adventure game.")
    print("You play as a late 90's high school student trying to survive")
    print("the worst day of the week... MONDAY!")
    print("\nThe full game features many more choices, locations,")
    print("and hilariously absurd death scenes.")
    
    # Show statistics
    if play_count > 0:
        if play_count == 1:
            print(f"\n📊 You've played this demo {play_count} time.")
        else:
            print(f"\n📊 You've played this demo {play_count} times.")
        
        if completion_count > 0:
            if completion_count == 1:
                print(f"🏆 You've completed it {completion_count} time.")
            else:
                print(f"🏆 You've completed it {completion_count} times.")
            
            completion_rate = (completion_count / play_count) * 100
            print(f"📈 Completion rate: {completion_rate:.0f}%")
        else:
            print("🎯 You haven't completed the demo yet. Give it a try!")
        
        # Fun milestone messages
        if completion_count >= 3:
            print("🌟 Demo master! You really know how to avoid Monday's traps!")
        elif completion_count >= 1:
            print("✨ Great job completing the demo!")
            
        if play_count >= 5:
            print("🎉 Wow, you really like this demo!")
        elif play_count >= 3:
            print("😄 You're getting the hang of this!")
    else:
        print("\n📊 This is your first time playing the demo. Welcome!")
    
    pause()

def quit_demo():
    print("\nThanks for trying the MONDAY demo!")
    print("Remember: Monday has claimed another victim!")
    state["running"] = False
    wait(1)
    return

def start_demo():
    # Increment play count when starting a new demo
    play_count = increment_play_count()
    
    state["pants_wet"] = False
    state["has_money"] = False
    state["snooze_count"] = 0
    
    if play_count == 1:
        print("\n🎮 Welcome to your first Monday demo!")
    else:
        print(f"\n🎮 Welcome back! This is play #{play_count}")
    
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
    while True:
        choice = menu("  YOU WAKE UP   ", [
            ("SNOOZE", snooze),
            ("GET UP", get_up),
            ("SMASH STEREO", smash_stereo)
        ])
        if await choice():
            break

def snooze():
    if state["snooze_count"] == 2:
        print("YOU'VE OVERSLEPT!")
        print("YOU MISS YOUR BUS AND TRY TO WALK TO SCHOOL.")
        print("OF COURSE YOU DON'T MAKE IT!")
        print("WHAT KIND OF GAME DO YOU THINK THIS IS?!?")
        game_over()
        return True
    print("ZZZZZ...")
    pause()
    state["snooze_count"] += 1
    print(f"(You've hit snooze {state['snooze_count']} time(s))")
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
    # Both relieve_self and hold_it_in need async
    await choice()

def hold_it_in():
    print("YOU WET YOUR PANTS.")
    state["pants_wet"] = True
    pause()
    ed_mcmahon()

def relieve_self():
    print("AHHHHH...")
    pause()
    ed_mcmahon()

def ed_mcmahon():
    if not state["pants_wet"]:
        print("ED MCMAHON SHOWS UP AT YOUR DOOR!")
        print("HE SAYS YOU'VE WON 10 MILLION BUCKS!")
        print("WHOO-HOO!")
        print("YOU STUFF THE ENTIRE 10 MILLION BUCKS IN YOUR POCKET.")
        state["has_money"] = True
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
    # Increment completion count when demo is completed
    completion_count = increment_completion_count()
    
    print("Now you need to get ready for school...")
    print("But this is where the demo ends!")
    pause()
    print("\n" + "="*50)
    print("         DEMO COMPLETE!")
    print("="*50)
    
    # Show completion message
    if completion_count == 1:
        print(f"\n🎉 Congratulations! You completed the Monday demo!")
        print("🏆 This is your first completion!")
    else:
        print(f"\n🎉 Demo completed! This is completion #{completion_count}!")
        if completion_count >= 3:
            print("🌟 You're becoming a Monday survival expert!")
    
    print("\nIn the full game, you would continue with:")
    print("• Washing hands and eating breakfast")
    print("• Packing your school bag")
    print("• Catching the bus to school")
    print("• Navigating classes and social situations")
    print("• Making choices that affect your survival")
    print("• Discovering multiple endings")
    print("\nThe full game contains dozens of decision points")
    print("and hilariously unexpected death scenes!")
    print("\nPlay the full game at: https://lazyspaniard.com/monday/")
    pause()
    
    choice = menu("What would you like to do?", [
        ("PLAY AGAIN", start_demo),
        ("MAIN MENU", main_menu),
        ("QUIT", quit_demo)
    ])
    await choice()

def game_over():
    print(" " + "="*30)
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
    await choice()

if __name__ == "__main__": # need to remove this line for Pyodide compatibility
    title_screen()