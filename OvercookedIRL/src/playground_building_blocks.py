# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 15:29:18 2022

@author: Kellen Cheng
"""


# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 14:43:02 2022

@author: Kellen Cheng
"""

# Import Statements
import os
import sys
import copy
import time
import queue
import socket
import pickle
import threading
import numpy as np

# # File Import Statements
# from config import *
# from player import *
# from sprites import *
# from counters import *
# from color_mouse import *
# from ingredients import * 

# %% Utility Functions

# Game Parameters
HEADER = 4096
stations = ["Cutting Board", "Stove", "Ingredients Stand", 
            "Plates Cupboard", "Submission Countertop", "Share Station"]

###############################################################################
'''
Action Codes (AKA first entry in the list of data we send to the server):
    -1   -> Do nothing (AKA error code or performed invalid action)
    0    -> Register
    1    -> Move player
    2    -> Pick up item
    3    -> Put down item
    4    -> Perform Gesture/Speech
    5    -> Submit dish
    6    -> Destroy player inventory
    7    -> Destroy station items
    8    -> Exit the game
    
Additional Gameplay Notes:
    - Cannot have both a separated plate and ingredient at a station at the
    same time. They only coexist when the ingredient is on the plate.
    - Our inventory may only contain one item (plate OR ingredient), however do
    note that it can contain a plate that is NOT EMPTY (i.e. has food on it)
'''
###############################################################################

# Function: Prints the game status as an easy to read string
def print_status_as_string(status):
    # If dealing with a nonetype, print NONE and return
    if (status == None): 
        print("State is NONE!")
        return
    
    loc = status[0]
    inventory = status[1]
    pantry = status[2]
    target = status[3]
    share = status[4]
    ID = status[5]
    name = status[6]
    
    print("Current Player location:", loc)
    print("Current Player Inventory:", inventory)
    print("Pantry Ingredients:", pantry)
    print("Target Recipe:", target)
    print("Share Station:", share)
    print("Player ID:", str(ID), ", with Player Name:", name)

# Function: Get data (blocking version)
def get_data(client_socket, condition=None, count=0):
    # If we don't set a certain amount of timed data retrieval
    if (count == 0):
        while True:
            try: condition = pickle.loads(client_socket.recv(HEADER))
            except: condition = None
            
            if (condition != None): break
    else:
        while count > 0:
            try: condition = pickle.loads(client_socket.recv(HEADER))
            except: condition = None
            
            if (condition != None): break    
            count -= 1
    return condition

# Function: Get data (nonblocking version)
def get_unblocked_data(client_socket, condition=None):
    try: 
        condition = pickle.loads(client_socket.recv(HEADER))
        # print(condition)
        #print('in a pickle!!!')
    except: condition = None
    return condition

# Function: Blocked accept (blocking version)
def get_accept(server):
    while True:
        try: 
            client, address = server.accept() 
            break
        except: 
            pass
    return client, address

def game(client_socket):
    print("############### Welcome to Overcooked IRL ###############")
    current = None # Local copy of the name of the current player location
    
    # Set a dedicated thread for checking for updates to the game state
    input_thread = threading.Thread(target=retrieve_state, 
                                    args=(client_socket, ), 
                                    daemon=True)
    input_thread.start()
        
    # Begin game logic
    changes = 0
    while True:      
        # Move to a station on the first iteration, perform action otherwise
        if (changes == 0):
            current = move(client_socket, header=HEADER)
            changes = 1
        else:
            current = action(client_socket, header=HEADER, loc=current)
        print("_________________________________________________")

        # Prevent simultaneous erroneous fetching inbetween internal actions            
        time.sleep(0.01)
        pass
   
# Function: Register a game player
def register(client_socket, header=HEADER): # ACTION = 0
    name = input("Please enter your player's name:\n")
    client_socket.send(pickle.dumps([0, name])) # Send information to be stored
    
# Function: Move stations as a player
def move(client_socket, header=HEADER): # ACTION = 1
    print("Select a station from one of the following below:")
    print("(1) Cutting Board (2) Stove (3) Ingredients Stand" \
                 " (4) Plates Cupboard (5) Submission Countertop" \
                     " (6) Share Station\n")
    dest = int(input())
    client_socket.send(pickle.dumps([1, dest])) # Send information to be stored
    return stations[dest - 1]

# Function: Non-blocking input
def retrieve_state(client_socket):
    prev = None
    while (True):
        command = get_unblocked_data(client_socket)
        if (command != None and command != prev):
            prev = command
            # print(command)
            print_status_as_string(command)
            print("End of state:-----------------------")
        pass

