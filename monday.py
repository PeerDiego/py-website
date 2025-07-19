"""
Python text adventure: MONDAY
Converted from TI-BASIC by GitHub Copilot

Features:
- Menus and choices via input()
- Print for all narrative and UI
- Game state tracked with variables and lists
- Humor and tone preserved
"""

import os
import sys
import time
import base64
import hashlib

# Try to import cryptography, else disable save/load
try:
    from cryptography.fernet import Fernet, InvalidToken
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("[WARNING] Save/load is disabled: cryptography package not found. (ignore this on the website)")

def pause(prompt = "Press Enter to continue..."):
    # Print prompt, wait for Enter, then overwrite the prompt line with spaces
    input(prompt)  # Removed the \n to keep the prompt on same line
    # Move cursor up one line and clear it - not needed for web version
    # sys.stdout.write("\033[F")  # Move cursor up one line
    # sys.stdout.write(" " * len(prompt) + "\r")  # Overwrite with spaces
    # sys.stdout.flush()

def wait(s=2.0):
    time.sleep(s)

# Game state dictionary - maintains state across different functions
# This is a workaround for the limitations of Pyodide's handling of global variables
state = {
    "running"           : True,
    "snooze_count"      : 0,
    "pants_wet"         : False,
    "cash"              : 0,
    "ti-83_confiscated" : False,  # True if confiscated, False if player has it
    "has_money"         : False,
    "insists_on_going_home" : 0,  # inisists on going home at end of day; bypass win route
    # Statistics tracking (formerly LMNDY list)
    "times_played"      : 0,  # Number of times game has been played
    "times_won"         : 0,  # Number of times player has won
    "times_good_ending" : 0,  # Number of times player got the good ending
}

def menu(title, options):
    menu_text = f"\n{title}"
    for i, (label, _) in enumerate(options, 1):
        menu_text += f"\n  {i}. {label}"
    print(menu_text, "\n\n")
    while state["running"]:
        try:
            choice = int(input("Choose: "))
            if 1 <= choice <= len(options):
                return options[choice-1][1]
        except ValueError:
            pass
        print("Invalid choice. Try again.")


SAVE_FILE = "monday_save.dat"
SECRET = "monday_secret_key_2025"  # Change this to something unique for your game

def get_fernet():
    if not CRYPTO_AVAILABLE:
        raise RuntimeError("Cryptography not available")
    # Derive a 32-byte key from SECRET
    key = hashlib.sha256(SECRET.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))

def save_stats():
    if not CRYPTO_AVAILABLE:
        return
    f = get_fernet()
    stats = [
        state["times_played"],
        state["times_won"],
        state["times_good_ending"]
    ]
    data = ",".join(str(x) for x in stats).encode()
    token = f.encrypt(data)
    with open(SAVE_FILE, "wb") as file:
        file.write(token)

def load_stats():
    if not CRYPTO_AVAILABLE or not os.path.exists(SAVE_FILE):
        return
    f = get_fernet()
    try:
        with open(SAVE_FILE, "rb") as file:
            token = file.read()
        data = f.decrypt(token).decode()
        stats = [int(x) for x in data.split(",")]
        state["times_played"] = stats[0]
        state["times_won"] = stats[1]
        state["times_good_ending"] = stats[2]
    except Exception:
        state["times_played"] = 0
        state["times_won"] = 0
        state["times_good_ending"] = 0

def title_screen():
    print("\nA MODERN ADVENTURE OF EPIC PROPORTIONS")
    wait()
    print("\n    {}{}{}{}{}{}{}{}{}{}{}\n   {{{{{{{{ MONDAY }}}}}}}}\n    {}{}{}{}{}{}{}{}{}{}{}\n\n       SPECIAL EDITION")
    pause()
    main_menu()

def main_menu():
    while state["running"]:
        choice = menu("-----MONDAY-----", [
            ("PLAY GAME", play_game),
            ("BACKGROUND", background),
            ("HINTS", hints),
            ("POINTLESS INFO.", pointless_info),
            ("ABOUT", about),
            ("QUIT GAME", quit_game)
        ])
        await choice()
    print("Thanks for playing!")

