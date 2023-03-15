import csv
import os
import random



# define file paths for road, health, and inventory
road_file = "road.csv"
health_file = "health"
inventory_file = "inventory"
potion_available = "potion_avilable"

# define function to retrieve current position
def get_current_position():
    try:
        if os.path.isfile(road_file) == False:
            with open(road_file, 'w') as f:
                f.write("X,,,,,,,,,")
                return 1
        else:
            with open(road_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if "X" in row:
                        return (row.index("X") + 1)
                return 1  # Return a default value if X is not found
    except FileNotFoundError:
        print("The file does not exist.")
        return 1  # Return a default value on error
    except PermissionError:
        print("You don't have permission to access the file.")
        return 1  # Return a default value on error
    except Exception as e:
        print("An error occurred:", e)
        return 1  # Return a default value on error

def get_doubleMovement():
    try:
        with open(road_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if "XX" in row:
                        return (True)
                    else:
                        return (False)
    except FileNotFoundError:
        print("The file does not exist.")
        return 1  # Return a default value on error
    except PermissionError:
        print("You don't have permission to access the file.")
        return 1  # Return a default value on error
    except Exception as e:
        print("An error occurred:", e)
        return 1  # Return a default value on error

        

def update_position(steps):
    new_position = get_current_position() + steps
    with open(road_file, 'w') as f:
        for steps in range(10):
            if steps +1  == new_position:
                f.write('X')
            else:
                f.write(',')
    return 0
        

def get_current_health():
    try:
        if os.path.isfile(health_file) == False:
            with open(health_file, 'w') as f:
                f.write(str(100))
                return 100
        else:
            with open(health_file, 'r') as f:
                return int(f.read())
    except FileNotFoundError:
        print("The file does not exist.")
    except PermissionError:
        print("You don't have permission to access the file.")
    except Exception as e:
        print("An error occurred:", e)


def update_health(health):
    with open(health_file, 'w') as f:
        f.write(str(health))  

def get_inventory():
    try:
        if os.path.isfile(inventory_file) == False:
            with open(inventory_file, 'w') as f:
                f.write(str(70))
                return 70
        else:
            with open(inventory_file, 'r') as f:
                return int(f.read())
    except FileNotFoundError:
        print("The file does not exist.")
    except PermissionError:
        print("You don't have permission to access the file.")
    except Exception as e:
        print("An error occurred:", e)

# define functions for each possible action

def roll_dice():
    import random
    die = random.randint(1, 6)
    return die

def potion_available():
    try:
        if os.path.isfile(potion_available) == False:
            with open(inventory_file, 'w') as f:
                f.write(str(1))
                return 0
        else:
            with open(inventory_file, 'r') as f:
                return int(f.read())
    except FileNotFoundError:
        print("The file does not exist.")
    except PermissionError:
        print("You don't have permission to access the file.")
    except Exception as e:
        print("An error occurred:", e)

def consume_potion():

    potion_available = potion_available()
    player_health = get_current_health()

    if potion_available:
        player_health += 70
        if player_health > 100:
            player_health = 100
        potion_available = False
        update_health(player_health)
        update_inventory(potion_available )
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



def update_inventory(potion_available):
        with open(inventory_file, "w") as f:
            if potion_available:
                f.write("1")
            else:
                f.write("0")


'''Create Road Map'''
def roadMap(position):

    double_movement = get_doubleMovement()
    gameMap = []
    for steps in range(10):
        if steps == position - 1:
            if double_movement == True:
                gameMap.append('XX')
            else:
                gameMap.append('X')
        else:
            gameMap.append('|')
    return(gameMap)


def dice_outcomes(die):
        outcomes = {
        1: -10,
        2: -1,
        3: "pray",
        4: -40,
        5: "double",
        6: 1
    }
        return outcomes[die]

def getCurrentHealthStatus():
    
    player_health = get_current_health()
    print(f'Your current health is :{player_health}')

def gameStatus():
    getCurrentHealthStatus()
    double_movement = get_doubleMovement()
    position = get_current_position() 
    myMap = roadMap(position)
    print(*myMap,sep=' ')

'''define the main game loop'''
def game_loop():
    double_movement = get_doubleMovement()
    player_health = get_current_health()
    '''Starting game message'''
    

    gameStatus()
    print("Your journey begins.  you are")
    print("only at the first position.\n\n")
    
    while get_current_health() > 0:
        user_input = input("What will you do, Traveler?\n")
        if user_input == "r":
            die = roll_dice()
            print("You rolled a", die)
            outcome = dice_outcomes(die)
            if outcome == "win":
                print("You win!")
                break
            elif outcome == -10 or outcome == -40:
                player_health = get_current_health() + outcome 
                update_health(player_health)
                print(f'You took {abs(outcome)} damage')
                                
            elif outcome == 1 or outcome == -1:
                update_position(outcome)    # roll the dice and determine the outcome
                if double_movement == True:
                    update_position(outcome)
                    double_movement = False
                if outcome == 1:
                    print("You move forward")
                else:
                    print("You move back")
            elif outcome == "pray":
                prayer_outcome = random.randint(1, 10)
                if prayer_outcome == 7:
                    print ("You win!")
                    break
                else:
                    print("Nobody heard myour prayers")
            elif outcome == "double":
                double_movement = True
                # write to file the double XX          
        elif user_input == "p":
            potion_available = 70 - player_health
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
        
        gameStatus()

    '''start the game'''

game_loop()

'''Game clean up'''
try:
    os.remove(road_file)
    os.remove(health_file)
    os.remove(inventory_file)

except FileNotFoundError:
    print("The file does not exist.")
except PermissionError:
    print("You don't have permission to access the file.")
except Exception as e:
    print("An error occurred:", e)

