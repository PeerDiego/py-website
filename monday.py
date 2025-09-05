"""
MONDAY - A Text Adventure Game
Originally written in TI-BASIC, converted to Python
Copyright (c) 2001, 2025

A humorous adventure where you try to survive a Monday morning at high school.
Make increasingly bizarre choices while trying to make it through what might 
be the worst Monday ever. Features multiple endings, dark humor, and 
callbacks to classic 90's pop culture.

Features:
- Choice-based gameplay with branching paths
- Multiple endings including a secret "good" ending
- Persistent stats and achievements
- Modern Python implementation with save functionality
"""

#---------------------------------------
# Core Imports
#---------------------------------------
import os
import sys
import time
import json
import base64
import hashlib

#---------------------------------------
# Optional Features & Environment Setup
#---------------------------------------
# Check for Pyodide (browser) environment
try:
    PYODIDE_ENV = globals().get('PYODIDE_ENV', False)
    # print("Running in Pyodide environment." if PYODIDE_ENV else "Running in standard Python environment.")
except NameError:
    print("Assuming standard Python environment.")
    PYODIDE_ENV = False

# Setup save/load capability
try:
    from cryptography.fernet import Fernet, InvalidToken
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    if not PYODIDE_ENV:
        print("Note that progress will not be saved.")

#---------------------------------------
# Game State Management
#---------------------------------------

state = {
    # Core Statistics
    "times_played"      : 0,  # Number of times game has been played
    "times_won"         : 0,  # Number of times player has won
    "times_good_ending" : 0,  # Number of times player got the good ending
    "hints_seen"        : 0,  # Number of unique hints the player has viewed
    "total_choices"     : 0,  # Total number of choices made
    "choices_count"     : 0,  # Choices made in current session
    
    # Death Tracking
    "deaths": {
        "oversleeping": {
            "discovered": False,
            "description": "Overslept and missed the bus",
            "count": 0
        },
        "mob_hit": {
            "discovered": False,
            "description": "Smashed stereo containing mob boss's CD",
            "count": 0
        },
        "anvil": {
            "discovered": False,
            "description": "Found government secrets and met an anvil",
            "count": 0
        },
        "electrocution": {
            "discovered": False,
            "description": "Tried to get Pop-Tart out with a fork",
            "count": 0
        },
        "broken_jaw": {
            "discovered": False,
            "description": "Broke jaw on frozen pizza",
            "count": 0
        },
        "no_hygiene": {
            "discovered": False,
            "description": "Didn't brush teeth before packing bag",
            "count": 0
        },
        "skip_breakfast": {
            "discovered": False,
            "description": "Skipped the most important meal of the day",
            "count": 0
        },
        "unwashed_breakfast": {
            "discovered": False,
            "description": "Ate breakfast with unwashed hands",
            "count": 0
        },
        "starvation": {
            "discovered": False,
            "description": "Forgot school supplies and starved to death",
            "count": 0
        },
        "psycho": {
            "discovered": False,
            "description": "Met a psycho in Monica Lewinsky mask",
            "count": 0
        },
        "mcdonalds_fry": {
            "discovered": False,
            "description": "Heart attack from one McDonald's fry",
            "count": 0
        },
        "sun_blindness": {
            "discovered": False,
            "description": "Blinded by sun while crossing street",
            "count": 0
        },
        "live_tuna": {
            "discovered": False,
            "description": "Eaten by live tuna sandwich at airport",
            "count": 0
        },
        "iraq_guards": {
            "discovered": False,
            "description": "Mistaken for assassin in Iraq",
            "count": 0
        },
        "donkey_kong": {
            "discovered": False,
            "description": "Thrown into oblivion by Donkey Kong",
            "count": 0
        },
        "hostage_fail": {
            "discovered": False,
            "description": "Failed to help TI-83 hostage situation",
            "count": 0
        },
        "walk_texas": {
            "discovered": False,
            "description": "Tried walking home from Texas",
            "count": 0
        },
        "book_indigestion": {
            "discovered": False,
            "description": "Severe indigestion from eating alien book",
            "count": 0
        },
        "math_fail": {
            "discovered": False,
            "description": "Failed basic math in Area 51",
            "count": 0
        },
        "toilet_flush": {
            "discovered": False,
            "description": "Flushed down Area 51 toilet",
            "count": 0
        },
        "toilet_drink": {
            "discovered": False,
            "description": "Drank from Area 51 toilet",
            "count": 0
        },
        "toxic_nap": {
            "discovered": False,
            "description": "Napped in toxic Area 51 bathroom",
            "count": 0
        },
        "alien_blood": {
            "discovered": False,
            "description": "Dissolved by alien's acidic blood",
            "count": 0
        },
        "ymca_smack": {
            "discovered": False,
            "description": "Smacked for singing YMCA with aliens",
            "count": 0
        },
        "alien_dance": {
            "discovered": False,
            "description": "Died of embarrassment dancing with aliens",
            "count": 0
        },
        "final_loser": {
            "discovered": False,
            "description": "Gave up at the very end",
            "count": 0
        },
        "hand_falls_off": {
            "discovered": False,
            "description": "Hand fell off writing essay",
            "count": 0
        },
        "reject_girl": {
            "discovered": False,
            "description": "Said 'hell no' to the girl",
            "count": 0
        },
        "methane_gas": {
            "discovered": False,
            "description": "Choked on methane gas in library",
            "count": 0
        },
        "mad_cow": {
            "discovered": False,
            "description": "Got mad cow disease from beef taco",
            "count": 0
        },
        "salmonella": {
            "discovered": False,
            "description": "Got salmonella from chicken",
            "count": 0
        },
        "seizure": {
            "discovered": False,
            "description": "Had seizure from computer screen",
            "count": 0
        },
        "acid_face": {
            "discovered": False,
            "description": "Face fell in hydrochloric acid",
            "count": 0
        },
        "refused_donut": {
            "discovered": False,
            "description": "Refused to give donut to linebacker",
            "count": 0
        },
        "monday_revenge": {
            "discovered": False,
            "description": "Hit with Monday's best shot",
            "count": 0
        },
        "car_accident": {
            "discovered": False,
            "description": "Ran to bus without looking both ways",
            "count": 0
        },
        "cement": {
            "discovered": False,
            "description": "Sat in wet cement at bus stop",
            "count": 0
        },
        "spiteful_driver": {
            "discovered": False,
            "description": "Mooned the bus driver",
            "count": 0
        },
        "bad_neighborhood": {
            "discovered": False,
            "description": "Fell asleep on bus in bad neighborhood",
            "count": 0
        },
        "lost_forever": {
            "discovered": False,
            "description": "Got lost in school halls forever",
            "count": 0
        },
        "brain_overheat": {
            "discovered": False,
            "description": "Brain overheated from studying",
            "count": 0
        },
        "computer_explosion": {
            "discovered": False,
            "description": "Computer exploded checking email",
            "count": 0
        },
        "choked_tongue": {
            "discovered": False,
            "description": "Choked on tongue during speed debate",
            "count": 0
        },
        "gameboy_rage": {
            "discovered": False,
            "description": "Died from Gameboy rage after batteries died",
            "count": 0
        },
        "annie_cd": {
            "discovered": False,
            "description": "Jumped from bus after hearing Annie soundtrack",
            "count": 0
        },
        "buffalo_stampede": {
            "discovered": False,
            "description": "Run down by raging buffalo with dream girl",
            "count": 0
        },
        "alien_abduction": {
            "discovered": False,
            "description": "Abducted by aliens walking home",
            "count": 0
        },
        "bus_window": {
            "discovered": False,
            "description": "Thrown out bus window for no reason",
            "count": 0
        },
        "quit_early": {
            "discovered": False,
            "description": "Tried to go home early",
            "count": 0
        },
        "airport_quit": {
            "discovered": False,
            "description": "Tried to go home from airport",
            "count": 0
        },
        "texas_karma": {
            "discovered": False,
            "description": "Bad karma caught up in Texas",
            "count": 0
        }
    }
}

def record_death(death_type):
    """Record a death of a specific type in the game state"""
    if death_type in state["deaths"]:
        if not state["deaths"][death_type]["discovered"]:
            state["deaths"][death_type]["discovered"] = True
            print(f"\nNew death discovered: {state['deaths'][death_type]['description']}")
        state["deaths"][death_type]["count"] += 1
    else:
        print(f"Death cause '{death_type}' not found :(   Please tell the dev.")