# Function: Complete an action
def action(client_socket, header=HEADER, loc=None): # ACTION = VARIABLE
    print("Select an option from one of the following below:")
    print("(1) Move (2) Pick Up (3) Put Down" \
                 " (4) Gesture/Speech (5) Submit (6) Trash Inventory"\
                     " (7) Trash Station (8) Exit \n")
    dest = int(input())
    
    if (dest == 1): # ACTION = 1
        # Move
        loc = move(client_socket, header)
    elif (dest == 2 and loc != stations[2]): # ACTION = 2
        # Pick up but not at the pantry
        client_socket.send(pickle.dumps([2]))
    elif (dest == 3): # ACTION = 3
        # Put down item
        client_socket.send(pickle.dumps([3]))
    elif (dest == 4 or (dest == 2 and loc == stations[2])): # Gesture/Speech
        # Pick up item if currently at the ingredients pantry
        if (loc == stations[2]): # ACTION = 4
            # Replace w/ relevant speech later!
            speech = input("Select an item from the pantry:\n") 
            client_socket.send(pickle.dumps([4, speech]))
        else: # ACTION = 4
            gesture = 1 # Replace w/ relevant gesture later!
            client_socket.send(pickle.dumps([4, gesture]))
    elif (dest == 5): # ACTION = 5
        # Attempt to submit our dish
        client_socket.send(pickle.dumps([5]))
    elif (dest == 6): # ACTION = 6
        # Throw away our inventory!
        client_socket.send(pickle.dumps([6]))
    elif (dest == 7): # ACTION = 7
        # Throw away everything at the station!
        client_socket.send(pickle.dumps([7]))
    elif (dest == 8): # ACTION = 8
        sys.exit()
    
    return loc

# Class: Station Manager
class Kitchen_Stations:
    # Constructor method to initialize all kitchen stations
    def __init__(self, stations, idx):
        # Store stations in list for versatility of access
        self.idx = idx # Index of where the ingredient stand is
        self.stations = stations
        self.stations_list = []
        self.plate_counter = 0
        
        for name in stations:
            self.stations_list.append(Station(name))
            pass
        
    # Determine if station is empty
    def is_empty(self, station_name):
        if (self.stations_list[self.stations.index(station_name)].ingredients == []):
            return True
        else:
            return False
    
    # Set down item onto the kitchen station
    def add_item(self, station_name, item):
        # Place our inventory onto a station
        self.stations_list[self.stations.index(station_name)].ingredients.append(item)
        
    # Find item if choosing at a station
    def find_item(self, station_name, target):
        # Loop through the station's ingredients to see if we found it
        for item in self.stations_list[self.stations.index(station_name)].ingredients:
            # N.B. We will only deal with ingredients, NOT PLATES FOR NOW
            if (item.ingredient_name == target): return item
        
        return None
        
    # Pick up item from the kitchen station
    def pick_item(self, station_name, target=None):
        # Do nothing if the station has no item
        if (self.stations_list[self.stations.index(station_name)].ingredients == []):
            return None
        
        # Pick up target item if specified
        if (target != None):
            item = self.find_item(station_name, target)
            
            # Remove item from the station, if valid (excluding pantry and plates)
            if (item != None and (station_name != stations[2] and
                                  station_name != stations[3])):
                self.stations_list[self.stations.index(station_name)].ingredients.remove(item)
                return item
            elif (item != None and station_name == stations[2]):
                # Pantry should have an unlimited supply!
                return copy.deepcopy(item)
            elif (item != None and station_name == stations[3]):
                # Plates should have an unlimited supply!
                item.increment_ID()
                return copy.deepcopy(item)
        
        # Pick up item from station and clear the station (N.B. Fix for pantry)
        item = self.stations_list[self.stations.index(station_name)].ingredients[0]
        
        # Remove item from the station
        self.stations_list[self.stations.index(station_name)].ingredients.remove(item)
        return item
    
    # Set the old station to be denoted empty/free
    def set_free(self, station_name):
        self.stations_list[self.stations.index(station_name)].busy = False
    
    # Set the target station to be denoted busy
    def set_busy(self, station_name):
        self.stations_list[self.stations.index(station_name)].busy = True
        
    # Print out the states of every station in the kitchen
    def display_kitchen(self):
        status = ""
        for location in self.stations_list:
            message = location.station_name
            message += ", " + str(location.ingredients)
            message += ", busy: " + str(location.busy)
            message += " ||| "
            status += message
        print(status)
        