def pointless_info():
    print("\nHERE'S SOME USELESS INFORMATION.")
    pause()
    print(f"YOU HAVE PLAYED THIS GAME {state['times_played']} TIMES.")
    wait(1)
    print(f"YOU HAVE WON {state['times_won']} TIME(S).", 
          " >_> <_<" if state['times_won'] > state['times_played'] else "")
    wait(1.5)
    if state['times_good_ending'] > 0:
        print(f"YOU HAVE ACTUALLY WON {state['times_good_ending']} TIME(S).")
    elif state['times_won'] == 0:
        print("KEEP ON TRYING.")
    elif state['times_won'] == 1:
        print("YOU'RE GETTING THE HANG OF IT.")
    wait(1)
    # Return to main menu

def hints():
    choice = menu("  WANT A HINT?  ", [("YES", hint_yes), ("NO", main_menu)])
    await choice()

def hint_yes():
    print("KEEP THIS IN MIND:")
    pause()
    print("YOU WON'T ALWAYS FIND OUT IF YOU MADE THE WRONG CHOICE RIGHT AWAY.")
    pause()
    print("SOME DECISIONS WON'T AFFECT YOU UNTIL LATER ON.")
    pause()
    print("  MUHUWAHAHAHA")
    pause()
    choice = menu("WANT MORE HINTS?", [("YEA", hint_loser), ("NOPE", main_menu)])
    await choice()

def hint_loser():
    print("LOSER.")
    pause()
    # Return to main menu

def background():
    # print()
    print("YOU ARE A HIGH SCHOOL STUDENT.")
    wait()
    print("AND IT IS THE WORST DAY OF THE WEEK.")
    wait()
    print("MONDAY.")
    wait()
    print("'YOU' REFERS TO YOUR CHARACTER.")
    wait()
    print("'ME' OR 'I' REFERS TO ME, THE PROGRAMMER.")
    wait()
    print("THE GAME IS EXTREMELY LONG AND CHALLENGING, SO DON'T GIVE UP.")
    wait(3)
    print("SOME OF THE CHARACTERS ARE FICTIONAL, BUT SOME ARE BASED ON OR ARE REAL PEOPLE, SOME ARE WELL-KNOWN.")
    wait(4.3)
    print("IT SEEMS LIKE THE WHOLE WORLD IS AGAINST YOU.")
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
        " SENIOR PLAY-TESTERS   ANDRE 'MR. BOMBASTIC' OLIVEIRA",
        " SENIOR PLAY-TESTERS   DIEGO 'THE MASTER-HENTAI'",
        "          CREATED IN   TI-83 BASIC",
        "    2025 PYTHON PORT   GITHUB COPILOT, DIEGO",
        "",
        "           COPYRIGHT   2001",
        "",
        "                THE END?"
    ]
    # Number of lines to show at once (like a movie credits window)
    window = 22
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
        wait(0.8)
    state["times_won"] += 1
    save_stats()
    # quit_game()

def quit_game():
    save_stats()
    if state["times_played"] == 0:
        print("\n     LOSER\n   YOU DIDN'T\n EVEN START YET")
    else:
        print("\nTHANKS FOR PLAYING MONDAY!")
    state["running"] = False
    wait(1)
    return

def play_game():
    state["times_played"] += 1
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
        if await choice():
            break

def snooze():
    if state["snooze_count"] == 2:
        print("YOU'VE OVERSLEPT\nYOU MISS YOUR BUS AND YOU TRY TO WALK TO SCHOOL.\nOF COURSE YOU DON'T MAKE IT!\nWHAT KIND OF GAME DO YOU THINK THIS IS?!?")
        game_over()
        return True
    print("ZZZZZ...")
    pause()
    state["snooze_count"] += 1
    return False

