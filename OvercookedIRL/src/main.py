import pygame
from sprites import *
from config import *
from ingredients import * 
from singleplayer_player import *
from singleplayer_counters import *
from singleplayer_timer import *
from singleplayer_score import *
from recipe import *
import sys
import new_button
import os
from pygame.locals import *
from pygame import mixer
# import math
# import speech_recognition as sr 
import paho.mqtt.client as mqtt

pygame.init()

mixer.init()
mixer.music.load("Sounds/jazz_background.wav")
mixer.music.set_volume(0.1)
mixer.music.play(-1)

font = pygame.font.SysFont("comicsansms", 40)
r = pygame.rect.Rect((0, WIN_HEIGHT-30, 70, 30))
black = (0, 0, 0)

def on_connect(client,userdata,flags,rc):
    client.subscribe("overcooked_game", qos=1)
    print("connection returned result:" + str(rc))

def on_disconnect(client, userdata, rc):
    if rc != 0: 
        print('Undexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, message):
    print('Received message: "' + str(message.payload) + " on topic " + message.topic + '" with QoS ' + str(message.qos)) 
    # self.speech_log.write(str(message.payload) + "/n")
    print(".:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:.")
    line = str(message.payload)[2:][:-1]
    print(line)
    # userdata.speech_log.write(line + "\n")
    print("i am in singleplayer main")

    print(userdata.player.action)
    print(userdata.player.location)
    
    # if(str(message.payload) == "b\'" + "tomato" + "\'"):
    #     # client.publish("tomato")
    #     # client.publish('overcooked_mic', 'tomato', qos=1)
    #     print("recieved tomato")

    # if(userdata.player.action is not None):
    #     userdata.player.message = line
    if (line == "Mic Start"):
        if(userdata.player.location is not None):
            if(userdata.player.action is None):
                userdata.player.action = "Speak"
                userdata.player.before = True
                userdata.client.publish('overcooked_mic', "Start", qos=1)
        else:
            userdata.player.stop_everything()
    elif (line == "Pick Up" or line == "Put Down"):
        if(userdata.player.action is not None):
            userdata.player.message = line
        else:
            userdata.player.stop_everything()
    elif(line == "Gesture"):
        if(userdata.player.location == "Chopping Station" or userdata.player.location == "Cooking Station"):
            if(userdata.player.action is None):
                userdata.player.action = "Gesture"
                userdata.player.message = "Gesture"
                userdata.player.before = True
    elif(line == "Chop" or line == "Stir" or line == "Idle"):
        if(userdata.player.location == "Chopping Station" or userdata.player.location == "Cooking Station"):
            if(userdata.player.action == "Gesture"):
                userdata.player.message = line
                if(userdata.player.during == True):
                    userdata.client.publish('overcooked_mic', "During!", qos=1)
    elif(line == "Mic Stop"):
        userdata.player.stop_everything()
    elif(line == "Tomato" or line == "Bun" or line == "Lettuce" or line == "Meat"):
        userdata.player.message = line
    elif(line == "Plate"):
        # userdata.player.action == "Pick Up"
        userdata.player.message = line
    elif(line == "Stop Gesture"):
        userdata.player.stop_everything()
    else:
        userdata.player.stop_everything()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen_x, self.screen_y = self.screen.get_size()
        print(self.screen_x)
        print(self.screen_y)

        self.character_idle_spritesheet = Spritesheet('../img/chef1/chef1_idle_32.png')
        self.character_run_spritesheet = Spritesheet('../img/chef1/chef1_run_32.png')
        self.kitchen_spritesheet = Spritesheet('../img/12_Kitchen_32x32.png')
        self.kitchen_shadowless_spritesheet = Spritesheet('../img/12_Kitchen_Shadowless_32x32.png')
        # self.cook_cloud_spritesheet = Spritesheet('../img/cloud_32.png')
        self.character_chop_spritesheet = Spritesheet('../img/chef1/chop_idle.png')
        self.character_stir_spritesheet = Spritesheet('../img/chef1/chef_stir.png')
        self.character_pickup_spritesheet = Spritesheet('../img/chef1/chef1_pickup.png')
        self.character_putdown_spritesheet = Spritesheet('../img/chef1/chef1_place.png')
        self.cursor_spritesheet = Spritesheet('../img/cursor.png')
        self.knife_animation = Spritesheet('../img/chop_knife.png')
        self.plates_stack = Spritesheet('../img/individual_tiles/dish_pile.png')
        self.inventory_spritesheet = Spritesheet('../img/inventory_tile.png')
        self.bun_spritesheet = Spritesheet('../img/recipes/bun_spritesheet.png')
        self.full_bun_spritesheet = Spritesheet('../img/recipes/bun_full.png')
        self.meat_spritesheet = Spritesheet('../img/recipes/meat_spritesheet.png')
        self.tomato_spritesheet = Spritesheet('../img/recipes/tomato_spritesheet.png')
        self.lettuce_spritesheet = Spritesheet('../img/recipes/lettuce_spritesheet.png')
        self.plate_spritesheet = Spritesheet('../img/recipes/plate_spritesheet.png')
        self.progress_spritesheet = Spritesheet('../img/progress_bar.png')
        self.knife_icon = Spritesheet('../img/knife_icon.png')
        self.cook_icon = Spritesheet('../img/cook_icon.png')
        self.speaking_animation = Spritesheet('../img/speaking_animation.png')
        self.stirring_animation = Spritesheet('../img/stirring_animation.png')
        self.chopping_animation = Spritesheet('../img/chopping_animation.png')
        self.cook_state_spritesheet = Spritesheet('../img/cook_state.png')
        self.cut_state_spritesheet = Spritesheet('../img/cut_state.png')
        self.cut_state0_spritesheet = Spritesheet('../img/cut_state0.png', False)
        self.cut_state1_spritesheet = Spritesheet('../img/cut_state1.png', False)
        self.cut_state2_spritesheet = Spritesheet('../img/cut_state2.png', False)
        self.cut_state3_spritesheet = Spritesheet('../img/cut_state3.png', False)
        self.cook_state0_spritesheet = Spritesheet('../img/cook_state0.png', False)
        self.cook_state1_spritesheet = Spritesheet('../img/cook_state1.png', False)
        self.cook_state2_spritesheet = Spritesheet('../img/cook_state2.png', False)
        self.cook_state3_spritesheet = Spritesheet('../img/cook_state3.png', False)
        self.current_cut_sheet = self.cut_state_spritesheet
        self.current_cook_sheet = self.cook_state_spritesheet
        self.cook_state_list = [self.cook_state0_spritesheet, self.cook_state1_spritesheet, self.cook_state2_spritesheet, self.cook_state3_spritesheet]
        self.cut_state_list = [self.cut_state0_spritesheet, self.cut_state1_spritesheet, self.cut_state2_spritesheet, self.cut_state3_spritesheet]

        self.fridge_open_animation = Spritesheet('../img/object_animations/fridge_open_spritesheet.png')
        self.fridge_close_animation = Spritesheet('../img/object_animations/fridge_close_spritesheet.png')
        self.recipe_card = Spritesheet('../img/recipe_card.png')

        SING_WIN_WIDTH = self.screen_x
        SING_WIN_HEIGHT = self.screen_y
        title_screen = pygame.image.load("../img/title_background.png")
        self.title_screen = pygame.transform.scale(title_screen, (SING_WIN_WIDTH, SING_WIN_HEIGHT))
        start_button_img = pygame.image.load("Game_Texts/Start_the_game.png")
        start_button_alt_img = pygame.image.load('Game_Texts/Start_the_game_alt.png')
        tutorial_button_img = pygame.image.load('Game_Texts/tutorial.png')
        tutorial_button_alt_img = pygame.image.load('Game_Texts/tutorial_alt.png')
        title_img = pygame.image.load('Game_Texts/new_title.png')
        exit_img = pygame.image.load('Game_Texts/exit.png')
        exit_alt_img = pygame.image.load('Game_Texts/exit_alt.png')
        self.exit_button = new_button.Button(exit_img, exit_alt_img, 0.35, SING_WIN_WIDTH, SING_WIN_HEIGHT, False, True, SING_WIN_WIDTH - 80, SING_WIN_HEIGHT-80)
        self.new_start_button = new_button.Button(start_button_img, start_button_alt_img, 0.45, SING_WIN_WIDTH, SING_WIN_HEIGHT, True, True, 0, -90)
        self.new_tutorial_button = new_button.Button(tutorial_button_img, tutorial_button_alt_img, 0.45, SING_WIN_WIDTH, SING_WIN_HEIGHT, True, True, 0, 10)
        self.new_title = new_button.Button(title_img, None, 0.6, SING_WIN_WIDTH, SING_WIN_HEIGHT, True, False, 0, -330)
        enter_name_img = pygame.image.load('Game_Texts/enter_name.png')
        self.enter_name = new_button.Button(enter_name_img, None, 0.6, SING_WIN_WIDTH, SING_WIN_HEIGHT, True, False, 0, -330)
        back_img = pygame.image.load('Game_Texts/back.png')
        back_alt_img = pygame.image.load('Game_Texts/back_alt.png')
        self.back_button = new_button.Button(back_img, back_alt_img, 0.35, SING_WIN_WIDTH, SING_WIN_HEIGHT, False, True, SING_WIN_WIDTH - 80, SING_WIN_HEIGHT-80)
        welcome_2_tut_img = pygame.image.load('Game_Texts/welcome_2_tut.png')
        self.welcome_2_tut_button = new_button.Button(welcome_2_tut_img, None, 0.55, SING_WIN_WIDTH, SING_WIN_HEIGHT, True, False, 0, -300)

        gesture_img = pygame.image.load('Game_Texts/gesture.png')
        gesture_alt_img = pygame.image.load('Game_Texts/gesture_alt.png')
        self.gesture_button = new_button.Button(gesture_img, gesture_alt_img, 0.45, SING_WIN_WIDTH, SING_WIN_HEIGHT, True, True, 0, -200)
        controller_img = pygame.image.load('Game_Texts/controller.png')
        controller_alt_img = pygame.image.load('Game_Texts/controller_alt.png')
        self.controller_button = new_button.Button(controller_img, controller_alt_img, 0.45, SING_WIN_WIDTH, SING_WIN_HEIGHT, True, True, 0, 0)
        speech_img = pygame.image.load('Game_Texts/speech.png')
        speech_alt_img = pygame.image.load('Game_Texts/speech_alt.png')
        self.speech_button = new_button.Button(speech_img, speech_alt_img, 0.45, SING_WIN_WIDTH, SING_WIN_HEIGHT, True, True, 0, -100)
        movement_img = pygame.image.load('Game_Texts/movement.png')
        movement_alt_img = pygame.image.load('Game_Texts/movement_alt.png')
        self.movement_button = new_button.Button(movement_img, movement_alt_img, 0.45, SING_WIN_WIDTH, SING_WIN_HEIGHT, True, True, 0, 100)
        how2play_img = pygame.image.load('Game_Texts/how2play.png')
        how2play_alt_img = pygame.image.load('Game_Texts/how2play_alt.png')
        #self.how2play_button = new_button.Button(how2play_img, how2play_alt_img, 0.35, SING_WIN_WIDTH, SING_WIN_HEIGHT, False, True, 15, 200)
        self.how2play_button = new_button.Button(how2play_img, how2play_alt_img, 0.45, SING_WIN_WIDTH, SING_WIN_HEIGHT, True, True, 0, 200)
        wait_4_all_img = pygame.image.load('Game_Texts/wait_4_all.png')
        self.wait_4_all_button = new_button.Button(wait_4_all_img, None, 0.55, SING_WIN_WIDTH, SING_WIN_HEIGHT, True, False, 0, -330)
        ready_img = pygame.image.load('Game_Texts/ready.png')
        ready_alt_img = pygame.image.load('Game_Texts/ready_alt.png')
        self.ready_button = new_button.Button(ready_img, ready_alt_img, 0.45, SING_WIN_WIDTH, SING_WIN_HEIGHT, True, True, 0, -90)
        ready_up_img = pygame.image.load('Game_Texts/ready_up.png')
        self.ready_up_button= new_button.Button(ready_up_img, None, 0.55, SING_WIN_WIDTH, SING_WIN_HEIGHT, True, False, 0, -330)
        select_mode_img = pygame.image.load('Game_Texts/select_mode.png')
        self.select_mode_button = new_button.Button(select_mode_img, None, 0.55, SING_WIN_WIDTH, SING_WIN_HEIGHT, True, False, 0, -330)
        singleplayer_img = pygame.image.load('Game_Texts/singleplayer.png')
        singleplayer_alt_img = pygame.image.load('Game_Texts/singleplayer_alt.png')
        multiplayer_img = pygame.image.load('Game_Texts/multiplayer.png')
        multiplayer_alt_img = pygame.image.load('Game_Texts/multiplayer_alt.png')
        self.singleplayer_button = new_button.Button(singleplayer_img, singleplayer_alt_img, 0.45, SING_WIN_WIDTH, SING_WIN_HEIGHT, True, True, 0, -90)
        self.multiplayer_button = new_button.Button(multiplayer_img, multiplayer_alt_img, 0.45, SING_WIN_WIDTH, SING_WIN_HEIGHT, True, True, 0, 10)
        no_srv_fnd_img = pygame.image.load('Game_Texts/no_srv_fnd.png')
        self.no_srv_fnd_button = new_button.Button(no_srv_fnd_img, None, 0.6, SING_WIN_WIDTH, SING_WIN_HEIGHT, True, False, 0, -330)
        game_over_img = pygame.image.load('Game_Texts/game_over.png')
        self.game_over_button = new_button.Button(game_over_img, None, 0.6, SING_WIN_WIDTH, SING_WIN_HEIGHT, True, False, 0, -330)
        score_img = pygame.image.load('Game_Texts/score.png')
        self.score_button = new_button.Button(score_img, None, 0.45, SING_WIN_WIDTH, SING_WIN_HEIGHT, True, True, -30, -90)
        settings_img = pygame.image.load('Game_Texts/settings.png')
        self.settings_button = new_button.Button(settings_img, None, 0.6, SING_WIN_WIDTH, SING_WIN_HEIGHT, True, False, 0, -330)
        fivemin_img = pygame.image.load('Game_Texts/5min.png')
        fivemin_alt_img = pygame.image.load('Game_Texts/5min_alt.png')
        self.fivemin_button = new_button.Button(fivemin_img, fivemin_alt_img, 0.35, SING_WIN_WIDTH, SING_WIN_HEIGHT, False, True, 15, 240)
        tenmin_img = pygame.image.load('Game_Texts/10min.png')
        tenmin_alt_img = pygame.image.load('Game_Texts/10min_alt.png')
        self.tenmin_button = new_button.Button(tenmin_img, tenmin_alt_img, 0.35, SING_WIN_WIDTH, SING_WIN_HEIGHT, False, True, 15, 320)
        fifteenmin_img = pygame.image.load('Game_Texts/15min.png')
        fifteenmin_alt_img = pygame.image.load('Game_Texts/15min_alt.png')
        self.fifteenmin_button = new_button.Button(fifteenmin_img, fifteenmin_alt_img, 0.35, SING_WIN_WIDTH, SING_WIN_HEIGHT, False, True, 15, 400)
        resign_img = pygame.image.load('Game_Texts/resign.png')
        resign_alt_img = pygame.image.load('Game_Texts/resign_alt.png')
        self.resign_button = new_button.Button(resign_img, resign_alt_img, 0.45, SING_WIN_WIDTH, SING_WIN_HEIGHT, False, True, SING_WIN_WIDTH - 330, SING_WIN_HEIGHT-110)
        pickup_img = pygame.image.load('Game_Texts/pickup.png')
        self.pickup_button = new_button.Button(pickup_img, None, 0.45, SING_WIN_WIDTH, SING_WIN_HEIGHT, False, True, SING_WIN_WIDTH - 420, SING_WIN_HEIGHT-385)
        down_img = pygame.image.load('Game_Texts/down.png')
        self.down_button = new_button.Button(down_img, None, 0.45, SING_WIN_WIDTH, SING_WIN_HEIGHT, False, True, SING_WIN_WIDTH - 420, SING_WIN_HEIGHT-320)
        meat_img = pygame.image.load('Game_Texts/meat.png')
        self.meat_button = new_button.Button(meat_img, None, 0.45, SING_WIN_WIDTH, SING_WIN_HEIGHT, False, True, SING_WIN_WIDTH - 420, SING_WIN_HEIGHT-370)
        bread_img = pygame.image.load('Game_Texts/bread.png')
        self.bread_button = new_button.Button(bread_img, None, 0.45, SING_WIN_WIDTH, SING_WIN_HEIGHT, False, True, SING_WIN_WIDTH - 420, SING_WIN_HEIGHT-370)
        lettuce_img = pygame.image.load('Game_Texts/lettuce.png')
        self.lettuce_button = new_button.Button(lettuce_img, None, 0.45, SING_WIN_WIDTH, SING_WIN_HEIGHT, False, True, SING_WIN_WIDTH - 420, SING_WIN_HEIGHT-370)
        tomato_img = pygame.image.load('Game_Texts/tomato.png')
        self.tomato_button = new_button.Button(tomato_img, None, 0.45, SING_WIN_WIDTH, SING_WIN_HEIGHT, False, True, SING_WIN_WIDTH - 420, SING_WIN_HEIGHT-370)
        plate_img = pygame.image.load('Game_Texts/plate.png')
        self.plate_button = new_button.Button(plate_img, None, 0.45, SING_WIN_WIDTH, SING_WIN_HEIGHT, False, True, SING_WIN_WIDTH - 420, SING_WIN_HEIGHT-370)
        voice_commands_img = pygame.image.load('Game_Texts/voice_commands.png')
        self.voice_commands_button = new_button.Button(voice_commands_img, None, 0.45, SING_WIN_WIDTH, SING_WIN_HEIGHT, False, True, SING_WIN_WIDTH - 420, SING_WIN_HEIGHT-440)

    def createTilemap(self,tilemap,layer):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                # if column == "P":
                #     Player(self, j, i)
                if column == '0':
                    BackgroundObject(self, self.plates_stack, 0, 0, j, i, layer, (self.all_sprites))
                elif column == '1':
                    BackgroundObject(self, self.tomato_spritesheet, 0, 0, j, i, layer, (self.all_sprites))
                elif column == '2':
                    BackgroundObject(self, self.lettuce_spritesheet, 0, 0, j, i, layer, (self.all_sprites))
                elif column == '3':
                    BackgroundObject(self, self.meat_spritesheet, 0, 0, j, i, layer, (self.all_sprites))
                elif column == '4':
                    BackgroundObject(self, self.full_bun_spritesheet, 0, 0, j, i, layer, (self.all_sprites))
                elif column == '!':
                    IngredientsCounter("Tomato",self, self.kitchen_spritesheet,white_counter["!"][0],white_counter["!"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.bottom_perspective_counters,self.ingredients_stands))
                elif column == '^':
                    IngredientsCounter("Lettuce",self, self.kitchen_spritesheet,white_counter["!"][0],white_counter["!"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.bottom_perspective_counters,self.ingredients_stands))
                elif column == '(':
                    IngredientsCounter("Meat",self, self.kitchen_spritesheet,white_counter["!"][0],white_counter["!"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.bottom_perspective_counters,self.ingredients_stands))
                elif column == ')':
                    IngredientsCounter("Bun",self, self.kitchen_spritesheet,white_counter["!"][0],white_counter["!"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.bottom_perspective_counters,self.ingredients_stands))
                elif column == 'E':
                    Counter(self, self.kitchen_spritesheet,white_counter["E"][0],white_counter["E"][1],j,i,layer,(self.all_sprites,self.counters,self.bottom_perspective_counters))
                elif column == '$':
                    ChopCounter(self, self.kitchen_spritesheet,white_counter["B"][0],white_counter["B"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.chopping_stations))
                elif column == '*':
                    IngredientsCounter("Plate",self, self.kitchen_spritesheet,
                    white_counter["H"][0],white_counter["H"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.plate_stations))
                elif column == '%':
                    CookCounter('pan',self, self.kitchen_spritesheet,white_counter["%"][0],white_counter["%"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.bottom_perspective_counters,self.cooking_stations))
                elif column == 'B':
                    Counter(self, self.kitchen_spritesheet,white_counter["B"][0],white_counter["B"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.bottom_perspective_counters))
                elif column == 'J':
                    Counter(self, self.kitchen_spritesheet,white_counter["J"][0],white_counter["J"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.bottom_perspective_counters))
                elif column == 'G':
                    Counter(self, self.kitchen_spritesheet,white_counter["G"][0],white_counter["G"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.left_counters))
                elif column == 'H':
                    Counter(self, self.kitchen_spritesheet,white_counter["H"][0],white_counter["H"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.right_counters))
                elif column == 'V':
                    BackgroundObject(self,self.inventory_spritesheet,0,0,j,i,layer,(self.all_sprites)) 
                elif column == '8':
                    BackgroundObject(self,self.current_cut_sheet,0,0,j,i,layer,(self.all_sprites), 8, self.player, self.cook_state_list, self.cut_state_list)
                elif column == '9':
                    BackgroundObject(self,self.cook_state_spritesheet,0,0,j,i,layer,(self.all_sprites), 9, self.player, self.cook_state_list, self.cut_state_list)       
                elif column == 'S':
                    Counter(self, self.kitchen_spritesheet,white_counter["S"][0],white_counter["S"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.bottom_perspective_counters))
                elif column == 'M':
                    SubmitStation(self, self.kitchen_spritesheet,white_counter["G"][0],white_counter["G"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.left_counters,self.submit_stations))
                elif column == '&':
                    BackgroundObject(self, self.kitchen_spritesheet,9*TILE_SIZE,1408, j, i, COUNTER_LAYER+1, (self.all_sprites))
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
                    # self, self.kitchen_spritesheet,white_counter["G"][0],white_counter["G"][1],j,i,(self.all_sprites,self.counters,self.block_counters,self.ingredients_stands)
                    Counter(self, self.kitchen_spritesheet,white_counter[column][0],white_counter[column][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters))
                    # self.image = self.game.kitchen_spritesheet.get_sprite(white_counter[type][0],white_counter[type][1],0,0,self.width,self.height)
        # print('created tilemap')

    def new(self, timer):
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
        self.player = Player(self,10,11)
        self.timer = Timer(self,17,0,timer,FPS)
        self.score = Score(self,0,0)
        self.recipes = [RecipeCard(self,3*TILE_SIZE,0)]
        # game, x, y

        self.animations = pygame.sprite.LayeredUpdates()


        self.createTilemap(counter_tilemap_back,COUNTER_BACK_LAYER)
        self.createTilemap(counter_tilemap_back_items,COUNTER_BACK_ITEMS_LAYER)
        self.createTilemap(counter_tilemap,COUNTER_LAYER)
        self.createTilemap(counter_tilemap_ingredient, COUNTER_LAYER)
        self.createTilemap(counter_tilemap_2,COUNTER_FRONT_LAYER)
        self.createTilemap(counter_front_items_tilemap,COUNTER_FRONT_LAYER+1)
        # self.createTilemap(foreground_tilemap,FOREGROUND_LAYER)
        # initialize_camera()

        ProgressBar(self, self.progress_spritesheet, 7*TILE_SIZE, 4*TILE_SIZE, COUNTER_LAYER, (self.all_sprites), 3*TILE_SIZE, TILE_SIZE, self.player)
        # self.mouse.setupMouse()

        # self.setup_audiofile()
        self.setup_mqtt()

    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and self.clicked is True:
                pos = pygame.mouse.get_pos()
                self.player.dest_x = ((round(pos[0]/32)-1) * 32)
                self.player.dest_y = ((round(pos[1]/32)-1) * 32)
                if(self.player.action is not None):
                    self.client.publish('overcooked_mic', "Stop", qos=1)
                    self.client.publish('overcooked_imu', "Mic Stop", qos=1)
                    self.player.stop_everything()

                print('CLICK')
                # print(int(pos[0]/32) * 32, int(pos[1]/32) * 32)
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        # game loop updates

        # run the update method of every sprite in the all_sprites group

        self.all_sprites.update() 

    def draw(self):
        # game loop draw
        self.screen.fill((222,184,135))

        # draws the image and rect of all sprites in the all_sprites group onto the screen
        self.all_sprites.draw(self.screen)
        if self.resign_button.draw(self.screen) and self.clicked is True:
            self.playing = False
            self.clicked = False
        self.voice_commands_button.draw(self.screen)
        if self.player.location is not None:
            if self.player.location == "Plate Station":
                self.plate_button.draw(self.screen)
            elif self.player.location == "Ingredients Stand":
                if self.player.location_sprite.ingredient == 'Meat':
                    self.meat_button.draw(self.screen)
                elif self.player.location_sprite.ingredient == 'Lettuce':
                    self.lettuce_button.draw(self.screen)
                elif self.player.location_sprite.ingredient == 'Bun':
                    self.bread_button.draw(self.screen)
                elif self.player.location_sprite.ingredient == 'Tomato':
                    self.tomato_button.draw(self.screen)
            elif self.player.location in ["Chopping Station", "Cooking Station", "Top Counter", "Left Counter", "Right Counter"]:
                self.pickup_button.draw(self.screen)
                self.down_button.draw(self.screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        self.clock.tick(FPS)

    def setup_audiofile(self):
        i = 0
        while os.path.exists("speech%s.txt" % i):
            i += 1
        self.speech_log = open("speech" + str(i) + ".txt", "a")
        # self.r = sr.Recognizer()

    def setup_mqtt(self):
        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        self.client.on_message = on_message
        self.client.user_data_set(self)

        self.client.connect_async("test.mosquitto.org")
        self.client.connect("test.mosquitto.org", 1883, 60)
        self.client.loop_start()
        # self.client.publish('overcooked_mic', "t", qos=1)

    def main(self):
        # font = pygame.font.Font(None,40)
        # gray = pygame.Color('gray19')
        # blue = pygame.Color('dodgerblue')
        # timer = 120
        # clock = pygame.time.Clock()
        # dt = 0
        
        # game loop
        while self.playing:
        # if(self.playing):
            # self.mouse.mouseMovement()
            self.events()
            self.update()
            self.draw()
            # round_timer = int(math.ceil(timer))
            # min = str(int(round_timer/60))
            # sec = str(int(round_timer%60))
            # if(int(sec)<10):
            #     sec = '0'+str(sec)
            
            # txt = font.render(min+':'+sec, True, blue)
            # self.screen.blit(txt, (70, 70))
            # pygame.display.flip()
            # dt = clock.tick(30) / 1000  # / 1000 to convert to seconds.

            # if int(sec) == 0 and int(min) == 0:
            #     done = True
            # else:
            #     timer -= dt
            if self.timer.min == '0' and self.timer.sec == '00':
                break
            self.clicked=True
        self.player.game_on = False
        self.client.publish('overcooked_mic', "stop", qos=1)
        self.client.loop_stop()
        self.client.disconnect()
        # self.speech_log.close()
        self.running = False
        self.clicked = False
        self.player.stop_sounds()
        return self.game_over()

    def intro_screen(self):
            self.clicked = False
            while True:
                self.screen.blit(self.title_screen, (0,0))
                self.new_title.draw(self.screen)
                if self.new_start_button.draw(self.screen) and self.clicked is True:
                    return self.gamemode_selection_screen()
                if self.new_tutorial_button.draw(self.screen) and self.clicked is True:
                    return self.tutorial_screen_intro()
                if self.exit_button.draw(self.screen) and self.clicked is True:
                    print("exit")
                    pygame.quit()
                    sys.exit()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                self.clicked=True
                pygame.display.update()
                self.clock.tick(FPS)

    def gamemode_selection_screen(self):
            self.clicked = False
            while True:
                self.screen.blit(self.title_screen, (0,0))
                self.select_mode_button.draw(self.screen)
                if self.singleplayer_button.draw(self.screen) and self.clicked is True:
                    self.clicked = False
                    return self.settings_screen()
                if self.back_button.draw(self.screen) and self.clicked is True:
                    return self.intro_screen()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                self.clicked=True
                pygame.display.update()
                self.clock.tick(FPS)

    def settings_screen(self):
        self.clicked = False
        time_selected = False
        timer = 0
        while True:
            if self.clicked:
                
                self.screen.blit(self.title_screen, (0,0))
                self.settings_button.draw(self.screen)
                if time_selected is False:
                    if self.fivemin_button.draw(self.screen) and self.clicked is True:
                        timer = 300
                        time_selected = True
                    if self.tenmin_button.draw(self.screen) and self.clicked is True:
                        timer = 600
                        time_selected = True
                    if self.fifteenmin_button.draw(self.screen) and self.clicked is True:
                        timer = 900
                        time_selected = True
                else:
                    while True:
                        self.screen.blit(self.title_screen, (0,0))
                        self.ready_up_button.draw(self.screen)
                        if self.ready_button.draw(self.screen) and self.clicked is True:
                            self.new(timer)
                            self.running = True
                            self.clicked = False
                            while self.running:
                                self.main()
                            return None
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                        pygame.display.update()
                        self.clock.tick(FPS)           
                if self.back_button.draw(self.screen) and self.clicked is True:
                    return self.gamemode_selection_screen()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            self.clicked = True
            pygame.display.update()
            self.clock.tick(FPS)

    def tutorial_screen_intro(self):
        self.clicked = False
        while True:
            if self.clicked:
                self.screen.blit(self.title_screen, (0,0))
                self.welcome_2_tut_button.draw(self.screen)
                if self.gesture_button.draw(self.screen) and self.clicked is True:
                    print("gesture")
                if self.controller_button.draw(self.screen) and self.clicked is True:
                    print("controller")
                if self.speech_button.draw(self.screen) and self.clicked is True:
                    print("speech")
                if self.movement_button.draw(self.screen) and self.clicked is True:
                    print("movement")
                if self.back_button.draw(self.screen) and self.clicked is True:
                    return self.intro_screen()
                if self.how2play_button.draw(self.screen):
                    print("how2play")
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            self.clicked = True
            pygame.display.update()
            self.clock.tick(FPS)

    def game_over(self):
        self.player.game_on = False
        myFont = pygame.font.SysFont("Comic Sans MS", 40)
        scoreDisplay = myFont.render(str(self.score.score), 1, (0,0,0))
        while True:
            if self.clicked:
                self.screen.blit(self.title_screen, (0,0))
                self.game_over_button.draw(self.screen)
                self.score_button.draw(self.screen)
                self.screen.blit(scoreDisplay, (self.screen_x/2 + 35, self.screen_y/2 - 70))
                if self.back_button.draw(self.screen) and self.clicked is True:
                    return self.intro_screen()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            self.clicked = True
            pygame.display.update()
            self.clock.tick(FPS)


g = Game()
g.intro_screen()


pygame.quit()
sys.exit()