# text based implementation of Overcooked IRL single player mode only

import sys
import os
from Ingredients import Ingredients
from Station_Manager import Station_Manager
from Player import Player
from Plate import Plate
# import speech_recognition as sr
import copy

plate_num = 0 # first plate number starts at 0
valid_ingredients = ['tomato', 'cheese', 'bread', 'beef', 'lettuce']
valid_actions = ['put down', 'pick up']
stations = ["Cutting Station", "Stove Station", "Ingredients Station", "Submit Station", "Share Station", "Plate Station"]
station_num = ["1", "2", "3", "4", "5", "6"]
station_manager = Station_Manager()
target_recipe = [Ingredients("tomato", 2, "Cutting Station"), Ingredients("cheese", 3, "Cutting Station"), Ingredients("bread", 1, "Cutting Station"), Ingredients("beef", 1, "Stove Station"), Ingredients("lettuce", 0)]
base_ingr = [Ingredients("tomato", 0, "Cutting Station"), Ingredients("cheese", 0, "Cutting Station"), Ingredients("bread", 0, "Cutting Station"), Ingredients("beef", 0, "Stove Station"), Ingredients("lettuce", 0)]


def main():
    os.system('cls') # use cls for PowerShell; may need to change for other output terminals
    print("Welcome to OvercookedIRL!")
    print("Instructions: If you see option names with numbers in front, only type the number and press Enter.")
    print("If you see only option names, type the exact option name and press Enter.\n")
    print ("1.) Start")
    print ("2.) Load")
    print ("3.) Exit")
    option = input("-> ")
    if option == "1":
        start()
    elif option == "2":
        pass
    elif option == "3":
        sys.exit()
    else: 
        main()

def start():
    os.system('cls')
    print("Hello, what is your name (please type in your name): ")
    option = input("-> ")
    global PlayerIG
    PlayerIG = Player(option)
    start1()

def start1():
    os.system('cls')
    print ("Name: %s" % PlayerIG.name)
    print("Inventory: Empty")
    print("Plate Number: None")
    print("Location: %s\n" % PlayerIG.location)
    pick_station()

def start2():
    os.system('cls')
    print ("Name: %s" % PlayerIG.name)
    if PlayerIG.inventory:
        print("Inventory: %s" % PlayerIG.inventory[0].ingredient_name)
    else:
        print("Inventory: Empty")
    if PlayerIG.plate:
        print("Plate Number: %s" % PlayerIG.plate[0].plate_number)
    else:
        print("Plate Number: None")    
    print("Location: %s\n" % PlayerIG.location)

    print("What do you want to do?")
    print ("1.) Move")
    print ("2.) Pick Up")
    print ("3.) Put Down")
    print ("4.) Action")
    print ("5.) Submit ")
    option = input("-> ")
    if option == "1":
        pick_station()
    elif option == "2":
        pickup()
    elif option == "3":
        putdown()
    elif option == "4":
        action()
    elif option == "5":
        submit()
    else:
        start2()

def pick_station(): 
    os.system('cls')
    print ("Which station do you want to go to?")    
    print ("1.) Cutting Station")
    print ("2.) Stove Station")
    print ("3.) Ingredients Station")
    print ("4.) Submit Station")
    print ("5.) Share Station")
    print ("6.) Plate Station")
    option = input("-> ")
    if option in station_num:
        station_int = int(option) - 1
        move(stations[station_int])
    else: 
        start2()

def move(station_name):
    PlayerIG.location = station_name
    start2()

def action():
    os.system('cls')
    global station_manager
    if (PlayerIG.location == "Ingredients Station") and not PlayerIG.inventory:
        print ("What ingredient do you want?")
        #listen_ingredients()
        print(*valid_ingredients, sep = ", ")
        option = input("-> ")
        if option in valid_ingredients:
            n = 0
            while n < len(base_ingr): # is there a better way to access a single attribute of a list of objects?
                if option == base_ingr[n].ingredient_name:
                    PlayerIG.inventory.append(copy.copy(base_ingr[n])) # want new object that is a copy; don't want to reference the same exact object to use
                    break
                n += 1
            start2()
        else: 
            start2()
    elif (PlayerIG.location == "Ingredients Station") and PlayerIG.inventory:
        print("Your inventory is full.")
        print("Do you want to replace your item in your inventory?")
        print("1.) Yes")
        print("2.) No")
        option = input("-> ")
        if option == "1":
            PlayerIG.inventory.clear()
            print(*valid_ingredients, sep = ", ")
            option = input("-> ")
            if option in valid_ingredients:
                n = 0
                while n < len(base_ingr):
                    if option == base_ingr[n].ingredient_name:
                        PlayerIG.inventory.append(base_ingr[n])
                        break
                    n += 1
                start2()
            else: 
                start2()
        elif option == "2":
            start2()
        else:
            action()
    elif PlayerIG.location in ["Share Station", "Submit Station"]: # these have other specific functions
        start2()
    else: 
        n = 0
        while n < len(station_manager.stations):
            if PlayerIG.location == station_manager.stations[n].station_name:
                if station_manager.stations[n].ingredient: # if the station has an ingredient, process the item
                    station_manager.stations[n].ingredient.state += 1
                    break
                else:
                    start2()
            n += 1