def smash_stereo():
    print("YOU GRAB YOUR BASEBALL BAT AND BEGIN DESTROYING YOUR STEREO.\nIT IS NOW A PILE OF SPARE PARTS.\nBUT YOU FORGOT ABOUT YOUR FRIEND'S CD.\nAND HIS DAD IS A MOB KINGPIN!\nOH CRAP")
    game_over()
    return True

def get_up():
    print("YOU GET UP AND STRETCH. AS YOU TAKE A DEEP BREATH, FOULNESS INVADES YOUR NOSTRILS. THE FOULNESS COULD ONLY BE CAUSED BY ONE THING. ITS MONDAY. BUT YOU REALLY, REALLY GOTTA GO!")
    pause()
    bathroom_menu()
    return True

def bathroom_menu():
    choice = menu("   DO YOU GO?   ", [("RELIEVE SELF", relieve_self), ("HOLD IT IN", hold_it_in)])
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
        print("ED MCMAHON SHOWS UP AT YOUR DOOR TO SAY THAT YOU'VE WON 10 MILLION BUCKS. WHOO-HOO! YOU STUFF THE ENTIRE 10 MILLION BUCKS IN YOUR POCKET.")
        state["cash"] = 10000000
        pause()
        breakfast_menu()
    else:
        print("ED MCMAHON SHOWS UP AT YOUR DOOR TO SAY THAT YOU'VE WON 10 MILLION BUCKS. HE SEES YOUR PANTS AND IS DISGUSTED. HE TAKES BACK THE MONEY.")
        pause()
        game_over()

def breakfast_menu():
    choice = menu("   NOW WHAT?    ", [("EAT BREAKFAST", eat_breakfast), ("WASH HANDS", wash_hands), ("GO TO BUS STOP", skip_breakfast)])
    await choice()

def eat_breakfast():
    print("YOU DIDN'T WASH YOUR HANDS. THAT'S SICK! THE GERMS EVENTUALLY OVERRUN YOU.")
    game_over()

def wash_hands():
    print("YOU WASHED YOUR HANDS. GOOD JOB YOU'RE NOT NEARLY AS UNSANITARY AS I THOUGHT!")
    pause()
    after_wash()

def skip_breakfast():
    print("BREAKFAST IS THE MOST IMPORTANT MEAL OF THE DAY! BUT YOU SKIPPED IT, NOW DID YOU?")
    game_over()

def after_wash():
    print("YOU ARE HUNGRY, SO YOU HAVE BREAKFAST.")
    pause()
    food_menu()

def food_menu():
    choice = menu("    EAT WHAT?   ", [("POP-TART", poptart), ("FROZEN PIZZA", frozen_pizza), ("CEREAL", cereal)])
    await choice()

def poptart():
    print("IT IS STUCK IN THE TOASTER SO YOU TRY TO PRY IT OUT WITH A FORK. METAL CONDUCTS ELECTRICITY, FOOL!")
    game_over()

def frozen_pizza():
    print("YOU FORGET TO DEFROST IT AND BREAK YOUR JAW.")
    game_over()

def cereal():
    print("YUM!")
    pause()
    pack_bag_menu()

def pack_bag_menu():
    choice = menu("   NOW WHAT?    ", [("PACK BAG", pack_bag), ("BRUSH TEETH", brush_teeth)])
    await choice()

def pack_bag():
    print("DISGUSTING! YOU DIDN'T BRUSH YOUR TEETH!")
    game_over()

def brush_teeth():
    print("YOU RINSE OFF WHAT APPEARS TO BE CYANIDE, AND BRUSH...")
    pause()
    after_brush()

def after_brush():
    choice = menu("    AND NOW?    ", [("PACK BAG", pack_bag2), ("LEAVE FOR BUS", leave_for_bus)])
    await choice()

def pack_bag2():
    print("DON'T FORGET YOUR TI-83, GAMEBOY AND CD PLAYER. ONLY WHAT'S NECESSARY.")
    pause()
    bus_menu()

