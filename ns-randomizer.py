import pandas as pd
import os
import yaml

# Load the stations CSV file
CSV = pd.read_csv('stations-2023-09.csv')
VISITED_FILE = 'visited.yaml'

# Set the default menu selection
MENU_SELECT = 0

# Set the repeater selection
REPEATER = 0

# Count the number of task re-runs
RERUN = 0

### VISITED STATION LIST COMMANDS

# Ensure visited.yaml exists with base structure
if not os.path.exists(VISITED_FILE):
    with open(VISITED_FILE, 'w') as f:
        yaml.dump({'visited': []}, f)

# Load visited codes
def load_visited():
    with open(VISITED_FILE, 'r') as f:
        data = yaml.safe_load(f)
    return data['visited']

# Save visited codes
def save_visited(codes):
    with open(VISITED_FILE, 'w') as f:
        yaml.dump({'visited': codes}, f)

def mark_visited():
    codes = load_visited()
    codes.append({'code': CURRENT_SUGGESTED})
    save_visited(codes)
    print(f"Station {CURRENT_SUGGESTED} marked as visited.")
    input("Press Enter to suggest a new station...")
    clear()
    suggest_station()


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
    print("2 - Suggest a station")
    print("3 - List visited stations")
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

def suggest_repeat_input():
    print(" ")
    choice = int(input("1 - Run again, 2 - Back to menu, 3 - Mark visited: "))

    if choice == 1:
        suggest_station()
    elif choice == 2:
        main_menu()
    elif choice == 3:
        mark_visited()
    else:
        print("(!) No command found, try again.")
        suggest_repeat_input()

### RUNNER RELAY BOX

def script_runner():

    global MENU_SELECT

    if MENU_SELECT == 1:
        show_random()
    if MENU_SELECT == 2:
        suggest_station()
    if MENU_SELECT == 3:
        list_visited()
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
    code_width = max(len('CODE'), len(str(station['code']))) + 2
    name_width = max(len('NAME'), len(station['name_long'])) + 2
    type_width = max(len('TYPE'), len(station['type'])) + 2
    location_str = f"({station['geo_lat']}, {station['geo_lng']})"
    location_width = max(len('LOCATION'), len(location_str))

    header = f"{'CODE':<{code_width}}{'NAME':<{name_width}}{'TYPE':<{type_width}}{'LOCATION':<{location_width}}"
    separator = '-' * (code_width + name_width + type_width + location_width)
    row = f"{station['code']:<{code_width}}{station['name_long']:<{name_width}}{station['type']:<{type_width}}{location_str:<{location_width}}"

    # Print the output into the console
    print (header)
    print (separator)
    print (row)

    repeat_input()

def suggest_station():
    visited_codes = [v['code'] for v in load_visited()]
    csv_nl = CSV[CSV['country'] == 'NL']

    while True:
        station = csv_nl.sample(n=1).iloc[0]
        if station['code'] not in visited_codes:
            break

    clear()

    code_width = max(len('CODE'), len(str(station['code']))) + 2
    name_width = max(len('NAME'), len(station['name_long'])) + 2
    type_width = max(len('TYPE'), len(station['type'])) + 2
    location_str = f"({station['geo_lat']}, {station['geo_lng']})"
    location_width = max(len('LOCATION'), len(location_str))

    # ANSI color codes
    YELLOW = '\033[93m'
    RESET = '\033[0m'   

    header = f"{'CODE':<{code_width}}{'NAME':<{name_width}}{'TYPE':<{type_width}}{'LOCATION':<{location_width}}"
    separator = '-' * (code_width + name_width + type_width + location_width)
    name_colored = f"{YELLOW}{station['name_long']}{RESET}"
    row = f"{station['code']:<{code_width}}{name_colored:<{name_width + len(YELLOW) + len(RESET)}}{station['type']:<{type_width}}{location_str:<{location_width}}"

    print(header)
    print(separator)
    print(row)

    # Store the current station globally for marking visited
    global CURRENT_SUGGESTED
    CURRENT_SUGGESTED = station['code']

    suggest_repeat_input()


def list_visited():
    clear()
    
    # Load visited codes
    visited_entries = load_visited()
    visited_codes = [v['code'] for v in visited_entries]
    
    if not visited_codes:
        print("No stations marked as visited yet.")
        input("\nPress Enter to return to main menu.")
        main_menu()
        return

    # Filter CSV by visited codes
    csv_nl = CSV[CSV['country'] == 'NL']
    visited_stations = csv_nl[csv_nl['code'].isin(visited_codes)]

    # Prepare location strings
    visited_stations = visited_stations.copy()
    visited_stations['location_str'] = visited_stations.apply(lambda x: f"({x['geo_lat']}, {x['geo_lng']})", axis=1)

    code_width = max(len('CODE'), visited_stations['code'].str.len().max()) + 2
    name_width = max(len('NAME'), visited_stations['name_long'].str.len().max()) + 2
    type_width = max(len('TYPE'), visited_stations['type'].str.len().max()) + 2
    location_width = max(len('LOCATION'), visited_stations['location_str'].str.len().max())

    # ANSI color codes
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    header = f"{'CODE':<{code_width}}{'NAME':<{name_width}}{'TYPE':<{type_width}}{'LOCATION':<{location_width}}"
    separator = '-' * (code_width + name_width + type_width + location_width)

    print(header)
    print(separator)

    for _, station in visited_stations.iterrows():
        name_colored = f"{GREEN}{station['name_long']}{RESET}"
        row = f"{station['code']:<{code_width}}{name_colored:<{name_width + len(GREEN) + len(RESET)}}{station['type']:<{type_width}}{station['location_str']:<{location_width}}"
        print(row)

    # Print summary stats
    total_nl = csv_nl.shape[0]
    visited_count = len(visited_codes)
    to_go_count = total_nl - visited_count

    print("\nSummary:")
    print(f"- Stations visited: {GREEN}{visited_count}{RESET}")
    print(f"- To go: {YELLOW}{to_go_count}{RESET}")

    # Print progress bar
    bar_length = 40
    visited_ratio = visited_count / total_nl
    visited_blocks = int(bar_length * visited_ratio)
    to_go_blocks = bar_length - visited_blocks

    progress_bar = f"{GREEN}{'█' * visited_blocks}{YELLOW}{'█' * to_go_blocks}{RESET}"

    print(f"\nProgress: [{progress_bar}] {visited_ratio * 100:.2f}% visited")

    input("\nPress Enter to return to menu.")
    main_menu()

# Start the whole thing
main_menu()