# Class: Station
class Station:
    # Constructor method to initialize a kitchen station
    def __init__(self, station_name):
        self.station_name = station_name
        self.ingredients = [] # Initialize station to have no ingredients
        self.busy = False # Initialize station to be free    

# Class: Player
# class Player:
#     # Constructor method to initialize game player
#     def __init__(self, name):
#         self.name = name
        
#         # Initialize with empty inventories and beginning at the start location
#         self.location = None # N.B. String of station name
#         self.inventory = []
        
# Plate Class
class Plate:
    def __init__(self, ID_number):
        self.ID_number = ID_number # Identifier
        self.contents = []
        
    def plate_item(self, item):
        self.contents.append(item)
        
    def increment_ID(self):
        self.ID_number += 1
        
# Ingredient Class
class Ingredient:
    def __init__(self, name, cut_state, cook_state):
        self.ingredient_name = name
        self.cut_state = cut_state
        self.cook_state = cook_state
        
    def compare(self, ingred2):
        # Compare two ingredients' by similarity
        cut = abs(self.cut_state - ingred2.cut_state)
        cook = abs(self.cook_state - ingred2.cook_state)
        return cut + cook
        
# Recipe Class and Methods
def generate_recipe():
    # Pick a type of recipe to generate
    recipe_types = ["sandwich", "soup", "steak", "noodles"]
    recipe_type = recipe_types[np.random.randint(3)]
    
    # Depending on the recipe type, choose ingredients wisely!
    if (recipe_type == recipe_types[0]):
        # Generate a sandwich type recipe (2 Bread, 1 Meat, 1/2 Vegetable)
        bun1 = Ingredient("Bread", 0, 1)
        bun2 = Ingredient("Bread", 0, 1)
        meat = Ingredient("Beef", 1, 3)
        
        # If needed, we can even randomize whether it's lettuce/tomato/both
        toppings = Ingredient("Lettuce", 3, 0)
        materials = [bun1, bun2, meat, toppings]
        return Recipe(materials)
    elif (recipe_type == recipe_types[1]):
        # Generate a soup type recipe
        tofu = Ingredient("Tofu", 5, 3)
        cabbage = Ingredient("Cabbage", 2, 3)
        chicken = Ingredient("Chicken", 4, 3)
        
        # If needed, further randomization/customization
        materials = [tofu, cabbage, chicken]
        return Recipe(materials)
    elif (recipe_type == recipe_types[2]):
        # Generate a steak type recipe
        steak = Ingredient("Beef", 0, 6)
        potato = Ingredient("Potato", 2, 2)
        celery = Ingredient("Celery", 3, 3)
        
        # If needed, further randomization/customization
        materials = [steak, potato, celery]
        return Recipe(materials)
    else: # Once more types are added, we can alter this conditional
        # Generate a noodle type recipe/further recipe
        print("Still under development!")
        pass
    pass

class Recipe:
    def __init__(self, materials):
        self.materials = materials
        
    # Get the ingredients of the recipe
    def get_ingredients(self):
        ingredient_names = []
        
        for item in self.materials:
            ingredient_names.append(item.ingredient_name)
            pass
        
        return ingredient_names
        
    # Return the string representation of the recipe
    def recipe_string(self):
        representation = ""
        mats = []
        
        for item in self.materials:
            raw = "["
            details = [str(item.ingredient_name), str(item.cut_state), 
                       str(item.cook_state)]
            raw += ", ".join(details) + "]"
            mats.append(raw)
            pass
        
        return mats
        
    # Attribute a score to the target recipe
    def score_dish(self, dish):
        # Dish is a plate with all the necessary ingredients
        target_dish = copy.deepcopy(self.materials)
        test_dish = copy.deepcopy(dish)
        
        score = 0
        
        # Evaluate each element of the dish
        for item in test_dish:
            match = [part for part in target_dish if part.ingredient_name == item.ingredient_name]
            
            # Calculate the score for each item
            if (match == []):
                # No match found, we added a wrong ingredient!
                score -= 5
            else:
                target_item = match[0]
                diff = target_item.compare(item)
                score -= diff * 1 # Every different in cut/cook is penalized
            
            # Remove the items from our copies!
            target_dish.remove(match[0])
            pass
        
        return score
    
def format_timedelta(td):
    minutes, seconds = divmod(td.seconds + td.days * 86400, 60)
    hours, minutes = divmod(minutes, 60)
    return '{:02d}:{:02d}'.format(minutes, seconds)
    