def leave_for_bus():
    print("YOU FORGOT YOUR STUFF! YOU GET ALL F'S AND DON'T GO TO COLLEGE, NEVER GET A JOB AND STARVE TO DEATH.")
    game_over()

def bus_menu():
    choice = menu("   PACKED BAG   ", [("GO TO BUS STOP", get_to_bus_stop), ("BACK TO BED", back_to_bed)])
    await choice()

def get_to_bus_stop():
    choice = menu("HOW TO GET THERE", [("WALK", walk_to_bus), ("RUN", run_to_bus)])
    await choice()

def back_to_bed():
    print("YOU GO BACK TO YOUR ROOM. THERE IS A PSYCHO WAITING FOR YOU... WEARING A MONICA LEWENSKI MASK...")
    game_over()

def walk_to_bus():
    print("YOU GET TO THE BUS STOP.")
    pause()
    at_bus_stop()

def run_to_bus():
    print("YOU FORGET TO LOOK BOTH WAYS.")
    game_over()

def at_bus_stop():
    choice = menu("AT THE BUS STOP ", [("SIT", sit_at_bus), ("STAND", stand_at_bus)])
    await choice()

def sit_at_bus():
    print("A CAR RUNS YOU DOWN. WHY? YOU SAT IN THE WET CEMENT THAT SOME JOKER LEFT AND YOU WERE UNABLE TO AVOID A CAR DRIVING ON THE SIDEWALK.")
    game_over()

def stand_at_bus():
    print("AN 18-WHEELER NEARLY RUNS YOU DOWN. GOOD THING YOU ARE VERY AGILE.")
    pause()
    bus_arrives()

def bus_arrives():
    print("THE BUS COMES.")
    pause()
    choice = menu("  IT'S WAITING  ", [("GET ON", get_on_bus), ("MOON DRIVER", moon_driver)])
    await choice()

def get_on_bus():
    print("YOU'RE ON THE BUS.")
    pause()
    on_bus_menu()

def moon_driver():
    print("THE DRIVER RUNS YOU DOWN OUT OF SPITE.")
    game_over()

def on_bus_menu():
    choice = menu("   ON THE BUS   ", [("SLEEP", sleep_on_bus), ("STAY AWAKE", stay_awake_on_bus)])
    await choice()

def sleep_on_bus():
    print("YOU WAKE UP IN A BAD NEIGHBORHOOD...")
    game_over()

def stay_awake_on_bus():
    print("YOU FINALLY ARRIVE AT SCHOOL")
    pause()
    at_school_menu()

def at_school_menu():
    choice = menu("   AT SCHOOL    ", [("ROAM HALLS", roam_halls), ("GO TO LIBRARY", go_to_library)])
    await choice()

def roam_halls():
    print("YOU GET LOST, NEVER TO BE SEEN AGAIN.")
    game_over()

def go_to_library():
    print("YOU'RE IN THE LIBRARY.")
    pause()
    in_library_menu()

def in_library_menu():
    choice = menu("   IN LIBRARY   ", [("STUDY", study), ("GO ONLINE", go_online)])
    await choice()

def study():
    print("YOUR BRAIN OVERHEATS...")
    game_over()

def go_online():
    print("YOU GO ONLINE.")
    pause()
    where_to_online()

def where_to_online():
    choice = menu("   WHERE TO?    ", [("CIA.GOV", cia_gov), ("HENTAI SITE", hentai_site), ("MY SITE", my_site)])
    await choice()

def cia_gov():
    print("YOU MISTAKENLY FIND GOVERNMENT SECRETS AND YOU ARE LATER KILLED 'ACCIDENTALLY'. WHEN AN ANVIL IS DROPPED ON YOUR HEAD.")
    game_over()

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
    await choice()

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
    await choice()

def debate_speak():
    choice = menu("  CHOOSE EVENT  ", [
        ("TEAM DEBATE", team_debate),
        ("ORIGINAL ORATORY", original_oratory)
    ])
    await choice()