# NOT for picking up ingredients at INGREDIENT STATION; pickup anything else elsewhere
def pickup():
    os.system('cls')
    global station_manager
    if not PlayerIG.plate: # if player is holding 0 plates
        if PlayerIG.location == "Plate Station":
            global plate_num
            PlayerIG.plate.append(Plate(plate_num, 0)) # player now holds an empty plate
            plate_num += 1
            start2()
        elif PlayerIG.location == "Share Station": # need to add case to pick up plates from shared location; for multiplayer only
            pass
        else: # add unprepared foods to inv if player inv is empty, but do nothing if player inv is full; cannot pick up prepared ingr
            if not PlayerIG.inventory:
                n = 0
                while n < len(station_manager):
                    if (PlayerIG.location == station_manager.stations[n].station_name) and (station_manager.stations[n].ingredients.state == 0):
                        PlayerIG.inventory.append(station_manager.stations[n].ingredients)
                        station_manager[n].busy = 0
                        station_manager[n].ingredients = None
                        break
                    n += 1
                start2()
            else:
                start2()         
    else: # if player is holding a plate
        if PlayerIG.location in ["Plate Station", "Ingredients Station", "Submit Station"]:
            start2()
        elif PlayerIG.location == "Share Station": # add when share station is necessary
            pass
        else:  # add unprepared foods to inv if player inv is empty, but do nothing if player inv is full; add prepared ingr to plate
            if not PlayerIG.inventory:
                n = 0
                while n < len(station_manager):
                    if (PlayerIG.location == station_manager.stations[n].station_name) and (station_manager.stations[n].ingredients.state == 0):
                        PlayerIG.inventory.append(station_manager.stations[n].ingredients)
                        station_manager[n].busy = 0
                        station_manager[n].ingredients = None
                        break
                    if (PlayerIG.location == station_manager.stations[n].station_name) and (station_manager.stations[n].ingredients.state > 1):
                        PlayerIG.plate.append(station_manager.stations[n].ingredients)
                        station_manager[n].busy = 0
                        station_manager[n].ingredients = None
                        break
                    n += 1
            else:
                start2()

# player can only put down ingredients onto a station that processes food; plates are always kept with the player for now
# can only put down ingredients at a station if the ingredients belong to that station
def putdown():
    os.system('cls')
    global station_manager
    if not PlayerIG.inventory:
        start2()
    else:
        ingredient = PlayerIG.inventory[0]
        n = 0
        while n < len(station_manager.stations):
            if (PlayerIG.location == station_manager.stations[n].station_name) and (ingredient.prepare_station == station_manager.stations[n].station_name):
                if (station_manager[n].busy == 0):
                    station_manager[n].busy = 1
                    station_manager.stations[n].ingredient = ingredient
                    PlayerIG.inventory.clear()
                    break
            n += 1
        start2()


# only applies to Submit Station
def submit():
    os.system('cls')
    if PlayerIG.location == "Submit Station":
        if not PlayerIG.plate:
            start2()
        else:
            if PlayerIG.plate[0].ingredients == target_recipe:
                print("Good job!")
                # total_points += 1
            else:
                print("WRONG RECIPE")
                # total_points -= 1
            PlayerIG.plate.clear()
            start2()      
    else:
        start2()

# def listen_ingredients():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Say something!")
#         audio = r.listen(source)
#     try:
#         recog_word = r.recognize_google(audio)
#         if not inventory: #player inventory is empty, empty 'inventory' is false
#             if recog_word in valid_ingredients:
#                 inventory = recog_word
#                 print(inventory + " is added to your inventory")
#             else:
#                 print("Invalid item or action")
#         else: #player inventory is full
#             if recog_word in valid_actions: #so far only action is to put down which results in empty inv
#                 inventory = ''
#             else:
#                 print("Inventory is full") #nothing else but 'put down' works for now if inv is full
#     except sr.UnknownValueError:
#         print("Google Speech Recognition could not understand audio")
#     except sr.RequestError as e:
#         print("Could not request results from Google Speech Recognition service; {0}".format(e))


main()