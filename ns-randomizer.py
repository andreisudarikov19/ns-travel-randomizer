import pandas as pd
import os

# Load the stations CSV file
CSV = pd.read_csv('stations-2023-09.csv')

# Set the default menu selection
MENU_SELECT = 0

# Set the repeater selection
REPEATER = 0

# Count the number of task re-runs
RERUN = 0

### HOUSEKEEPING COMMANDS

def clear():
    os.system('clear')

def exit():
    clear()
    quit()

### USER INTERFACE COMMANDS

def main_menu():

    clear()

    HEADER = "Available commands:"

    print(HEADER)
    print("=" * len(HEADER))
    print("1 - Show random station")
    print("9 - Exit")

    main_input()

def main_input():

    global MENU_SELECT

    # Display prompt
    print(" ")
    MENU_SELECT = int(input("Enter command number: "))

    script_runner()

def repeat_input():
    
    global REPEATER

    # Display prompt
    print(" ")
    REPEATER = int(input("1 - Run again, 2 - Back to menu: "))

    repeat_runner()

### RUNNER RELAY BOX

def script_runner():

    global MENU_SELECT

    if MENU_SELECT == 1:
        show_random()
    if MENU_SELECT == 9:
        exit()
    else:
        print("(!) No command found, try again.")
        main_input()

def repeat_runner():

    global REPEATER
    global RERUN

    RERUN += 1

    if REPEATER == 1:
        script_runner()
    if REPEATER == 2:
        main_menu()
    else:
        print("(!) No command found, try again.")
        main_input()


### FUNCTION SCRIPTS

def show_random():

    global CSV

    clear()

    station = CSV.sample(n=1).iloc[0]

    # Display station information
    header = f"{'CODE':<6} {'NAME':<30} {'TYPE':<30} {'LOCATION'}"
    separator = '-' * (6 + 1 + 30 + 1 + 30 + 1 + 25)
    row = f"{station['code']:<6} {station['name_long']:<30} {station['type']:<30} ({station['geo_lat']}, {station['geo_lng']})"

    # Print the output into the console
    print (header)
    print (separator)
    print (row)

    repeat_input()

# Start the whole thing
main_menu()