def team_debate():
    print("YOU CHOOSE TEAM DEBATE.")
    pause()
    print("YOU SPEAK AS FAST AS YOU POSSIBLY CAN.")
    pause()
    print("BUT SOMEWHERE ALONG THE WAY, YOU CHOKE ON YOUR TONGUE.")
    game_over()

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
    game_over()

def next_class_menu():
    choice = menu("   WHERE TO?    ", [
        ("ENGINEERING", wrong_class2),
        ("LANGUAGE ARTS", language_arts),
        ("CHEMISTRY", wrong_class2)
    ])
    await choice()

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
    await choice()

def write_essay():
    print("YOU WRITE A KICKASS ESSAY. TIME FOR THE FINISHING TOUCHES.")
    pause()
    print("T...H...E...")
    print("E...N...")
    pause()
    print("AND YOUR HAND FALLS OFF. OWW!")
    game_over()

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
    await choice()

def lunch_eat():
    print("A REALLY REALLY FINE GIRL IN A REALLY REALLY SHORT SKIRT ASKS TO BORROW 10 BUCKS.")
    pause()
    choice = menu("   SAY WHAT?    ", [
        ("LET ME CHECK", lunch_check),
        ("HELL NO!", lunch_hellno)
    ])
    await choice()

def lunch_check():
    if state["cash"] == 10000000:
        print("*KISS* THANKS! :) :) :) :) :)")
        pause()
        print("SHE ASKS YOU TO MEET YOU AFTER SCHOOL.")
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
    game_over()

def lunch_eat2():
    pause()
    choice = menu("   EAT WHAT?    ", [
        ("CHICKEN", lunch_chicken),
        ("BEEF TACO", lunch_beef),
        ("PIZZA", lunch_pizza)
    ])
    await choice()

def lunch_library():
    print("YOU GO TO THE LIBRARY.")
    pause()
    print("SOMEONE RELEASED POISONOUS METHANE GAS IN THE LIBRARY.")
    pause()
    print("YOU CHOKE ON YOUR FINAL BREATH OF AIR.")
    game_over()

def lunch_pizza():
    print("YUM!")
    pause()
    after_lunch()

def lunch_beef():
    print("MAD COW DISEASE...?")
    game_over()

def lunch_chicken():
    print("HMM... SALMONELLA...?")
    game_over()

def after_lunch():
    choice = menu("   WHERE TO?    ", [
        ("GO ONLINE", lunch_online),
        ("NEXT CLASS", lunch_next_class)
    ])
    await choice()

def lunch_online():
    print("THE SCREEN FLASHES AND YOU HAVE A SEIZURE.")
    game_over()

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
    await choice()

def wrong_class3():
    print("WRONG CLASS, FOOL")
    pause()
    next_class2_menu()

def next_chemistry():
    print("AS YOU ARE WALKING, YOU HEAR A LOUD CRASHING NOISE.")
    pause()
    print("YOU DIVE OUT OF THE WAY, AND THE ANVIL FALLS HARMLESSLY TO THE SPOT WHERE YOU WERE.")
    pause()
    print("WAIT!!")
    pause()
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
    await choice()

def donut_yes():
    print("THE SCHOOL FOOTBALL TEAM'S BIGGEST LINEBACKER LOOKS AT YOU MENACINGLY.")
    pause()
    choice = menu("    GIVE IT?    ", [
        ("YES", donut_give),
        ("NO", donut_refuse)
    ])
    await choice()

def donut_no():
    print("YOU FALL ASLEEP WITH YOUR FACE IN HYDROCHLORIC ACID!")
    game_over()

def donut_give():
    print("YOU HAND IT TO HIM. HE EATS IT. BEFORE HE CAN BEAT YOU DOWN, HE CHOKES ON THE DONUT AND DIES.")
    pause()
    print("YOU SEARCH HIS POCKETS AND FIND A PACKET OF PURE SUGAR. OKAY.")
    pause()
    after_donut()

def donut_refuse():
    print("WHAT HAPPENS NEXT? I'LL LEAVE THAT TO YOUR IMAGINATION...")
    game_over()