def reset_saved_stats():
    state["times_played"]      = 0
    state["times_won"]         = 0
    state["times_good_ending"] = 0
    state["hints_seen"]        = 0
    state["total_choices"]     = 0
    state["choices_count"]     = 0
    # Reset death tracking
    for death in state["deaths"]:
        state["deaths"][death]["discovered"] = False
        state["deaths"][death]["count"] = 0

def initialize_game_state():
    """Reset the game state to default values for a new game."""
    state["running"] = True
    state["snooze_count"] = 0
    state["pants_wet"] = False
    state["cash"] = 0
    state["ti-83_confiscated"] = False
    state["has_money"] = False
    state["insists_on_going_home"] = 0  # insists on going home at end of day; bypass win route
initialize_game_state()

#---------------------------------------
# Core Game Utilities
#---------------------------------------

def pause(prompt = "Press Enter to continue..."):
    if PYODIDE_ENV:
        wait()
    elif not PYODIDE_ENV:
        # Print prompt, wait for Enter, then overwrite the prompt line with spaces
        input(prompt)  # Removed the \n to keep the prompt on same line
        # Move cursor up one line and clear it - not needed for web version
        sys.stdout.write("\033[F")  # Move cursor up one line
        sys.stdout.write(" " * len(prompt) + "\r")  # Overwrite with spaces
        sys.stdout.flush()

def wait(s=2.0):
    """Wait for specified number of seconds."""
    time.sleep(s)

def menu(title, options, count_choice=True):
    menu_text = f"\n{title}"
    for i, (label, _) in enumerate(options, 1):
        menu_text += f"\n  {i}. {label}"
    print(menu_text, "\n\n")
    
    while state["running"]:
        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= len(options):
                if count_choice:
                    state["choices_count"] += 1  # Increment choice counter
                    state["total_choices"] += 1  # Increment perma choice counter
                    save_stats()  # Save progress
                return options[choice-1][1]
        except ValueError:
            pass
        print("Invalid choice. Try again.")

#---------------------------------------
# File Save/Load System Configuration
#---------------------------------------
SAVE_FILE = "monday_save.dat"
SECRET = "monday_secret_key_2025"

# List of state keys that should be saved/loaded
SAVEABLE_STATS = [
    "times_played",
    "times_won",
    "times_good_ending",
    "hints_seen",
    "total_choices",
    "deaths"
]

def get_fernet():
    """Initialize encryption for save files."""
    if not CRYPTO_AVAILABLE:
        raise RuntimeError("Cryptography not available")
    # Derive a 32-byte key from SECRET
    key = hashlib.sha256(SECRET.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))


#---------------------------------------
# Save/Load System Implementation 
#---------------------------------------

def save_stats():
    """Save game statistics to persistent storage"""
    # Prepare the stats to be saved
    saveable_data = {k: state[k] for k in SAVEABLE_STATS}
    
    if PYODIDE_ENV:
        # Use browser's localStorage via Pyodide bridge
        success = save_data(saveable_data, "monday_stats")
    else:
        # Use local file encryption
        if not CRYPTO_AVAILABLE:
            return
        f = get_fernet()
        data = json.dumps(saveable_data).encode()
        token = f.encrypt(data)
        with open(SAVE_FILE, "wb") as file:
            file.write(token)

def load_stats():
    """Load game statistics from persistent storage"""
    if PYODIDE_ENV:
        # Load from browser's localStorage
        loaded_data = load_data("monday_stats") or {}
    else:
        # Load from encrypted local file
        if not CRYPTO_AVAILABLE or not os.path.exists(SAVE_FILE):
            return
        try:
            f = get_fernet()
            with open(SAVE_FILE, "rb") as file:
                token = file.read()
            data = f.decrypt(token).decode()
            try:
                # Try loading as JSON first
                loaded_data = json.loads(data)
            except json.JSONDecodeError:
                # Fall back to old CSV format
                stats = [int(x) for x in data.split(",")]
                loaded_data = {
                    "times_played": stats[0],
                    "times_won": stats[1],
                    "times_good_ending": stats[2],
                    "hints_seen": stats[3] if len(stats) > 3 else 0,
                    "total_choices": stats[4] if len(stats) > 4 else 0
                }
        except Exception as e:
            print("Error loading save file:", e)
            reset_saved_stats()
            return

    def deep_update(target, source):
        """Recursively update nested dictionaries."""
        for key, value in source.items():
            if key in target:
                if isinstance(value, dict) and isinstance(target[key], dict):
                    deep_update(target[key], value)
                else:
                    target[key] = value
        return target

    # Update existing state with saved values instead of replacing
    for key, value in loaded_data.items():
        if key in state:
            if isinstance(value, dict) and isinstance(state[key], dict):
                deep_update(state[key], value)
            else:
                state[key] = value

def clear_stats():
    """Clear game statistics from persistent storage"""
    reset_saved_stats()
    if PYODIDE_ENV:
        # Clear browser storage
        clear_data("monday_stats")
        print("Save cleared.", msg_type='system')
        wait(1) # Needed for Pyodide to process to comply with cascading awaits from menu()'s `choice()`
    else:
        # Delete local save file
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        print("Save cleared.")
    save_stats()
    
def title_screen():
    print("\nA MODERN ADVENTURE OF EPIC PROPORTIONS\n")
    wait(1.5)
    print("    {}{}{}{}{}{}{}{}{}{}{}\n   {{{{{{{{ MONDAY }}}}}}}}\n    {}{}{}{}{}{}{}{}{}{}{}\n")
    wait(1.5)
    print("       SPECIAL EDITION\n\n")
    wait(1.5)
    pause()
    main_menu()

def main_menu():
    while state["running"]:
        choice = menu("-----MONDAY-----", [
            ("PLAY GAME", play_game),
            ("BACKGROUND", background),
            ("HINTS", hints),
            ("POINTLESS INFO", pointless_info),
            ("ABOUT", about),
            ("CLEAR STATS", clear_stats),
            ("QUIT GAME", quit_game)
        ], count_choice=False)
        choice()
    print("Thanks for playing!")

