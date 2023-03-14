import csv
import os.path

# define file paths for road, health, and inventory
road_file = "road.csv"
health_file = "health.txt"
inventory_file = "inventory.txt"

# initialize player's health and inventory
player_health = 100
potion_available = True

# define functions to retrieve current position, current health, and current inventory
def get_current_position():
    try:
        with open(road_file, "a+") as f:
            reader = csv.reader(f)
        for row in reader:
            if "X" in row:
                return row.index("X") + 1
    except:
        print("Error with current position function")

def get_current_health():
    try:
        if os.path.isfile(health_file) == False:
            with open(health_file, "a+") as f:
                f.write(100)
                return int(f.read())
        else:
            with open(health_file, "a+") as f:
                return int(f.read())
    except:
        print("Error with current health function")

def get_inventory():
    try:
        if os.path.isfile(inventory_file) == False:
            with open(inventory_file, "a+") as f:
                f.write(1)
                return int(f.read())
        else:
        with open(inventory_file, "a+") as f:
            return int(f.read())
    except:
        print("Error with get_inventory function")

# define functions for each possible action
def roll_dice():
    # define dice outcomes and their effects
    dice_outcomes = {
        1: -10,
        2: -1,
        3: "pray",
        4: -40,
        5: "double",
        6: 1
    }
    # roll the dice and determine the outcome
    import random
    outcome = random.randint(1, 6)
    if dice_outcomes[outcome] == "pray":
        prayer_outcome = random.randint(1, 10)
        if prayer_outcome == 7:
            return "win"
        else:
            return "no effect"
    elif dice_outcomes[outcome] == "double":
        # set a flag to indicate that the player's next movement will be doubled
        global double_movement
        double_movement = True
        return "no effect"
    else:
        # update the player's health and position
        global player_health
        if double_movement:
            double_movement = False
            outcome *= 2
        player_health += dice_outcomes[outcome]
        current_position = get_current_position()
        new_position = current_position + outcome
        if new_position < 1:
            new_position = 1
        elif new_position > 10:
            new_position = 10
        update_road(current_position, new_position)
        return outcome

def consume_potion():
    global player_health
    global potion_available
    if potion_available:
        player_health += 70
        if player_health > 100:
            player_health = 100
        potion_available = False
        update_inventory(potion_available)
        return "potion used"
    else:
        return "no potion"

def quit_game():
    # end the game and display the final score
    current_health = get_current_health()
    print("Game over! Final health:", current_health)
    if current_health >= 70:
        print("You win!")
    else:
        print("You lose.")

# define functions to update the road, health, and inventory files
def update_road(old_position, new_position):
    with open(road_file, "r") as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
        rows[0][old_position - 1] = "-"
        rows[0][new_position - 1] = "X"
    with open(road_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def update_health(current_health):
    with open(health_file, "w") as f:
        f.write(str(current_health))

def update_inventory(potion_available):
        with open(inventory_file, "w") as f:
            if potion_available:
                f.write("1")
            else:
                f.write("0")
'''define a function to display the current status to the user'''
def display_status():
        current_position = get_current_position()
        current_health = get_current_health()
        current_inventory = get_inventory()
        print("Current position:", current_position)
        print("Current health:", current_health)
        print("Potion available:", "Yes" if current_inventory else "No")

'''define the main game loop'''
def game_loop():
    while True:
        display_status()
        user_input = input("Enter r to roll the dice, p to consume a potion, or q to quit: ")
        if user_input == "r":
            outcome = roll_dice()
            print("You rolled a", outcome)
            if outcome == "win":
                print("You win!")
                break
            elif outcome == "no effect":
                print("Nothing happened.")
        elif user_input == "p":
            outcome = consume_potion()
            if outcome == "potion used":
                print("You consumed a potion and restored some health.")
            else:
                print("You don't have any potions left.")
        elif user_input == "q":
            quit_game()
            break
        else:
            print("Invalid input. Please try again.")
            

    '''start the game'''
double_movement = False
game_loop()