def after_donut():
    print("IT WASN'T YOUR FAULT HE HAD TERRIBLE KARMA.")
    pause()
    end_of_day_menu()

def end_of_day_menu():
    choice = menu("THE DAY'S OVER! ", [
        ("WALK AROUND", walk_around),
        ("GO TO BUS", go_to_bus)
    ])
    await choice()

def go_to_bus():
    insistant = state["insists_on_going_home"] > 1
    if state["cash"] != 10000000 or insistant:
        print("FINE! " if insistant else "","YOU'RE ON THE BUS...")
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
        print("SHE'S SIGNALING FOR YOU TO GO WITH HER INTO THE JANITOR'S CLOSET WITH HER.")
        pause()
        print("SHE'S HOT!!! SHE LOOKS LIKE YOUR DREAM GIRL AND SHE'S ONLY WEARING A TOWEL!")
        pause()
        print("AS SOON AS YOU GET WITHIN REACHING DISTANCE...")
        pause()
        print("SHE UNWRAPS HER TOWEL AND...")
        pause()
        print("YOU ARE BOTH RUN DOWN BY A HERD OF RAGING BUFFALO.")
        game_over()
    else:
        print("THERE IS NO ONE IN SIGHT.")
        pause()
        print("YOU MISSED THE BUS AND TRY TO MAKE THE 10 MILE WALK HOME.")
        pause()
        print("YOU ARE ALMOST HOME, BUT YOU ARE ABDUCTED BY ALIENS.")
        game_over()

def bus_end_menu():
    choice = menu("   ON THE BUS   ", [
        ("PLAY GAMEBOY", bus_gameboy),
        ("LISTEN TO CD", bus_cd),
        ("SLEEP", bus_sleep),
        ("TALK TO PEOPLE", bus_talk)
    ])
    await choice()

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
    game_over()

def bus_cd():
    print("YOU LISTEN TO A CD, AND SOMETHING WEIRD HAPPENS.")
    pause()
    print("YOU GET THE URGE TO JUMP OUT OF THE MOVING BUS.")
    pause()
    print("BUT WHY? IT SEEMS SOME BASTARD REPLACED YOUR GREEN DAY CD WITH THE SOUNDTRACK FROM ANNIE.")
    game_over()

def bus_sleep():
    print("YOU LOOK OUT THE WINDOW AND SEE A BILLBOARD WITH A PICTURE OF THE GIRL ON IT.")
    pause()
    print("AND SHE'S GIVING A PEACE SIGN. STRANGE.")
    pause()
    print("YOU SLEEP. THEN YOU WAKE UP.")
    pause()
    print("HEY, IT WORKS FOR ME ALL THE TIME!")
    pause()
    bus_arrival()

def bus_talk():
    print("YOU WALK ON THE BUS AND TRY TO SAY 'WHATS UP'")
    pause()
    print("BUT IT COMES OUT SOUNDING LIKE...")
    pause()
    print("'ALL OF YOUR MOTHERS WEAR ARMY BOOTS.'")
    pause()
    print("THEN THEY THROW YOU OUT THE WINDOW.")
    pause()
    print("FOR NO APPARENT REASON.")
    game_over()

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
    await choice()

def go_home():
    print("I SHOULD SMACK YOU FOR THINKING OF GOING RIGHT HOME!")
    game_over()

def go_eat():
    print("YOU GO TO MCDONALDS.")
    pause()
    print("YOU EAT ONE FRY. ONE FRY TOO MANY. THE GREASE CLOGS YOUR ARTERIES AND YOU HAVE A HEART ATTACK.")
    game_over()

def stare_sun():
    print("YOU STARE AT THE SUN.")
    pause()
    print("YOUR RETINAS BURN AS YOU ARE CROSSING THE STREET AND YOU ARE BLINDED.")
    game_over()

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
    await choice()

def at_airport():
    print("YOU GO TO THERE.")
    pause()
    airport_action_menu()