def pointless_info():
    def once_or_x_times(integer, end_punctutation="."):
        return ("ONCE" if integer == 1 else f"{integer} TIMES") + end_punctutation
    wait_coefficient = 1.0 - min(state["times_played"] // 10, 5) * 0.18
    print("\nHERE'S SOME USELESS INFORMATION.")
    pause()
    print("YOU HAVE PLAYED THIS GAME", once_or_x_times(state["times_played"]))
    wait(1 * wait_coefficient)
    if state["times_played"] == 0:
        print("WHAT ARE YOU WAITING FOR? START THE GAME.")
        if state["hints_seen"]:
            wait(1 * wait_coefficient)
            print("\nWAIT! YOU CHECKED OUT HINTS BEFORE EVEN TRYING THE GAME?? HOW LAME. ┑(￣Д ￣)┍")
            wait(4 * wait_coefficient)
        return
    if state["choices_count"]:
        print(F"YOU HAVE MADE {state['choices_count']} CHOICE{'' if state['choices_count'] == 1 else 'S'} THIS ROUND.")
    wait(1 * wait_coefficient)
    if state["total_choices"] and state["total_choices"] != state["choices_count"]:
        print(F"YOU HAVE MADE {state['total_choices']} CHOICE{'' if state['total_choices'] == 1 else 'S'}{', IN TOTAL' if state['choices_count'] != 0 else ''}.")
    wait(1 * wait_coefficient)
    print(f"YOU HAVE WON", once_or_x_times(state["times_won"]), 
          " >_> <_<" if state['times_won'] > state['times_played'] else "")
    wait(1 * wait_coefficient)
    if state["hints_seen"]:
            print(F"YOU HAVE VIEWED {'ONLY ONE' if state['hints_seen'] == 1 else state['hints_seen']} HINT{'' if state['hints_seen'] == 1 else 'S'}.")
    wait(1.5 * wait_coefficient)
    if state['times_good_ending'] > 0:
        print("AND YOU ACTUALLY WON", once_or_x_times(state["times_good_ending"], end_punctutation="!"), "NOT THAT FAKE PARTICIPATION MEDAL WIN.")
        wait(1 * wait_coefficient)
        if state["total_choices"] == 40:
            print("WOW! YOU SMASHED THE GOOD ENDING IN THE MINIMUM POSSIBLE CHOICES!")
            wait(3 * wait_coefficient)
            print("YOU F***ING ROCK!!!")
            wait(4 * wait_coefficient)
        elif state["total_choices"] == 42:
            print("WOW! YOU FORCED THE GOOD ENDING IN ALMOST THE LEAST AMOUNT OF CHOICES!")
            print("THINK YOU CAN DO IT IN LESS?")
            wait(3 * wait_coefficient)
        if state["hints_seen"] == 0:
            print("HOLY CRAP! AND YOU DID IT WITHOUT ANY HINTS! IMPRESSIVE!!")
            wait()
    
    # Show death statistics
    total_deaths = len(state["deaths"])
    discovered_deaths = sum(1 for death in state["deaths"].values() if death["discovered"])
    if discovered_deaths == 0 and state["times_played"]:
        wait(1 * wait_coefficient)
        print("\nYOU HAVEN'T DISCOVERED ANY DEATHS YET. WHAT KIND OF MONDAY PLAYER ARE YOU?")
        print("THERE ARE SO MANY WAYS TO DIE, AND YOU HAVEN'T FOUND A SINGLE ONE! ¯\\_(ツ)_/¯")
    elif discovered_deaths == total_deaths:
        wait(1 * wait_coefficient)
        print("\nINCREDIBLE! YOU'VE DISCOVERED EVERY POSSIBLE WAY TO DIE!")
        print("YOU ARE THE ULTIMATE MASTER OF MONDAY MAYHEM! (╯°□°）╯︵ ┻━┻")
    if discovered_deaths > 0:
        print(f"\nYOU'VE DISCOVERED {discovered_deaths} UNIQUE WAY{'S' if discovered_deaths !=1 else ''} TO DIE!")
        wait(1 * wait_coefficient)
        for death_type, info in state["deaths"].items():
            if info["discovered"]:
                print("-", info['description'].upper(), once_or_x_times(info['count'], end_punctutation=""))
                wait(0.5 * wait_coefficient)
        wait(1 * wait_coefficient)
    
    if state['times_won'] == 0:
        if state['total_choices'] > 20:
            print("\nYOU'RE WELL ON YOUR WAY. KEEP GOING!")
        elif state['times_played']:
            print("\nKEEP ON TRYING.")
    elif (state['times_won'] or state['times_played']) and not state['times_good_ending']:
        print("YOU'RE GETTING THE HANG OF IT.")
    wait(1 * wait_coefficient)
    # Return to main menu

def hints():
    choice = menu("  WANT A HINT?  ", [("YES", hint_yes), ("NO", main_menu)], count_choice=False)
    choice()

def hint_yes():
    if state["hints_seen"] < 1:
        state["hints_seen"] = 1
        save_stats()  # Save progress after seeing new hint
    print("KEEP THIS IN MIND:")
    pause()
    print("YOU WON'T ALWAYS FIND OUT IF YOU MADE THE WRONG CHOICE RIGHT AWAY.")
    pause()
    print("SOME DECISIONS WON'T AFFECT YOU UNTIL LATER ON.")
    pause()
    print("...MUHUWAHAHAHA")
    wait(1)
    choice = menu("WANT MORE HINTS?", [("YEA", hint_yes_two), ("NOPE", main_menu)], count_choice=False)
    choice()

def hint_yes_two():
    if state["hints_seen"] < 2:
        state["hints_seen"] = 2
        save_stats()  # Save progress after seeing new hint
    print("PERSEVERANCE AND GRIT ARE GOOD QUALITIES.")
    wait(1)
    choice = menu("MORE HINTS?", [("YES PLEASE", hint_yes_three), ("NO, I'LL FLEX MY GRIT", main_menu)], count_choice=False)
    choice()

def hint_yes_three():
    if state["hints_seen"] < 3:
        state["hints_seen"] = 3
        save_stats()  # Save progress after seeing new hint
    print("SOME CHOICES ARE NOT AS OBVIOUS AS THEY SEEM.")
    pause()
    print("SOMETIMES YOU HAVE TO THINK OUTSIDE THE BOX.")
    pause()
    print("OR MAYBE JUST THINK AT ALL.")
    wait()
    choice = menu("EVEN MORE HINTS?", [("YEA, I'M DESPERATE", hint_yes_four), ("NAW DUDE, I'M GOOD", main_menu)], count_choice=False)
    choice()

def hint_yes_four():
    if state["hints_seen"] < 4:
        state["hints_seen"] = 4
        save_stats()  # Save progress after seeing new hint
    print("MONEY IS THE ROOT OF ALL THAT KILLS.")
    wait(3)
    choice = menu("WANT EVEN MORE HINTS!? HMM???", [("YES, JUST SPOON FEED ME PLEASE", hint_loser), ("NO, I WILL THINK FOR MYSELF. THANKS", main_menu)], count_choice=False)
    choice()

def hint_loser():
    print("NO MORE HINTS FOR YOU! LOSER.\n")
    pause()
    # Return to main menu

def background():
    # print()
    print("YOU ARE A HIGH SCHOOL STUDENT IN THE LATE 90'S.")
    wait()
    print("AND IT IS THE WORST DAY OF THE WEEK.")
    wait()
    print("MONDAY.\n")
    wait()
    print("\"YOU\" REFERS TO YOUR CHARACTER.")
    wait()
    print("\"ME\" OR \"I\" REFERS TO ME, THE PROGRAMMER.")
    wait()
    print("THE GAME IS EXTREMELY LONG AND CHALLENGING, SO DON'T GIVE UP.")
    wait(3)
    print("SOME OF THE CHARACTERS ARE FICTIONAL, BUT SOME ARE BASED ON OR ARE REAL PEOPLE, SOME ARE WELL-KNOWN.")
    wait(4.3)
    print("IT SEEMS LIKE THE WHOLE WORLD IS AGAINST YOU.\n")
    wait(5)
    print("IS IT?")
    wait(2)
    pause()
    # Return to main menu

def about():
    print("""
    ^o^^o^^o^^o^^o MONDAY o^^o^^o^^o^^o^^o^^
         ---------------------------
              A TEXT ADVENTURE
                FOR THE TI-83
         ---------------------------
               EBG1@JUNO.COM
         ---------------------------
     HTTP://WWW.GEOCITIES.COM/EVERETT710""")
    pause("Press Enter to see credits...")
    credits()

def credits():
    import sys
    import os
    credits_lines = ["",
        "                  CREDITS",
        "",
        "               STORY   EVERETT, DIEGO",
        "         PROGRAMMING   EVERETT, DIEGO",
        "          PRODUCTION   EVERETT",
        "         IMAGINATION   EVERETT, DIEGO, ANDRE",
        "       TECH. SUPPORT   DIEGO",
        "ENTICING DEATH SCENE   DIEGO",
        "      SADISTIC HUMOR   EVERETT, DIEGO",
        "        PLAY-TESTING   LAZ, JOHN, JENNIFER, ERIC, DEBORA, ANDRES, JOHN, MOLLY, JEFF",
        "                       HELYETT, NATHAN, GREG, SEAN, CHRIS, MARCO, KELLY AND PEDRO",
        " SENIOR PLAY-TESTERS   ANDRE \"MR. BOOMBASTIC\" OLIVEIRA",
        " SENIOR PLAY-TESTERS   DIEGO \"THE MASTER-HENTAI\"",
        "          CREATED IN   TI-83 BASIC",
        "    2025 PYTHON PORT   GITHUB COPILOT, DIEGO",
        "",
        "           COPYRIGHT   2001",
        "",
        "                THE END?"
    ]
    # Number of lines to show at once (like a movie credits window)
    window = 30
    # Pad with empty lines at the top and bottom for effect
    pad = ["" for _ in range(window)]
    scroll_lines = pad + credits_lines + pad
    for i in range(len(scroll_lines) - window + 1):
        # Clear screen (or just enough lines)
        if os.name == 'nt':
            os.system('cls')
        else:
            sys.stdout.write("\033[H\033[J")
        # Print the current window
        for line in scroll_lines[i:i+window]:
            print(line)
        wait(0.5 if PYODIDE_ENV else 0.8)
    state["times_won"] += 1
    save_stats()
    if state["times_good_ending"]:
        print()
        if state["hints_seen"] == 0:
            print("HEY...")
            wait(5)
            print("WE WANTED TO TAKE A MOMENT TO COMMEND YOU ON YOUR GRIT AND PERSERVERENCE")
            wait(3)
            print("WHICH YOU UTILIZED TO THEIR FULLEST TO COMLETE MONDAY WITHOUT *ANY* HINTS!")
            wait(6)
            print("\n\n\tWELL DONE CHAMP! (GOLF CLAP)")
        elif state["hints_seen"] < 4:
            print("CONGRATS, YOU WON WITHOUT PEEKING AT ALL THE HINTS!",
                  "\nEITHER YOU'RE LUCKY, A GENIUS, OR YOU REALLY NEED TO GET OUT MY HEAD.")
        print()
        pause("Press Enter to return to the main menu...")
    # quit_game()

def quit_game():
    save_stats()
    if state["times_played"] == 0:
        print("\n     LOSER\n   YOU DIDN'T\n EVEN START YET")
    else:
        print("\nTHANKS FOR PLAYING MONDAY!")
        if state["times_good_ending"] > 0:
            print("YOU'RE A CHAMPION!!\n")
    state["running"] = False
    wait(1)
    return

def debug_bypass():
    """Debug function to bypass game logic for testing purposes."""
    # state["cash"] = 10000000  # Bypass cash requirement
    # state["ti-83_confiscated"] = True  # Bypass TI-83 confiscation
    # board_plane()
    # print('nothing to bypass atm')
    return

def play_game():
    state["times_played"] += 1
    initialize_game_state()
    debug_bypass()
    print("YOU'RE IN BED, ASLEEP.")
    pause()
    print("IT'S 5:15 A.M.")
    pause()
    print("YOUR STEREO TURNS ON AND A LOCAL RADIO STATION IS PLAYING A SONG BY PRINCE.")
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
        if choice():
            break

def snooze():
    if state["snooze_count"] == 2:
        print("YOU OVERSLEPT\nYOU MISS YOUR BUS AND YOU TRY TO WALK TO SCHOOL.\nOF COURSE YOU DON'T MAKE IT!\nWHAT KIND OF GAME DO YOU THINK THIS IS?!?")
        game_over("oversleeping")
        return True
    print("ZZZZZ...")
    pause()
    state["snooze_count"] += 1
    return False

def smash_stereo():
    print("YOU GRAB YOUR BASEBALL BAT AND BEGIN DESTROYING YOUR STEREO.\nIT IS NOW A PILE OF SPARE PARTS.\nBUT YOU FORGOT ABOUT YOUR FRIEND'S CD.\nAND HIS DAD IS A MOB KINGPIN!\nOH CRAP")
    game_over("mob_hit")
    return True

def get_up():
    print("YOU GET UP AND STRETCH. AS YOU TAKE A DEEP BREATH, FOULNESS INVADES YOUR NOSTRILS. THE FOULNESS COULD ONLY BE CAUSED BY ONE THING. ITS MONDAY. BUT YOU REALLY, REALLY GOTTA GO!")
    pause()
    bathroom_menu()
    return True

def bathroom_menu():
    choice = menu("   DO YOU GO?   ", [("RELIEVE SELF", relieve_self), ("HOLD IT IN", hold_it_in)])
    choice()

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
        print("ED MCMAHON SHOWS UP AT YOUR DOOR TO SAY THAT YOU'VE WON 10 MILLION BUCKS. WHOO-HOO! YOU STUFF THE ENTIRE 10 MILLION BUCKS IN YOUR POCKET.")
        state["cash"] = 10000000
        pause()
        breakfast_menu()
    else:
        print("ED MCMAHON SHOWS UP AT YOUR DOOR TO SAY THAT YOU'VE WON 10 MILLION BUCKS. HE SEES YOUR PANTS AND IS DISGUSTED. HE TAKES BACK THE MONEY.")
        pause()
        breakfast_menu()

def breakfast_menu():
    choice = menu("   NOW WHAT?    ", [("EAT BREAKFAST", eat_breakfast), ("WASH HANDS", wash_hands), ("GO TO BUS STOP", skip_breakfast)])
    choice()

def eat_breakfast():
    print("YOU DIDN'T WASH YOUR HANDS. THAT'S SICK! THE GERMS EVENTUALLY OVERRUN YOU.")
    game_over("unwashed_breakfast")

def wash_hands():
    print("YOU WASHED YOUR HANDS. GOOD JOB YOU'RE NOT NEARLY AS UNSANITARY AS I THOUGHT!")
    pause()
    after_wash()

def skip_breakfast():
    print("BREAKFAST IS THE MOST IMPORTANT MEAL OF THE DAY! BUT YOU SKIPPED IT, NOW DID YOU?")
    game_over("skip_breakfast")

def after_wash():
    print("YOU ARE HUNGRY, SO YOU HAVE BREAKFAST.")
    pause()
    food_menu()

def food_menu():
    choice = menu("    EAT WHAT?   ", [("POP-TART", poptart), ("FROZEN PIZZA", frozen_pizza), ("CEREAL", cereal)])
    choice()

def poptart():
    print("IT IS STUCK IN THE TOASTER SO YOU TRY TO PRY IT OUT WITH A FORK. METAL CONDUCTS ELECTRICITY, FOOL!")
    game_over("electrocution")

def frozen_pizza():
    print("YOU FORGET TO DEFROST IT AND BREAK YOUR JAW.")
    game_over("broken_jaw")

def cereal():
    print("YUM!")
    pause()
    pack_bag_menu()

def pack_bag_menu():
    choice = menu("   NOW WHAT?    ", [("PACK BAG", pack_bag), ("BRUSH TEETH", brush_teeth)])
    choice()

def pack_bag():
    print("DISGUSTING! YOU DIDN'T BRUSH YOUR TEETH!")
    game_over("no_hygiene")

def brush_teeth():
    print("YOU RINSE OFF WHAT APPEARS TO BE CYANIDE, AND BRUSH...")
    pause()
    after_brush()

def after_brush():
    choice = menu("    AND NOW?    ", [("PACK BAG", pack_bag2), ("LEAVE FOR BUS", leave_for_bus)])
    choice()

def pack_bag2():
    print("DON'T FORGET YOUR TI-83, GAMEBOY AND CD PLAYER. ONLY WHAT'S NECESSARY.")
    pause()
    bus_menu()

def leave_for_bus():
    print("YOU FORGOT YOUR STUFF! YOU GET ALL F'S AND DON'T GO TO COLLEGE, NEVER GET A JOB AND STARVE TO DEATH.")
    game_over("starvation")

def bus_menu():
    choice = menu("   BAG PACKED.   ", [("GO TO BUS STOP", get_to_bus_stop), ("BACK TO BED", back_to_bed)])
    choice()

def get_to_bus_stop():
    choice = menu("HOW TO GET THERE", [("WALK", walk_to_bus), ("RUN", run_to_bus)])
    choice()

def back_to_bed():
    print("YOU GO BACK TO YOUR ROOM. THERE IS A PSYCHO WAITING FOR YOU... WEARING A MONICA LEWINSKI MASK...")
    game_over("psycho")

def walk_to_bus():
    print("YOU GET TO THE BUS STOP.")
    pause()
    at_bus_stop()

def run_to_bus():
    print("YOU FORGET TO LOOK BOTH WAYS.")
    game_over("car_accident")

def at_bus_stop():
    choice = menu("AT THE BUS STOP ", [("SIT", sit_at_bus), ("STAND", stand_at_bus)])
    choice()

def sit_at_bus():
    print("A CAR RUNS YOU DOWN. WHY? YOU SAT IN THE WET CEMENT THAT SOME JOKER LEFT AND YOU WERE UNABLE TO AVOID A CAR DRIVING ON THE SIDEWALK.")
    game_over("cement")

def stand_at_bus():
    print("AN 18-WHEELER NEARLY RUNS YOU DOWN. GOOD THING YOU ARE VERY AGILE.")
    pause()
    bus_arrives()

def bus_arrives():
    print("THE BUS COMES.")
    pause()
    choice = menu("  IT'S WAITING  ", [("GET ON", get_on_bus), ("MOON DRIVER", moon_driver)])
    choice()

def get_on_bus():
    print("YOU'RE ON THE BUS.")
    pause()
    on_bus_menu()

def moon_driver():
    print("THE DRIVER RUNS YOU DOWN OUT OF SPITE.")
    game_over("spiteful_driver")

def on_bus_menu():
    choice = menu("   ON THE BUS   ", [("SLEEP", sleep_on_bus), ("STAY AWAKE", stay_awake_on_bus)])
    choice()

def sleep_on_bus():
    print("YOU WAKE UP IN A BAD NEIGHBORHOOD...")
    game_over("bad_neighborhood")

def stay_awake_on_bus():
    print("YOU FINALLY ARRIVE AT SCHOOL")
    pause()
    at_school_menu()

def at_school_menu():
    choice = menu("   AT SCHOOL    ", [("ROAM HALLS", roam_halls), ("GO TO LIBRARY", go_to_library)])
    choice()

def roam_halls():
    print("YOU GET LOST, NEVER TO BE SEEN AGAIN.")
    game_over("lost_forever")

def go_to_library():
    print("YOU'RE IN THE LIBRARY.")
    pause()
    in_library_menu()

def in_library_menu():
    choice = menu("   IN LIBRARY   ", [("STUDY", study), ("GO ONLINE", go_online)])
    choice()

def study():
    print("YOUR BRAIN OVERHEATS...")
    game_over("brain_overheat")

def go_online():
    print("YOU GO ONLINE.")
    pause()
    where_to_online()

def where_to_online():
    choice = menu("   WHERE TO?    ", [("CIA.GOV", cia_gov), ("HENTAI SITE", hentai_site), ("MY SITE", my_site)])
    choice()

def cia_gov():
    print("YOU MISTAKENLY FIND GOVERNMENT SECRETS AND YOU ARE LATER KILLED \"ACCIDENTALLY\". WHEN AN ANVIL IS DROPPED ON YOUR HEAD.")
    game_over("anvil")

def hentai_site():
    print("IT'S BLOCKED BY SURFWATCH!")
    pause()
    where_to_online()

def my_site():
    print("YOU WENT TO MY SITE! GOOD FOR YOU!")
    pause()
    bell_rings()

def bell_rings():
    print("THE BELL RINGS.")
    pause()
    class_menu()

def class_menu():
    choice = menu("   WHERE TO?    ", [
        ("CHEMISTRY", wrong_class),
        ("PRE-CAL", wrong_class),
        ("DEBATE", debate_class)
    ])
    choice()

def wrong_class():
    print("WRONG CLASS!")
    pause()
    bell_rings()

def debate_class():
    print("YOU'RE IN DEBATE")
    pause()
    debate_menu()

def debate_menu():
    choice = menu("    DO YOU...   ", [
        ("SPEAK", debate_speak),
        ("PLAY TI-83", debate_ti83),
        ("CHECK E-MAIL", debate_email)
    ])
    choice()

def debate_speak():
    choice = menu("  CHOOSE EVENT  ", [
        ("TEAM DEBATE", team_debate),
        ("ORIGINAL ORATORY", original_oratory)
    ])
    choice()

def team_debate():
    print("YOU CHOOSE TEAM DEBATE.")
    pause()
    print("YOU SPEAK AS FAST AS YOU POSSIBLY CAN.")
    pause()
    print("BUT SOMEWHERE ALONG THE WAY, YOU CHOKE ON YOUR TONGUE.")
    game_over("choked_tongue")

def original_oratory():
    print("YOU CHOOSE ORIGINAL ORATORY")
    pause()
    print("AND REALIZE YOU FORGOT TO WRITE SOMETHING ***ORIGINAL***.")
    pause()
    print("SO YOU USE THE 'I HAVE A DREAM' SPEECH.")
    pause()
    print("NO ONE NOTICES.")
    pause()
    print("THE BELL RINGS.")
    pause()
    next_class_menu()

def debate_ti83():
    if state["ti-83_confiscated"]:
        print("YOU DON'T HAVE IT!")
    else:
        print("THE TEACHER CONFISCATES IT!")
        state["ti-83_confiscated"] = True
    pause()
    debate_class()

def debate_email():
    print("YOU CHECK YOUR E-MAIL. AND THE COMPUTER EXPLODES.")
    game_over("computer_explosion")

def next_class_menu():
    choice = menu("   WHERE TO?    ", [
        ("ENGINEERING", wrong_class2),
        ("LANGUAGE ARTS", language_arts),
        ("CHEMISTRY", wrong_class2)
    ])
    choice()

def wrong_class2():
    print("WRONG CLASS, FOOL")
    pause()
    next_class_menu()

def language_arts():
    print("YOU'RE IN LANGUAGE ARTS.")
    pause()
    la_menu()

def la_menu():
    choice = menu("  LANGUAGE ARTS ", [
        ("WRITE ESSAY", write_essay),
        ("PLAY GAMEBOY", play_gameboy),
        ("PLAY TI-83", la_ti83)
    ])
    choice()

def write_essay():
    print("YOU WRITE A KICKASS ESSAY. TIME FOR THE FINISHING TOUCHES.")
    pause()
    print("T...H...E...")
    print("E...N...")
    pause()
    print("AND YOUR HAND FALLS OFF. OWW!")
    game_over("hand_falls_off")

def play_gameboy():
    print("YOU PLAY YOUR GAME BOY ALL PERIOD. COOL.")
    pause()
    print("THE BELL RINGS.")
    pause()
    lunch_menu()

def la_ti83():
    if state["ti-83_confiscated"]:
        print("IT WAS ALREADY CONFISCATED.")
    else:
        print("THE TEACHER CONFISCATES IT.")
        state["ti-83_confiscated"] = True
    pause()
    language_arts()

def lunch_menu():
    choice = menu("     LUNCH      ", [
        ("EAT", lunch_eat),
        ("GO TO LIBRARY", lunch_library)
    ])
    choice()

def lunch_eat():
    print("A REALLY REALLY FINE GIRL IN A REALLY REALLY SHORT SKIRT ASKS TO BORROW 10 BUCKS.")
    pause()
    choice = menu("   SAY WHAT?    ", [
        ("LET ME CHECK", lunch_check),
        ("HELL NO!", lunch_hellno)
    ])
    choice()

def lunch_check():
    if state["cash"] == 10000000:
        print("*KISS* THANKS! :) :) :) :) :)")
        pause()
        print("SHE ASKS YOU TO MEET HER AFTER SCHOOL.")
        pause()
        print("YES!")
        lunch_eat2()
    else:
        print("OH, NO MONEY? AWWW... TOO BAD!")
        lunch_eat2()

def lunch_hellno():
    print("OKAY, SHE SAYS SADLY.")
    pause()
    print("HOW DUMB CAN YOU POSSIBLY BE???")
    game_over("reject_girl")

def lunch_eat2():
    pause()
    choice = menu("   EAT WHAT?    ", [
        ("CHICKEN", lunch_chicken),
        ("BEEF TACO", lunch_beef),
        ("PIZZA", lunch_pizza)
    ])
    choice()

def lunch_library():
    print("YOU GO TO THE LIBRARY.")
    pause()
    print("SOMEONE RELEASED POISONOUS METHANE GAS IN THE LIBRARY.")
    pause()
    print("YOU CHOKE ON YOUR FINAL BREATH OF AIR.")
    game_over("methane_gas")

def lunch_pizza():
    print("YUM!")
    pause()
    after_lunch()

def lunch_beef():
    print("MAD COW DISEASE...?")
    game_over("mad_cow")

def lunch_chicken():
    print("HMM... SALMONELLA...?")
    game_over("salmonella")

def after_lunch():
    choice = menu("   WHERE TO?    ", [
        ("GO ONLINE", lunch_online),
        ("NEXT CLASS", lunch_next_class)
    ])
    choice()

def lunch_online():
    print("THE SCREEN FLASHES AND YOU HAVE A SEIZURE.")
    game_over("seizure")

def lunch_next_class():
    print("WALKING TO NEXT CLASS.")
    pause()
    next_class2_menu()

def next_class2_menu():
    choice = menu("  NEXT CLASS?   ", [
        ("ENGINEERING", wrong_class3),
        ("CHEMISTRY", next_chemistry),
        ("HISTORY", wrong_class3)
    ])
    choice()

def wrong_class3():
    print("WRONG CLASS, FOOL")
    pause()
    next_class2_menu()

def next_chemistry():
    print("AS YOU ARE WALKING, YOU HEAR A LOUD CRASHING NOISE.")
    pause()
    print("YOU DIVE OUT OF THE WAY, AND THE ANVIL DROPS WITHOUT CASUALTY ONTO THE SPOT WHERE YOU WERE.")
    pause()
    print("WAIT!!")
    wait(0.5)
    print("AN ANVIL?!?!")
    pause()
    print("YOU MAKE IT TO CLASS IN ONE PIECE.")
    pause()
    print("BUT YOU ARE FEELING DROWSY. YOU NEED SUGAR.")
    pause()
    donut_menu()

def donut_menu():
    choice = menu("  BUY A DONUT?  ", [
        ("YES", donut_yes),
        ("NO", donut_no)
    ])
    choice()

def donut_yes():
    print("THE SCHOOL'S FOOTBALL TEAM'S BIGGEST LINEBACKER LOOKS AT YOU MENACINGLY.")
    pause()
    choice = menu("    GIVE IT?    ", [
        ("YES", donut_give),
        ("NO", donut_refuse)
    ])
    choice()

def donut_no():
    print("YOU FALL ASLEEP WITH YOUR FACE IN HYDROCHLORIC ACID!")
    game_over("acid_face")

def donut_give():
    print("YOU HAND IT TO HIM. HE EATS IT. BEFORE HE CAN BEAT YOU DOWN, HE CHOKES ON THE DONUT AND DIES.")
    pause()
    print("YOU SEARCH HIS POCKETS AND FIND A PACKET OF PURE SUGAR. OKAY.")
    pause()
    print("WHY LET IT GO TO WASTE. HE WON'T NEED IT ANYMORE.")
    pause()
    after_donut()

def donut_refuse():
    print("WHAT HAPPENS NEXT? I'LL LEAVE THAT TO YOUR IMAGINATION...")
    game_over("refused_donut")

def after_donut():
    print("IT WASN'T YOUR FAULT HE HAD TERRIBLE KARMA.")
    pause()
    end_of_day_menu()

def end_of_day_menu():
    choice = menu("THE DAY'S OVER! ", [
        ("WALK AROUND", walk_around),
        ("GO TO BUS", go_to_bus)
    ])
    choice()

def go_to_bus():
    insistant = state["insists_on_going_home"] > 1
    if state["cash"] != 10000000 or insistant:
        print("FINE. " if insistant else "","YOU'RE ON THE BUS...")
        pause()
        bus_end_menu()
    else:
        print("WHAT ARE YOU, GAY? " if state["insists_on_going_home"] else "", "GO MEET THE GIRL, FOOL!!!")
        pause()
        state["insists_on_going_home"] += 1
        end_of_day_menu()

def walk_around():
    if state["cash"] == 10000000:
        print("YOU MEET UP WITH THE GIRL FROM LUNCH.")
        pause()
        print("SHE'S SIGNALING FOR YOU TO GO WITH HER INTO THE JANITOR'S CLOSET.")
        pause()
        print("SHE'S HOT!!! SHE LOOKS LIKE YOUR DREAM GIRL AND SHE'S ONLY WEARING A TOWEL!")
        pause()
        print("AS SOON AS YOU GET WITHIN REACHING DISTANCE...")
        pause()
        print("SHE UNWRAPS HER TOWEL AND...")
        pause()
        print("YOU ARE BOTH RUN DOWN BY A HERD OF RAGING BUFFALO.")
        game_over("buffalo_stampede")
    else:
        print("THERE IS NO ONE IN SIGHT.")
        pause()
        print("YOU MISSED THE BUS AND TRY TO MAKE THE 10 MILE WALK HOME.")
        pause()
        print("YOU ARE ALMOST HOME, BUT YOU ARE ABDUCTED BY ALIENS.")
        game_over("alien_abduction")

def bus_end_menu():
    choice = menu("   ON THE BUS   ", [
        ("PLAY GAMEBOY", bus_gameboy),
        ("LISTEN TO CD", bus_cd),
        ("SLEEP", bus_sleep),
        ("TALK TO PEOPLE", bus_talk)
    ])
    choice()

def bus_gameboy():
    print("YOU PLAY YOUR GAMEBOY.")
    pause()
    print("YOU ARE MOMENTS AWAY FROM BEATING ZELDA: LINK'S AWAKENING")
    pause()
    print("BUT YOUR BATTERIES DIE.")
    pause()
    print("YOU GET REALLY, REALLY PI55ED.")
    pause()
    print("YOUR PULSE RISES TO 400 BEATS PER MINUTE.")
    game_over("gameboy_rage")

def bus_cd():
    print("YOU LISTEN TO A CD, AND SOMETHING WEIRD HAPPENS.")
    pause()
    print("YOU GET THE URGE TO JUMP OUT OF THE MOVING BUS.")
    pause()
    print("BUT WHY? IT SEEMS SOME BASTARD REPLACED YOUR GREEN DAY CD WITH THE SOUNDTRACK FROM ANNIE.")
    game_over("annie_cd")

def bus_sleep():
    print("YOU LOOK OUT THE WINDOW AND SEE A BILLBOARD WITH THE GIRL FROM LUNCH ON IT.")
    pause()
    print("IT'S ABOUT SINGLES IN YOUR AREA AND SHE'S MAKING A PEACE SIGN. STRANGE.")
    pause()
    print("WAIT, SHE'S A MODEL?")
    pause()
    print("OH CRUD, YOU FORGOT TO MEET HER AFTER SCHOOL!")
    pause()
    print("YOU FALL ASLEEP KICKING YOURSELF. THEN YOU WAKE UP.")
    pause()
    print("HEY, IT WORKS FOR ME ALL THE TIME!")
    pause()
    bus_arrival()

def bus_talk():
    print("YOU WALK ON THE BUS AND TRY TO SAY \"WHATS UP\"")
    pause()
    print("BUT IT COMES OUT SOUNDING LIKE...")
    pause()
    print("\"ALL OF YOUR MOTHERS WEAR ARMY BOOTS.\"")
    pause()
    print("THEN THEY THROW YOU OUT THE WINDOW.")
    pause()
    print("FOR NO APPARENT REASON.")
    game_over("bus_window")

def bus_arrival():
    print("THE BUS GETS TO YOUR STOP AND YOU GET OUT.")
    pause()
    after_bus_menu()

def after_bus_menu():
    choice = menu("    WHAT NOW?   ", [
        ("GO HOME", go_home),
        ("WHISTLE", whistle),
        ("GO TO EAT", go_eat),
        ("STARE AT SUN", stare_sun)
    ])
    choice()

def go_home():
    print("I SHOULD SMACK YOU FOR THINKING OF GOING RIGHT HOME!")
    game_over("quit_early")

def go_eat():
    print("YOU GO TO MCDONALDS.")
    pause()
    print("YOU EAT ONE FRY. ONE FRY TOO MANY. THE GREASE CLOGS YOUR ARTERIES AND YOU HAVE A HEART ATTACK.")
    game_over("mcdonalds_fry")

def stare_sun():
    print("YOU STARE AT THE SUN.")
    pause()
    print("YOUR RETINAS BURN AS YOU ARE CROSSING THE STREET AND YOU ARE BLINDED.")
    game_over("sun_blindness")

def whistle():
    print("YOU WHISTLE A HAPPY TUNE.")
    pause()
    print("SOMEONE HIRED A HITMAN TO KILL YOU. HE HEARS YOU WHISTLING AND BEGINS TO WHISTLE ALONG.")
    pause()
    print("HE FORGETS TO KILL YOU AND WALKS ALONG ON HIS MERRY 'OLE WAY.")
    pause()
    print("OKAY, WHATEVER.")
    pause()
    airport_menu()

def airport_menu():
    choice = menu("   WHERE NOW?   ", [
        ("THE AIRPORT", at_airport),
        ("HOME", airport_home)
    ])
    choice()

def at_airport():
    print("YOU GO TO THERE.")
    pause()
    airport_action_menu()

def airport_action_menu():
    choice = menu(" AT THE AIRPORT ", [
        ("GO EAT", airport_eat),
        ("BUY TICKET", airport_buy)
    ])
    choice()

def airport_eat():
    print("YOU EAT A TUNA SANDWHICH THEN REALIZE THAT THE TUNA'S NOT DEAD YET...")
    game_over("live_tuna")

def airport_home():
    print("YOU'RE KIDDING.")
    game_over("airport_quit")

def airport_buy():
    if state["cash"] != 10000000:
        print("YOU HAVE NO CASH.")
        pause()
        print("YOU SEE A CREDIT CARD ON THE FLOOR.")
        pause()
        print("ITS TED TURNER'S!")
        pause()
        print("YOU BUY A TICKET")
    else:
        print("WHY NOT. YOU HAVE ALL THIS MONEY TO BURN.")
    pause()
    ticket_menu()

def ticket_menu():
    choice = menu("     WHERE?     ", [
        ("IRAQ", iraq),
        ("KYOTO", kyoto),
        ("TEXAS", texas)
    ])
    choice()

def iraq():
    print("YOU GO TO IRAQ.")
    pause()
    print("YOU MEET SADAAM HUSSEIN.")
    pause()
    print("HE THINKS YOU'RE AN ASSASSIN AND THE GUARDS TAKE YOU OUT.")
    game_over("iraq_guards")

def kyoto():
    print("YOU VISIT NINTENDO HQ IN KYOTO.")
    pause()
    print("YOU TRY TO STEAL A GAME BOY ADVANCE PROTOTYPE")
    pause()
    print("DONKEY KONG STOPS YOU, AND TOSSES YOU INTO OBLIVION.")
    game_over("donkey_kong")

def texas():
    print("YOU GO TO TEXAS. YOU WALK AROUND THE STREETS.")
    pause()
    print("THERE IS A PSYCHOTIC THERE WHO HAS JUST TAKEN A HOSTAGE.")
    pause()
    print("HE IS DEMANDING... A TI-83???")
    pause()
    texas_menu()

def texas_menu():
    choice = menu("GIVE HIM YOUR'S?", [
        ("YES", texas_give),
        ("NO", texas_no)
    ])
    choice()

def texas_give():
    if not state["ti-83_confiscated"]:
        print("YOU GIVE HIM YOUR TI-83. HE LETS THE HOSTAGE GO AND RUNS AWAY.")
        pause()
        print("THE HOSTAGE WAS THE PRESIDENT OF TEXAS INSTRUMENTS!")
        pause()
        print("HE TAKES YOU TO THE COMPANY BUILDING AND GIVES YOU A TI-83 PLUS.")
        pause()
        print("EXCELLENT! *GUITAR RIFF*")
        pause()
        print("YOU TAKE IT AND START TO LEAVE, BUT HE'S NOT DONE YET.")
        pause()
        print("HE GIVES YOU A PLANE TICKET HOME, ON A TOP SECRET CONCORDE.")
        pause()
        print("FLIGHT AT THE SPEED OF LIGHT!")
        pause()
        print("THEN YOU LEAVE.")
        pause()
        plane_menu()
    else:
        print("YOU REACH INTO YOUR BACKPACK AND COME UP EMPTY.")
        pause()
        print("UH-OH...")
        game_over("hostage_fail")

def texas_no():
    print("YOU RUN AWAY, BUT YOUR BAD KARMA CATCHES UP WITH YOU...")
    game_over("texas_karma")

def plane_menu():
    choice = menu("  DO WHAT NOW?  ", [
        ("SCALP TICKET", scalp_ticket),
        ("BOARD PLANE", board_plane)
    ])
    choice()

def scalp_ticket():
    print("YOU SELL THE TICKET AND MAKE SOME MONEY, BUT YOU ARE STRANDED IN TEXAS!")
    pause()
    print("YOU TRY WALKING HOME, BUT YOU OBVIOUSLY DON'T MAKE IT.")
    game_over("walk_texas")

def board_plane():
    print("YOU EXCITEDLY BOARD THE PLANE TO GO HOME BUT PROMPTLY FALL ASLEEP.")
    pause()
    print("ZZZZZ...")
    pause()
    print("YOU WAKE UP SUDDENLY AND RELAIZE THE PLANE HAS CRASHED AND IS ON FIRE.")
    pause()
    print("YOU ESCAPE, AND RELIZE THAT YOU'RE THE ONLY SURVIVOR.")
    pause()
    print("YOU KNOW WHY?")
    pause()
    print("BECAUSE YOU HAD YOUR TRAY TABLE UP, AND YOUR SEAT BACK IN THE FULL, UPRIGHT POSITION.")
    pause()
    print("YOU CRAWL FROM THE TWISTED, BURNING WRECKAGE AND LOOK AROUND.")
    pause()
    if state["cash"] or not state["ti-83_confiscated"]:
        print("SEEMS LIKE YOUR LUCK IS RUNNING OUT.")
        pause()
        if not state["ti-83_confiscated"]:
            print("YOUR BACKPACK IS NOWHERE TO BE FOUND.")
            pause()
        if state["cash"]:
            print(f"{'' if state['ti-83_confiscated'] else 'AND '}YOUR CASH IS GONE!")
            pause()
    print("YOUR GPS TELLS YOU THAT YOU ARE NEAR ROSWELL, NM.")
    pause()
    print("YOU SEE A LARGE SIGN. IT SAYS:")
    pause()
    print("----------------\n!  WELCOME TO  ! \n!    AREA 51   !\n----------------")
    pause()
    print("AND ANOTHER ONE:")
    pause()
    print("----------------\n! PLEASE ENJOY !\n!  YOUR  STAY  !\n----------------")
    pause()
    area51_menu()

def area51_menu():
    print("THE GATE IS WIDE OPEN.")
    pause()
    choice = menu(" DO YOU GO IN?  ", [
        ("YES", area51_yes),
        ("NO", area51_no)
    ])
    choice()

def area51_yes():
    print("GOOD FOR YOU!")
    pause()
    print("YOU ENTER A BUILDING, AND FIND THE LIBRARY.")
    pause()
    print("YOU PICK UP A BOOK: THE EVIL SOCK.")
    pause()
    area51_book_menu()

def area51_no():
    print("WHAT KIND OF LOSER ARE YOU?!?")
    pause()
    print("LET'S TRY THAT AGAIN.")
    pause()
    area51_menu()

def area51_book_menu():
    choice = menu("WHAT DO YOU DO?", [
        ("READ IT", area51_read),
        ("EAT IT", area51_eat)
    ])
    choice()

def area51_eat():
    print("NOT BAD, BUT IT COULD HAVE USED SOME SALT.")
    pause()
    print("YOU THEN EXPERIENCE THE WORST CASE OF INDIGESTION EVER")
    game_over("book_indigestion")

def area51_read():
    print("YOU OPEN THE BOOK AND A KEY FALLS OUT.")
    pause()
    print("THE KEYCHAIN SAYS: ROOM 15^2.")
    pause()
    area51_room_menu()

def area51_room_menu():
    choice = menu("   WHICH ROOM  ?", [
        ("0", area51_wrong_room),
        ("15", area51_wrong_room),
        ("30", area51_wrong_room),
        ("152", area51_wrong_room),
        ("225", area51_right_room),
        ("1515", area51_wrong_room)
    ])
    choice()

def area51_wrong_room():
    print("IF THAT'S TOO HARD, WHY DO YOU EVEN HAVE A GRAPHING CALCULATOR?")
    game_over("math_fail")

def area51_right_room():
    print("GOOD JOB!")
    pause()
    print("YOU GO TO RM.225")
    pause()
    print("IT'S A BATHROOM!")
    pause()
    area51_bathroom_menu()

def area51_bathroom_menu():
    choice = menu("WHAT DO YOU DO? ", [
        ("TAKE A LEAK", area51_leak),
        ("TAKE A DRINK", area51_drink),
        ("TAKE A LOOK", area51_look),
        ("TAKE A NAP", area51_nap)
    ])
    choice()

def area51_leak():
    print("AHHHHH...")
    pause()
    print("BUT YOU SOMEHOW MANAGE TO GET FLUSHED DOWN THE TOILET.")
    game_over("toilet_flush")

def area51_drink():
    print("YOU SICKEN ME!")
    pause()
    print("SO MUCH SO THAT I THINK YOU SHOULD DIE.")
    game_over("toilet_drink")

def area51_look():
    print("YOU LOOK AT THE AIR VENT AND GET A SUDDEN URGE TO CLIMB THROUGH IT")
    pause()
    print("SO YOU DO. YIPPEE KI-YAY")
    pause()
    area51_vent()

def area51_nap():
    print("YOU TAKE A NAP. BUT AS YOU DO, YOU BREATHE IN TOO MUCH FLATULENCE.")
    pause()
    print("YOUR LUNGS CAN'T TAKE IT.")
    game_over("toxic_nap")

def area51_vent():
    print("YOU CRAWL ON YOUR HANDS AND KNEES, UNTIL YOU FINALLY SEE A LIGHT AT THE END OF THE TUNNEL.")
    pause()
    print("YOU HEAR HORRIFYING SOUNDS COMING FROM THE COURTYARD.")
    pause()
    print("YOU LOOK DOWN THE HATCH AND SEE THE MOST BIZZARE SIGHT YOU WILL EVER SEE.")
    pause()
    print("THERE IS A GROUP OF CREATURES WHICH APPEAR TO BE MUTATED SQUID...")
    pause()
    print("ALL DANCING THE YMCA!!!")
    pause()
    print("AND THAT'S WHY YOU GOT THE URGE TO CUT YOUR WRISTS.")
    pause()
    print("YOU JUMP DOWN AND...")
    pause()
    area51_courtyard_menu()

def area51_courtyard_menu():
    choice = menu(" WHAT DO YOU DO?", [
        ("SING", area51_sing),
        ("TELL JOKES", area51_jokes),
        ("DANCE", area51_dance),
        ("BITE", area51_bite)
    ])
    choice()

def area51_bite():
    print("YOU TAKE A BIG BITE OUT OF AN ALIEN'S JUGULAR VEIN. YOU ARE SPRAYED WITH ITS ACIDIC BLOOD.")
    game_over("alien_blood")

def area51_sing():
    print("YOU START TO SING ALONG WITH THE SONG.")
    pause()
    print("NOW I MUST SMACK YOU.")
    game_over("ymca_smack")

def area51_dance():
    print("YOU START TO DANCE ALONG WITH THE ALIENS. THEY ALL POINT AND LAUGH AT YOU.")
    pause()
    print("SELF-ESTEEM METER: |0| |-| |-| |-| |-| |-| |-|")
    pause()
    game_over("alien_dance")

def area51_jokes():
    print("YOU WALK TO THE FRONT OF THE CROWD AND START TO RECITE A JERRY SEINFELD STAND-UP ROUTINE")
    pause()
    print("THEY ALL GIVE YOU A BLANK STARE, UNTIL ONE OF THEM, RUPERT, TRANSLATES WHAT YOU SAID.")
    pause()
    print("THEY ALL LAUGH UNTIL THEY FALL OVER, GASPING FOR AIR.")
    pause()
    print("YOU KILLED THEM ALL!")
    pause()
    print("NEWS OF THE MASSACRE IS SENT AND BIG BOSS BILLY BOB THE ALIENS' LEADER IS FURIOUS.")
    pause()
    print("SO YOU TRY THE ACT ON HIM TOO.")
    pause()
    print("ACK! HE HAS NO SENSE OF HUMOR!")
    pause()
    print("SO YOU TELL HIM THAT THERE IS A BUG ON HIS SHOULDER.")
    pause()
    print("HE FREAKS OUT AND RUNS AWAY, SCREAMING LIKE A LITTLE GIRL.")
    pause()
    print("YOU ARE A HERO. YOU SAVED AREA51 FROM THE EVIL ALIEN SQUID CULT.")
    pause()
    print("BUT SINCE IT IS CLASSIFIED INFO. NO ONE WILL EVER KNOW ABOUT IT.")
    pause()
    print("D'OH!")
    pause()
    print("SO YOU WALK HOME DEPRESSED.")
    pause()
    print("YES, I REALIZE ITS A LONG WAY.")
    pause()
    print("WHAT A DAY IT'S BEEN.")
    pause()
    print("HEY, ISN'T THAT THE GIRL FROM LUNCH EARLIER TODAY?")
    pause()
    print("YEA! YEA!")
    pause()
    print("YOU REACH INTO YOUR POCKET AND MAGICALLY, YOU FIND 10 BUCKS!")
    pause()
    print("YOU RUN UP TO HER AND ASK HER IF SHE STILL NEEDS THE MONEY.")
    pause()
    print("YEA, SURE.")
    pause()
    print("YOU GIVE IT TO HER AND YOU TWO LIVE HAPPILY EVER AFTER.")
    pause()
    print("...")
    wait()
    pause()
    print("\nWHAT THE HELL KIND OF CRAP ENDING WAS THAT?!?!")
    pause()
    print("LETS TRY THAT AGAIN.")
    pause()
    print("TIME TRAVELING...")
    print()
    wait(1)
    pause()
    print("SO YOU KILLED THE ALIEN SQUID CULT AND YOU ARE A HERO.")
    pause()
    print("SO YOU WALK HOME AND YOU SEE THE GIRL FROM LUNCH.")
    pause()
    print("SHE MUST LIKE YOU, SHE KEEPS SHOWING UP ALONG THE WAY!")
    pause()
    print("SHE LEANS CLOSE TO YOUR EAR AND WHISPERS...")
    pause()
    print("\"YOU KNOW WHAT I WANT TO DO...\"")
    pause()
    print("*GULP* \"YEA... BUT I'M NOT REALLY IN THE MOOD.\"")
    pause()
    final_menu()

def final_menu():
    choice = menu("  SO NOW WHAT?  ", [
        ("SCREAM", final_scream),
        ("DIG HOLE", final_dig),
        ("GIVE UP", final_giveup)
    ])
    choice()

def final_giveup():
    print("WHAT KIND OF LOSER ARE YOU!?!")
    pause()
    print("YOU CAME ALL THIS WAY FOR... NOTHING!")
    wait()
    print("YOU LOSER.")
    pause("Press Enter to roll the credits...")
    game_over("final_loser")

def final_scream():
    print("YOU SCREAM AS LOUD AS YOU CAN.")
    pause()
    print("\"I'M ALIVE AND I GOT A HOT CHICK. HIT ME WITH YOUR BEST SHOT, MONDAY!!!\"")
    pause()
    print("AND GUESS WHAT.")
    pause()
    print("IT DOES.")
    wait()
    pause("Press Enter to roll the credits...")
    game_over("monday_revenge")

def final_dig():
    print("YOU BEGIN TO DIG FOR NO APPARENT REASON.")
    pause()
    print("YOU DIG AND DIG AND DIG.")
    pause()
    print("YOU HAVE NO IDEA WHY YOU'RE EVEN DIGGING.")
    pause()
    print("ITS HOPELESS. THERE'S NOTHING THERE.")
    pause()
    print("YOU THROW YOUR SHOVEL DOWN IN FRUSTRATION, NEARLY SMASHING A GLASS VIAL MARKED...")
    pause()
    print("----------------\nI    AUSTIN    I\nI    POWER'S   I\nI     MOJO     I\n----------------")
    pause()
    print("OH, BEHAVE!")
    pause()
    print("YOU DOWN THE ENTIRE VIAL AND...")
    pause()
    print("YOU CAN IMAGINE WHAT HAPPENS NEXT.")
    pause()
    print("USE YOUR IMAGINATION.")
    pause()
    print("HEEHEEHEEHEE.")
    wait(1)
    pause()
    print("A HALF HOUR LATER, YOU DRIFT OFF TO SLEEP.")
    pause()
    print("AND YOU THINK TO YOURSELF...")
    pause()
    print("THIS DAY WAS AWESOME!\n\n")
    wait()
    print("      ROLL\n      THE\n    CREDITS!   ")
    pause("Press Enter to roll the credits...")
    state["times_good_ending"] += 1
    credits()

def game_over(death_cause=""):
    if death_cause:
        record_death(death_cause)
    save_stats()
    print("\n---GAME--OVER---\nMONDAY HAS CLAIMED ANOTHER VICTIM!\n\nTRY AGAIN!")
    pause()
    main_menu()

if __name__ == "__main__":
    load_stats()
    title_screen()