# %% Game Class 
'''
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_idle_spritesheet = Spritesheet('../img/chef1/chef1_idle_32.png')
        self.character_run_spritesheet = Spritesheet('../img/chef1/chef1_run_32.png')
        self.kitchen_spritesheet = Spritesheet('../img/12_Kitchen_32x32.png')
        self.kitchen_shadowless_spritesheet = Spritesheet('../img/12_Kitchen_Shadowless_32x32.png')
        self.character_chop_spritesheet = Spritesheet('../img/chef1/chop_idle.png')
        self.character_stir_spritesheet = Spritesheet('../img/chef1/chef_stir.png')
        self.character_pickup_spritesheet = Spritesheet('../img/chef1/chef1_pickup.png')
        self.character_putdown_spritesheet = Spritesheet('../img/chef1/chef1_place.png')
        self.cursor_spritesheet = Spritesheet('../img/cursor.png')
        self.knife_animation = Spritesheet('../img/chop_knife.png')
        self.plates_stack = Spritesheet('../img/individual_tiles/dish_pile.png')
        self.inventory_spritesheet = Spritesheet('../img/inventory_tile.png')
        self.bun_spritesheet = Spritesheet('../img/recipes/bun_spritesheet.png')
        self.meat_spritesheet = Spritesheet('../img/recipes/meat_spritesheet.png')
        self.tomato_spritesheet = Spritesheet('../img/recipes/tomato_spritesheet.png')
        self.lettuce_spritesheet = Spritesheet('../img/recipes/lettuce_spritesheet.png')
        self.plate_spritesheet = Spritesheet('../img/recipes/plate_spritesheet.png')
        self.progress_spritesheet = Spritesheet('../img/progress_bar.png')
        self.knife_icon = Spritesheet('../img/knife_icon.png')
        self.cook_icon = Spritesheet('../img/cook_icon.png')
        self.speaking_animation = Spritesheet('../img/speaking_animation.png')

        self.fridge_open_animation = Spritesheet('../img/object_animations/fridge_open_spritesheet.png')
        self.fridge_close_animation = Spritesheet('../img/object_animations/fridge_close_spritesheet.png')

        self.mouse = ColorMouse()

    def createTilemap(self,tilemap,layer):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                if column == '0':
                    BackgroundObject(self, self.plates_stack, 0, 0, j, i, layer, (self.all_sprites))
                elif column == '!':
                    IngredientsCounter("Tomato",self, self.kitchen_spritesheet,white_counter["!"][0],white_counter["!"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.ingredients_stands))
                elif column == '^':
                    IngredientsCounter("Lettuce",self, self.kitchen_spritesheet,white_counter["!"][0],white_counter["!"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.ingredients_stands))
                elif column == '(':
                    IngredientsCounter("Meat",self, self.kitchen_spritesheet,white_counter["!"][0],white_counter["!"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.ingredients_stands))
                elif column == ')':
                    IngredientsCounter("Bun",self, self.kitchen_spritesheet,white_counter["!"][0],white_counter["!"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.ingredients_stands))
                elif column == 'E':
                    Counter(self, self.kitchen_spritesheet,white_counter["E"][0],white_counter["E"][1],j,i,layer,(self.all_sprites,self.counters,self.bottom_perspective_counters))
                elif column == '$':
                    ChopCounter(self, self.kitchen_spritesheet,white_counter["B"][0],white_counter["B"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.chopping_stations))
                elif column == '*':
                    IngredientsCounter("Plate",self, self.kitchen_spritesheet,white_counter["H"][0],white_counter["H"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.plate_stations))
                elif column == '%':
                    CookCounter('pan',self, self.kitchen_spritesheet,white_counter["%"][0],white_counter["%"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.cooking_stations))
                elif column == '&':
                    Counter(self, self.kitchen_spritesheet,white_counter["&"][0],white_counter["&"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.submit_stations))
                elif column == 'B':
                    Counter(self, self.kitchen_spritesheet,white_counter["B"][0],white_counter["B"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters))
                elif column == 'J':
                    Counter(self, self.kitchen_spritesheet,white_counter["J"][0],white_counter["J"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.bottom_perspective_counters))
                elif column == 'G':
                    Counter(self, self.kitchen_spritesheet,white_counter["G"][0],white_counter["G"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.left_counters))
                elif column == 'H':
                    Counter(self, self.kitchen_spritesheet,white_counter["H"][0],white_counter["H"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.right_counters))
                elif column == 'H':
                    Counter(self, self.kitchen_spritesheet,white_counter["H"][0],white_counter["H"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.right_counters))
                elif column == 'V':
                    BackgroundObject(self,self.inventory_spritesheet,0,0,j,i,layer,(self.all_sprites))             
                elif column == 'S':
                    Counter(self, self.kitchen_spritesheet,white_counter["S"][0],white_counter["S"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.bottom_perspective_counters))
                elif column == 'Z':
                    BackgroundObject(self,self.kitchen_shadowless_spritesheet,front_items["Z"][0],front_items["Z"][1],j,i,layer,(self.all_sprites))   
                elif column == 'U':
                    BackgroundObject(self,self.kitchen_shadowless_spritesheet,front_items["U"][0],front_items["U"][1],j,i,layer,(self.all_sprites))   
                elif column == 'Y':
                    BackgroundObject(self,self.kitchen_shadowless_spritesheet,front_items["Y"][0],front_items["Y"][1],j,i,layer,(self.all_sprites))   
                elif column == 'W':
                    BackgroundObject(self,self.kitchen_shadowless_spritesheet,back_items["W"][0],back_items["W"][1],j,i,layer,(self.all_sprites))   
                elif column == 'X':
                    BackgroundObject(self,self.kitchen_shadowless_spritesheet,back_items["X"][0],back_items["X"][1],j,i,layer,(self.all_sprites))   
                elif column != "." and column != "P":
                    Counter(self, self.kitchen_spritesheet,white_counter[column][0],white_counter[column][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters))
        print('Created tilemap!')

    def new(self):
        # a new game starts
        self.playing = True

        # initialize empty sprite groups
        self.all_sprites = pygame.sprite.LayeredUpdates()   # layered updates object
        self.counters = pygame.sprite.LayeredUpdates()
        self.block_counters = pygame.sprite.LayeredUpdates()
        self.bottom_perspective_counters = pygame.sprite.LayeredUpdates()
        self.top_perspective_counters = pygame.sprite.LayeredUpdates()
        self.chopping_stations = pygame.sprite.LayeredUpdates()
        self.plate_stations = pygame.sprite.LayeredUpdates()
        self.ingredients_stands = pygame.sprite.LayeredUpdates()
        self.cooking_stations = pygame.sprite.LayeredUpdates()
        self.submit_stations = pygame.sprite.LayeredUpdates()
        self.left_counters = pygame.sprite.LayeredUpdates()
        self.right_counters = pygame.sprite.LayeredUpdates()
        self.cursor = Cursor(self,8,9)
        self.player = Player(self,6,4)

        self.animations = pygame.sprite.LayeredUpdates()

        self.createTilemap(counter_tilemap_back,COUNTER_BACK_LAYER)
        self.createTilemap(counter_tilemap_back_items,COUNTER_BACK_ITEMS_LAYER)
        self.createTilemap(counter_tilemap,COUNTER_LAYER)
        self.createTilemap(counter_tilemap_2,COUNTER_FRONT_LAYER)
        self.createTilemap(counter_front_items_tilemap,COUNTER_FRONT_LAYER+1)

        ProgressBar(self, self.progress_spritesheet, 0*TILE_SIZE, 0*TILE_SIZE, COUNTER_LAYER, (self.all_sprites), 3*TILE_SIZE, TILE_SIZE, self.player)
        self.mouse.setupMouse()

        self.setup_mqtt()

    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.player.dest_x = (int(pos[0]/32) * 32)
                self.player.dest_y = ((int(pos[1]/32)-1) * 32)
                print('CLICK')
                print(int(pos[0]/32) * 32, int(pos[1]/32) * 32)
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        # run the update method of every sprite in the all_sprites group
        self.all_sprites.update() 

    def draw(self):
        # game loop draw
        self.screen.fill((0,0,0))

        # draws the image and rect of all sprites in the all_sprites group onto the screen
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def setup_audiofile(self):
        i = 0
        while os.path.exists("speech%s.txt" % i):
            i += 1
        self.speech_log = open("speech" + str(i) + ".txt", "a")

    def setup_mqtt(self):
        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        self.client.on_message = on_message
        self.client.user_data_set(self)

        self.client.connect_async("test.mosquitto.org")
        self.client.connect("test.mosquitto.org", 1883, 60)
        self.client.loop_start()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.client.publish('overcooked_mic', "stop", qos=1)
        self.client.loop_stop()
        self.client.disconnect()
        # self.speech_log.close()
        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass
'''
     

    