def airport_action_menu():
    choice = menu(" AT THE AIRPORT ", [
        ("GO EAT", airport_eat),
        ("BUY TICKET", airport_buy)
    ])
    await choice()

def airport_eat():
    print("YOU EAT A TUNA SANDWHICH THEN REALIZE THAT THE TUNA'S NOT DEAD YET...")
    game_over()

def airport_home():
    print("YOU'RE KIDDING.")
    game_over()

def airport_buy():
    if state["cash"] != 10000000:
        print("YOU HAVE NO CASH")
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
    await choice()

def iraq():
    print("YOU GO TO IRAQ.")
    pause()
    print("YOU MEET SADAAM HUSSEIN.")
    pause()
    print("HE THINKS YOU'RE AN ASASIN AND THE GUARDS TAKE YOU OUT.")
    game_over()

def kyoto():
    print("YOU VISIT NINTENDO HQ IN KYOTO.")
    pause()
    print("YOU TRY TO STEAL A GAME BOY ADVANCE PROTOTYPE")
    pause()
    print("DONKEY KONG STOPS YOU, AND TOSSES YOU INTO OBLIVION.")
    game_over()

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
    await choice()

def texas_give():
    if not state["ti-83_confiscated"]:
        print("YOU GIVE HIM YOUR TI-83. HE LETS THE HOSTAGE GO AND RUNS AWAY.")
        pause()
        print("THE HOSTAGE WAS THE PRESIDENT OF TEXAS INSTRUMENTS!")
        pause()
        print("EXCELLENT!")
        pause()
        print("YOU TAKE IT AND START TO LEAVE, BUT HE'S NOT DONE YET.")
        pause()
        print("HE GIVES YOU A PLANE TICKET HOME, ON AN TOP SECRET CONCORDE.")
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
        game_over()

def texas_no():
    print("YOU RUN AWAY, BUT YOUR BAD KARMA CATCHES UP WITH YOU...")
    game_over()

def plane_menu():
    choice = menu("  DO WHAT NOW?  ", [
        ("SCALP TICKET", scalp_ticket),
        ("BOARD PLANE", board_plane)
    ])
    await choice()

def scalp_ticket():
    print("YOU SELL THE TICKET AND MAKE SOME MONEY, BUT YOU ARE STRANDED IN TEXAS!")
    pause()
    print("YOU TRY WALKING HOME, BUT YOU OBVIOUSLY DON'T MAKE IT.")
    game_over()

def board_plane():
    print("YOU BOARD THE PLANE TO GO HOME AND FALL ASLEEP.")
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
    await choice()

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
    choice = menu("WHAT DO YOU DO ?", [
        ("READ IT", area51_read),
        ("EAT IT", area51_eat)
    ])
    await choice()

def area51_eat():
    print("NOT BAD, BUT IT COULD HAVE USED SOME SALT.")
    pause()
    print("YOU THEN EXPERIENCE THE WORST CASE OF INDIGESTION EVER")
    game_over()

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
    await choice()

def area51_wrong_room():
    print("IF THAT'S TOO HARD, WHY DO YOU HAVE A GRAPHING CALC.?")
    game_over()

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
    await choice()

def area51_leak():
    print("AHHHHH...")
    pause()
    print("BUT YOU SOMEHOW MANAGE TO GET FLUSHED DOWN THE TOILET.")
    game_over()

def area51_drink():
    print("YOU SICKEN ME!")
    pause()
    print("SO MUCH SO THAT I THINK YOU SHOULD DIE.")
    game_over()

def area51_look():
    print("YOU LOOK AT THE AIR VENT AND GET A SUDDEN URGE TO CLIMB THROUGH IT")
    pause()
    print("SO YOU DO.")
    pause()
    area51_vent()

def area51_nap():
    print("YOU TAKE A NAP. BUT AS YOU DO, YOU BREATHE IN TOO MUCH FLATULENCE.")
    pause()
    print("YOUR LUNGS CAN'T TAKE IT.")
    game_over()

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
    print("SO THAT'S WHY YOU GOT THE URGE TO CUT YOUR WRISTS.")
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
    await choice()

def area51_bite():
    print("YOU TAKE A BIG BITE OUT OF AN ALIEN'S JUGULAR VEIN. YOU ARE SPRAYED WITH ITS ACIDIC BLOOD.")
    game_over()

def area51_sing():
    print("YOU START TO SING ALONG WITH THE SONG.")
    pause()
    print("NOW I MUST SMACK YOU.")
    game_over()

def area51_dance():
    print("YOU START TO DANCE ALONG WITH THE ALIENS. THEY ALL POINT AND LAUGH AT YOU.")
    pause()
    print("SELF-ESTEEM METER: |-| |-| |-| |-| |-| |-| |-|")
    pause()
    game_over()

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
    print("YOU ARE A HERO. YOU SAVED AREA51 FROM THE EVIL ALIEN SQUID CULT")
    pause()
    print("BUT SINCE IT IS CLASSIFIED INFO. NO ONE WILL EVER KNOW ABOUT IT.")
    pause()
    print("D'OH!")
    pause()
    print("SO YOU WALK HOME DEPRESSED.")
    pause()
    print("YES, I REALIZE ITS A LONG WAY.")
    pause()
    print("WHAT A DAY ITS BEEN.")
    pause()
    print("HEY, ISN'T THAT THE GIRL THAT YOU SAW EARLIER IN LUNCH?")
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
    pause()
    print("WHAT THE HELL KIND OF ENDING WAS THAT?!?!")
    pause()
    print("LETS TRY THAT ONE AGAIN.")
    pause()
    print("TIME TRAVELING...")
    pause()
    print("SO YOU KILLED THE ALIEN SQUID CULT AND YOU ARE A HERO.")
    pause()
    print("SO YOU WALK HOME AND YOU SEE THE GIRL FROM LUNCH.")
    pause()
    print("SHE MUST LIKE YOU, SHE KEEPS SHOWING UP ALONG THE WAY!")
    pause()
    print("SHE LEANS CLOSE TO YOUR EAR AND WHISPERS...")
    pause()
    print("'YOU KNOW WHAT I WANT TO DO...'")
    pause()
    print("'YEA... BUT I'M NOT REALLY IN THE MOOD.'")
    pause()
    final_menu()

def final_menu():
    choice = menu("  SO NOW WHAT?  ", [
        ("SCREAM", final_scream),
        ("DIG HOLE", final_dig),
        ("GIVE UP", final_giveup)
    ])
    await choice()

def final_giveup():
    print("WHAT KIND OF LOSER ARE YOU!?!")
    pause()
    print("YOU CAME ALL THIS WAY FOR... NOTHING!")
    game_over()

def final_scream():
    print("YOU SCREAM AS LOUD AS YOU CAN.")
    pause()
    print("'I'M ALIVE AND I GOT A HOT CHICK. HIT ME WITH YOUR BEST SHOT, MONDAY!!!'")
    pause()
    print("AND GUESS WHAT.")
    pause()
    print("IT DOES.")
    game_over()

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
    print("YOU CAN IMAGINE WHAT HAPPENS NEXT.")
    pause()
    print("USE YOUR IMAGINATION.")
    pause()
    print("HEHEHEHE.")
    pause()
    print("A HALF HOUR LATER, YOU DRIFT OFF TO SLEEP.")
    pause()
    print("AND YOU THINK TO YOURSELF...")
    pause()
    print("THAT DAY WAS AWESOME!")
    pause()
    print("      ROLL\n      THE\n    CREDITS!   ")
    wait()
    state["times_good_ending"] += 1
    credits()

def game_over():
    save_stats()
    print("\n---GAME--OVER---\nMONDAY HAS CLAIMED ANOTHER VICTIM!\n\nTRY AGAIN!")
    pause()
    main_menu()

# if __name__ == "__main__": # trying out copilot's solution to SyntaxError: 'await' outside async function
def da_game():
    load_stats()
    title_screen()

da_game()