# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 15:27:07 2022
@author: Kellen Cheng
"""

from tkinter import FALSE
from counter_items_generator import CounterItemsGenerator
import pygame
from sprites import *
from multiplayer_config_48 import *
from ingredients import * 
from multiplayer_player import *
from multiplayer_counters import *
from multiplayer_timer import *
from score import *
from recipe import *
import sys
import os
from input_box import *
import new_button
from pygame import mixer
import paho.mqtt.client as mqtt

pygame.init()

mixer.init()
mixer.music.load("Sounds/jazz_background.wav")
mixer.music.set_volume(0.3)
mixer.music.play(-1)

font = pygame.font.SysFont("comicsansms", 40)
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
    #print('Received message: "' + str(message.payload) + " on topic " + message.topic + '" with QoS ' + str(message.qos)) 
    # self.speech_log.write(str(message.payload) + "/n")
    #print(".:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:.")
    line = str(message.payload)[2:][:-1]
    #print(line)
    # userdata.speech_log.write(line + "\n")

    # if(userdata.player.action is not None):
    #     userdata.player.message = line
    if (line == "Mic Start"):
        if(userdata.player.location is not None):
            if(userdata.player.action is None):
                userdata.player.action = "Speak"
                userdata.player.before = True
                userdata.client.publish('overcooked_mic'+str(userdata.player.client_ID), "Start", qos=1)
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
    elif(line == "Chop" or line == "Stir"):
        if(userdata.player.location == "Chopping Station" or userdata.player.location == "Cooking Station"):
            if(userdata.player.action == "Gesture"):
                userdata.player.message = line
                if(userdata.player.during == True):
                    userdata.client.publish('overcooked_mic'+str(userdata.player.client_ID), "During!", qos=1)
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
    def __init__(self, client_socket, header):
        pygame.init()
        # self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.screen = pygame.display.set_mode((1200, 800))
        self.screen_x, self.screen_y = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.running = True
        self.socket_client = client_socket
        self.clicked = False
        self.header = header
        self.in_tutorial=False
        
        self.character_idle_spritesheet = Spritesheet('../img/chef1/chef1_idle_48.png')
        self.character_run_spritesheet = Spritesheet('../img/chef1/chef1_run_48.png')
        self.kitchen_spritesheet = Spritesheet('../img/12_Kitchen_48x48.png')
        self.kitchen_shadowless_spritesheet = Spritesheet('../img/12_Kitchen_Shadowless_48x48.png')
        self.character_chop_spritesheet = Spritesheet('../img/chef1/chop_idle_48.png')
        self.character_stir_spritesheet = Spritesheet('../img/chef1/chef_stir_48.png')
        self.character_pickup_spritesheet = Spritesheet('../img/chef1/chef1_pickup_48.png')
        self.character_putdown_spritesheet = Spritesheet('../img/chef1/chef1_place_48.png')
        self.cursor_spritesheet = Spritesheet('../img/cursor_48.png')
        self.knife_animation = Spritesheet('../img/chop_knife_48.png')
        self.plates_stack = Spritesheet('../img/individual_tiles/dish_pile_48.png')
        self.inventory_spritesheet = Spritesheet('../img/inventory_tile_48.png')
        self.bun_spritesheet = Spritesheet('../img/recipes/bun_spritesheet_48.png')
        self.meat_spritesheet = Spritesheet('../img/recipes/meat_spritesheet_48.png')
        self.tomato_spritesheet = Spritesheet('../img/recipes/tomato_spritesheet_48.png')
        self.lettuce_spritesheet = Spritesheet('../img/recipes/lettuce_spritesheet_48.png')
        self.bun_2_spritesheet = Spritesheet('../img/recipes/bun_2_spritesheet_48.png')
        self.meat_2_spritesheet = Spritesheet('../img/recipes/meat_2_spritesheet_48.png')
        self.bun_full_1_spritesheet = Spritesheet('../img/recipes/bun_full_48.png')
        self.bun_full_2_spritesheet = Spritesheet('../img/recipes/bun_full_2_48.png')
        self.plate_spritesheet = Spritesheet('../img/recipes/plate_spritesheet_48.png')
        self.progress_spritesheet = Spritesheet('../img/progress_bar_48.png')
        self.knife_icon = Spritesheet('../img/knife_icon_48.png')
        self.cook_icon = Spritesheet('../img/cook_icon_48.png')
        self.speaking_animation = Spritesheet('../img/speaking_animation_48.png')
        self.cook_state_spritesheet = Spritesheet('../img/cook_state.png')
        self.cut_state_spritesheet = Spritesheet('../img/cut_state.png')
        self.share_left_spritesheet = Spritesheet('../img/share_left_48.png')
        self.share_right_spritesheet = Spritesheet('../img/share_right_48.png')
        self.cut_state0_spritesheet = Spritesheet('../img/cut_state0.png')
        self.cut_state1_spritesheet = Spritesheet('../img/cut_state1.png')
        self.cut_state2_spritesheet = Spritesheet('../img/cut_state2.png')
        self.cut_state3_spritesheet = Spritesheet('../img/cut_state3.png')
        self.cook_state0_spritesheet = Spritesheet('../img/cook_state0.png')
        self.cook_state1_spritesheet = Spritesheet('../img/cook_state1.png')
        self.cook_state2_spritesheet = Spritesheet('../img/cook_state2.png')
        self.cook_state3_spritesheet = Spritesheet('../img/cook_state3.png')
        self.stirring_animation = Spritesheet('../img/stirring_animation.png')
        self.chopping_animation = Spritesheet('../img/chopping_animation.png')
        self.current_cut_sheet = self.cut_state_spritesheet
        self.current_cook_sheet = self.cook_state_spritesheet
        self.cook_state_list = [self.cook_state0_spritesheet, self.cook_state1_spritesheet, self.cook_state2_spritesheet, self.cook_state3_spritesheet]
        self.cut_state_list = [self.cut_state0_spritesheet, self.cut_state1_spritesheet, self.cut_state2_spritesheet, self.cut_state3_spritesheet]

        self.fridge_open_animation = Spritesheet('../img/object_animations/fridge_open_spritesheet_48.png')
        self.fridge_close_animation = Spritesheet('../img/object_animations/fridge_close_spritesheet_48.png')
        self.recipe_card = Spritesheet('../img/recipe_card_48.png')
        
        self.all_share_stations = []
        self.all_counters = []

        self.r = pygame.rect.Rect((0, self.screen_y-30, 70, 30))

        title_screen = pygame.image.load("../img/title_background.png")
        self.title_screen = pygame.transform.scale(title_screen, (self.screen_x, self.screen_y))
        start_button_img = pygame.image.load("Game_Texts/Start_the_game.png")
        start_button_alt_img = pygame.image.load('Game_Texts/Start_the_game_alt.png')
        tutorial_button_img = pygame.image.load('Game_Texts/tutorial.png')
        tutorial_button_alt_img = pygame.image.load('Game_Texts/tutorial_alt.png')
        title_img = pygame.image.load('Game_Texts/new_title.png')
        exit_img = pygame.image.load('Game_Texts/exit.png')
        exit_alt_img = pygame.image.load('Game_Texts/exit_alt.png')
        self.exit_button = new_button.Button(exit_img, exit_alt_img, 0.35, self.screen_x, self.screen_y, False, True, self.screen_x - 80, self.screen_y-80)
        self.new_start_button = new_button.Button(start_button_img, start_button_alt_img, 0.45, self.screen_x, self.screen_y, True, True, 0, -90)
        self.new_tutorial_button = new_button.Button(tutorial_button_img, tutorial_button_alt_img, 0.45, self.screen_x, self.screen_y, True, True, 0, 10)
        self.new_title = new_button.Button(title_img, None, 0.6, self.screen_x, self.screen_y, True, False, 0, -330)
        enter_name_img = pygame.image.load('Game_Texts/enter_name.png')
        self.enter_name = new_button.Button(enter_name_img, None, 0.6, self.screen_x, self.screen_y, True, False, 0, -330)
        back_img = pygame.image.load('Game_Texts/back.png')
        back_alt_img = pygame.image.load('Game_Texts/back_alt.png')
        self.back_button = new_button.Button(back_img, back_alt_img, 0.35, self.screen_x, self.screen_y, False, True, self.screen_x - 80, self.screen_y-80)
        self.tutorial_back_button = new_button.Button(back_img, back_alt_img, 0.35, self.screen_x, self.screen_y, False, True, self.screen_x - 180, self.screen_y-80)
        welcome_2_tut_img = pygame.image.load('Game_Texts/welcome_2_tut.png')
        self.welcome_2_tut_button = new_button.Button(welcome_2_tut_img, None, 0.55, self.screen_x, self.screen_y, True, False, 0, -300)

        gesture_img = pygame.image.load('Game_Texts/gesture.png')
        gesture_alt_img = pygame.image.load('Game_Texts/gesture_alt.png')
        self.gesture_button = new_button.Button(gesture_img, gesture_alt_img, 0.45, self.screen_x, self.screen_y, True, True, 0, 100)
        controller_img = pygame.image.load('Game_Texts/controller.png')
        controller_alt_img = pygame.image.load('Game_Texts/controller_alt.png')
        self.controller_button = new_button.Button(controller_img, controller_alt_img, 0.45, self.screen_x, self.screen_y, True, True, 0, -200)
        speech_img = pygame.image.load('Game_Texts/speech.png')
        speech_alt_img = pygame.image.load('Game_Texts/speech_alt.png')
        self.speech_button = new_button.Button(speech_img, speech_alt_img, 0.45, self.screen_x, self.screen_y, True, True, 0, -100)
        movement_img = pygame.image.load('Game_Texts/movement.png')
        movement_alt_img = pygame.image.load('Game_Texts/movement_alt.png')
        self.movement_button = new_button.Button(movement_img, movement_alt_img, 0.45, self.screen_x, self.screen_y, True, True, 0, 0)
        how2play_img = pygame.image.load('Game_Texts/how2play.png')
        how2play_alt_img = pygame.image.load('Game_Texts/how2play_alt.png')
        self.how2play_button = new_button.Button(how2play_img, how2play_alt_img, 0.45, self.screen_x, self.screen_y, True, True, 0, 200)
        wait_4_all_img = pygame.image.load('Game_Texts/wait_4_all.png')
        self.wait_4_all_button = new_button.Button(wait_4_all_img, None, 0.55, self.screen_x, self.screen_y, True, False, 0, -330)
        ready_img = pygame.image.load('Game_Texts/ready.png')
        ready_alt_img = pygame.image.load('Game_Texts/ready_alt.png')
        self.ready_button = new_button.Button(ready_img, ready_alt_img, 0.45, self.screen_x, self.screen_y, True, True, 0, -90)
        ready_up_img = pygame.image.load('Game_Texts/ready_up.png')
        self.ready_up_button= new_button.Button(ready_up_img, None, 0.55, self.screen_x, self.screen_y, True, False, 0, -330)
        select_mode_img = pygame.image.load('Game_Texts/select_mode.png')
        self.select_mode_button = new_button.Button(select_mode_img, None, 0.55, self.screen_x, self.screen_y, True, False, 0, -330)
        singleplayer_img = pygame.image.load('Game_Texts/singleplayer.png')
        singleplayer_alt_img = pygame.image.load('Game_Texts/singleplayer_alt.png')
        multiplayer_img = pygame.image.load('Game_Texts/multiplayer.png')
        multiplayer_alt_img = pygame.image.load('Game_Texts/multiplayer_alt.png')
        self.singleplayer_button = new_button.Button(singleplayer_img, singleplayer_alt_img, 0.45, self.screen_x, self.screen_y, True, True, 0, -90)
        self.multiplayer_button = new_button.Button(multiplayer_img, multiplayer_alt_img, 0.45, self.screen_x, self.screen_y, True, True, 0, 10)
        no_srv_fnd_img = pygame.image.load('Game_Texts/no_srv_fnd.png')
        self.no_srv_fnd_button = new_button.Button(no_srv_fnd_img, None, 0.6, self.screen_x, self.screen_y, True, False, 0, -330)
        game_over_img = pygame.image.load('Game_Texts/game_over.png')
        self.game_over_button = new_button.Button(game_over_img, None, 0.6, self.screen_x, self.screen_y, True, False, 0, -330)
        score_img = pygame.image.load('Game_Texts/score.png')
        self.score_button = new_button.Button(score_img, None, 0.45, self.screen_x, self.screen_y, True, True, -30, -90)
        settings_img = pygame.image.load('Game_Texts/settings.png')
        self.settings_button = new_button.Button(settings_img, None, 0.6, self.screen_x, self.screen_y, True, False, 0, -330)
        fivemin_img = pygame.image.load('Game_Texts/5min.png')
        fivemin_alt_img = pygame.image.load('Game_Texts/5min_alt.png')
        self.fivemin_button = new_button.Button(fivemin_img, fivemin_alt_img, 0.35, self.screen_x, self.screen_y, False, True, 15, 240)
        tenmin_img = pygame.image.load('Game_Texts/10min.png')
        tenmin_alt_img = pygame.image.load('Game_Texts/10min_alt.png')
        self.tenmin_button = new_button.Button(tenmin_img, tenmin_alt_img, 0.35, self.screen_x, self.screen_y, False, True, 15, 320)
        fifteenmin_img = pygame.image.load('Game_Texts/15min.png')
        fifteenmin_alt_img = pygame.image.load('Game_Texts/15min_alt.png')
        self.fifteenmin_button = new_button.Button(fifteenmin_img, fifteenmin_alt_img, 0.35, self.screen_x, self.screen_y, False, True, 15, 400)
        resign_img = pygame.image.load('Game_Texts/resign.png')
        resign_alt_img = pygame.image.load('Game_Texts/resign_alt.png')
        self.resign_button = new_button.Button(resign_img, resign_alt_img, 0.45, self.screen_x, self.screen_y, False, True, self.screen_x - 330, self.screen_y-110)
        pickup_img = pygame.image.load('Game_Texts/pickup.png')
        self.pickup_button = new_button.Button(pickup_img, None, 0.45, self.screen_x, self.screen_y, False, True, self.screen_x - 420, self.screen_y-385)
        down_img = pygame.image.load('Game_Texts/down.png')
        self.down_button = new_button.Button(down_img, None, 0.45, self.screen_x, self.screen_y, False, True, self.screen_x - 420, self.screen_y-320)
        meat_img = pygame.image.load('Game_Texts/meat.png')
        self.meat_button = new_button.Button(meat_img, None, 0.45, self.screen_x, self.screen_y, False, True, self.screen_x - 420, self.screen_y-370)
        bread_img = pygame.image.load('Game_Texts/bread.png')
        self.bread_button = new_button.Button(bread_img, None, 0.45, self.screen_x, self.screen_y, False, True, self.screen_x - 420, self.screen_y-370)
        lettuce_img = pygame.image.load('Game_Texts/lettuce.png')
        self.lettuce_button = new_button.Button(lettuce_img, None, 0.45, self.screen_x, self.screen_y, False, True, self.screen_x - 420, self.screen_y-370)
        tomato_img = pygame.image.load('Game_Texts/tomato.png')
        self.tomato_button = new_button.Button(tomato_img, None, 0.45, self.screen_x, self.screen_y, False, True, self.screen_x - 420, self.screen_y-370)
        plate_img = pygame.image.load('Game_Texts/plate.png')
        self.plate_button = new_button.Button(plate_img, None, 0.45, self.screen_x, self.screen_y, False, True, self.screen_x - 420, self.screen_y-370)
        voice_commands_img = pygame.image.load('Game_Texts/voice_commands.png')
        self.voice_commands_button = new_button.Button(voice_commands_img, None, 0.45, self.screen_x, self.screen_y, False, True, self.screen_x - 420, self.screen_y-440)
        begin_img = pygame.image.load('Game_Texts/begin.png')
        begin_alt_img = pygame.image.load('Game_Texts/begin_alt.png')
        self.begin_button = new_button.Button(begin_img, begin_alt_img, 0.45, self.screen_x, self.screen_y, False, True, 380, 630)
        try_it_img = pygame.image.load('Game_Texts/try_it.png')
        try_it_alt_img = pygame.image.load('Game_Texts/try_it_alt.png')
        self.try_it_button = new_button.Button(try_it_img, try_it_alt_img, 0.45, self.screen_x, self.screen_y, True, True, 0, 300)
        skip_alt_img = pygame.image.load('Game_Texts/skip_alt.png')
        skip_img = pygame.image.load('Game_Texts/skip.png')
        self.skip_button = new_button.Button(skip_img, skip_alt_img, 0.35, self.screen_x, self.screen_y, False, True, self.screen_x - 280, self.screen_y-80)
        continue_alt_img = pygame.image.load('Game_Texts/continue_alt.png')
        continue_img = pygame.image.load('Game_Texts/continue.png')
        self.continue_button = new_button.Button(continue_img, continue_alt_img, 0.45, self.screen_x, self.screen_y, True, True, 0, 80)
        great_job_img = pygame.image.load('Game_Texts/great_job.png')
        self.great_job_button = new_button.Button(great_job_img, None, 0.6, self.screen_x, self.screen_y, True, False, 0, -20)
        tut_completed_img = pygame.image.load('Game_Texts/tut_completed.png')
        self.tut_completed_button = new_button.Button(tut_completed_img, None, 0.6, self.screen_x, self.screen_y, True, False, 0, -20)
        # have_fun_img = pygame.image.load('Game_Texts/have_fun.png')
        # self.have_fun_button = new_button.Button(have_fun_img, None, 0.6, SING_WIN_WIDTH, SING_WIN_HEIGHT, True, False, 0, 260)
        welcome_how2play_img = pygame.image.load('Game_Texts/wel_howtoplay.png')
        self.welcome_how2play_button = new_button.Button(welcome_how2play_img, None, 0.6, self.screen_x, self.screen_y, False, False, 120, 100)
        how2play_intro_text_img = pygame.image.load('Game_Texts/Intro_txt.png')
        self.how2play_intro_text_button = new_button.Button(how2play_intro_text_img, None, 0.5, self.screen_x, self.screen_y, False, False, 15, 220)

        tut_1_img = pygame.image.load('Game_Texts/tut_1_pic.png')
        self.tut_1_button = new_button.Button(tut_1_img, None, 0.5, self.screen_x, self.screen_y, False, True, 680, 220)
        tut_2_img = pygame.image.load('Game_Texts/tut_2_pic.png')
        self.tut_2_button = new_button.Button(tut_2_img, None, 0.3, self.screen_x, self.screen_y, False, True, 830, 220)
        tut_3_img = pygame.image.load('Game_Texts/tut_3_pic.png')
        self.tut_3_button = new_button.Button(tut_3_img, None, 0.2, self.screen_x, self.screen_y, False, True, 680, 460)
        tut_4_img = pygame.image.load('Game_Texts/tut_4_pic.png')
        self.tut_4_button = new_button.Button(tut_4_img, None, 0.5, self.screen_x, self.screen_y, False, True, 680, 340)
        obj1_text_img = pygame.image.load('Game_Texts/obj1_text.png')
        self.obj1_text_button = new_button.Button(obj1_text_img, None, 0.5, self.screen_x, self.screen_y, False, True, 15, 220)
        obj1_title_img = pygame.image.load('Game_Texts/obj1_title.png')
        self.obj1_title = new_button.Button(obj1_title_img, None, 0.6, self.screen_x, self.screen_y, False, True, 15, 100)

        tut_5_img = pygame.image.load('Game_Texts/tut_5_pic.png')
        self.tut_5_button = new_button.Button(tut_5_img, None, 0.35, self.screen_x, self.screen_y, False, True, 620, 220)
        tut_6_img = pygame.image.load('Game_Texts/tut_6_pic.png')
        self.tut_6_button = new_button.Button(tut_6_img, None, 0.5, self.screen_x, self.screen_y, False, True, 870, 220)
        tut_7_img = pygame.image.load('Game_Texts/tut_7_pic.png')
        self.tut_7_button = new_button.Button(tut_7_img, None, 0.5, self.screen_x, self.screen_y, False, True, 870, 400)
        tut_8_img = pygame.image.load('Game_Texts/tut_8_pic.png')
        self.tut_8_button = new_button.Button(tut_8_img, None, 0.5, self.screen_x, self.screen_y, False, True, 870, 470)
        obj2_text_img = pygame.image.load('Game_Texts/obj2_text.png')
        self.obj2_text_button = new_button.Button(obj2_text_img, None, 0.5, self.screen_x, self.screen_y, False, True, 15, 220)
        obj2_title_img = pygame.image.load('Game_Texts/obj2_title.png')
        self.obj2_title = new_button.Button(obj2_title_img, None, 0.6, self.screen_x, self.screen_y, False, True, 15, 100)

        tut_9_img = pygame.image.load('Game_Texts/tut_9_pic.png')
        self.tut_9_button = new_button.Button(tut_9_img, None, 0.4, self.screen_x, self.screen_y, False, True, 620, 220)
        tut_10_img = pygame.image.load('Game_Texts/tut_10_pic.png')
        self.tut_10_button = new_button.Button(tut_10_img, None, 0.6, self.screen_x, self.screen_y, False, True, 800, 220)
        tut_11_img = pygame.image.load('Game_Texts/tut_11_pic.png')
        self.tut_11_button = new_button.Button(tut_11_img, None, 0.6, self.screen_x, self.screen_y, False, True, 800, 300)
        obj3_text_img = pygame.image.load('Game_Texts/obj3_text.png')
        self.obj3_text_button = new_button.Button(obj3_text_img, None, 0.5, self.screen_x, self.screen_y, False, True, 15, 220)
        obj3_title_img = pygame.image.load('Game_Texts/obj3_title.png')
        self.obj3_title = new_button.Button(obj3_title_img, None, 0.6, self.screen_x, self.screen_y, False, True, 15, 100)

        tut_12_img = pygame.image.load('Game_Texts/tut_12_pic.png')
        self.tut_12_button = new_button.Button(tut_12_img, None, 0.45, self.screen_x, self.screen_y, False, True, 600, 80)
        tut_13_img = pygame.image.load('Game_Texts/tut_13_pic.png')
        self.tut_13_button = new_button.Button(tut_13_img, None, 0.6, self.screen_x, self.screen_y, False, True, 600, 420)
        tut_14_img = pygame.image.load('Game_Texts/tut_14_pic.png')
        self.tut_14_button = new_button.Button(tut_14_img, None, 0.6, self.screen_x, self.screen_y, False, True, 900, 460)
        obj4_text_img = pygame.image.load('Game_Texts/obj4_text.png')
        self.obj4_text_button = new_button.Button(obj4_text_img, None, 0.5, self.screen_x, self.screen_y, False, True, 15, 220)
        obj4_title_img = pygame.image.load('Game_Texts/obj4_title.png')
        self.obj4_title = new_button.Button(obj4_title_img, None, 0.6, self.screen_x, self.screen_y, False, True, 15, 100)

        tut_15_img = pygame.image.load('Game_Texts/tut_15_pic.png')
        self.tut_15_button = new_button.Button(tut_15_img, None, 0.35, self.screen_x, self.screen_y, False, True, 620, 100)
        tut_16_img = pygame.image.load('Game_Texts/tut_16_pic.png')
        self.tut_16_button = new_button.Button(tut_16_img, None, 0.5, self.screen_x, self.screen_y, False, True, 760, 360)
        tut_17_img = pygame.image.load('Game_Texts/tut_17_pic.png')
        self.tut_17_button = new_button.Button(tut_17_img, None, 0.35, self.screen_x, self.screen_y, False, True, 620, 370)
        tut_18_img = pygame.image.load('Game_Texts/tut_18_pic.png')
        self.tut_18_button = new_button.Button(tut_18_img, None, 0.6, self.screen_x, self.screen_y, False, True, 760, 440)
        obj5_text_img = pygame.image.load('Game_Texts/obj5_text.png')
        self.obj5_text_button = new_button.Button(obj5_text_img, None, 0.5, self.screen_x, self.screen_y, False, True, 15, 220)
        obj5_title_img = pygame.image.load('Game_Texts/obj5_title.png')
        self.obj5_title = new_button.Button(obj5_title_img, None, 0.6, self.screen_x, self.screen_y, False, True, 15, 100)

        tut_19_img = pygame.image.load('Game_Texts/tut_19_pic.png')
        self.tut_19_button = new_button.Button(tut_19_img, None, 0.6, self.screen_x, self.screen_y, False, True, 620, 140)
        tut_20_img = pygame.image.load('Game_Texts/tut_20_pic.png')
        self.tut_20_button = new_button.Button(tut_20_img, None, 0.5, self.screen_x, self.screen_y, False, True, 740, 270)
        tut_21_img = pygame.image.load('Game_Texts/tut_21_pic.png')
        self.tut_21_button = new_button.Button(tut_21_img, None, 0.4, self.screen_x, self.screen_y, False, True, 620, 450)
        obj6_text_img = pygame.image.load('Game_Texts/obj6_text.png')
        self.obj6_text_button = new_button.Button(obj6_text_img, None, 0.5, self.screen_x, self.screen_y, False, True, 15, 220)
        obj6_title_img = pygame.image.load('Game_Texts/obj6_title.png')
        self.obj6_title = new_button.Button(obj6_title_img, None, 0.6, self.screen_x, self.screen_y, False, True, 15, 100)

        controller_1_img = pygame.image.load('Game_Texts/controller_1.png')
        self.controller_1_button = new_button.Button(controller_1_img, None, 0.08, self.screen_x, self.screen_y, False, True, 690, 170)
        controller_2_img = pygame.image.load('Game_Texts/controller_2.png')
        self.controller_2_button = new_button.Button(controller_2_img, None, 0.08, self.screen_x, self.screen_y, False, True, 690, 550)
        controller_title_img = pygame.image.load('Game_Texts/controller_title.png')
        self.controller_title_button = new_button.Button(controller_title_img, None, 0.6, self.screen_x, self.screen_y, False, True, 15, 100)
        controller_text = pygame.image.load('Game_Texts/controller_text.png')
        self.controller_text_button = new_button.Button(controller_text, None, 0.5, self.screen_x, self.screen_y, False, True, 15, 220)

        speech_1_img = pygame.image.load('Game_Texts/speech_1.png')
        self.speech_1_button = new_button.Button(speech_1_img, None, 0.7, self.screen_x, self.screen_y, False, True, 630, 220)
        speech_title_img = pygame.image.load('Game_Texts/speech_title.png')
        self.speech_title_button = new_button.Button(speech_title_img, None, 0.6, self.screen_x, self.screen_y, False, True, 15, 100)
        speech_text = pygame.image.load('Game_Texts/speech_text.png')
        self.speech_text_button = new_button.Button(speech_text, None, 0.5, self.screen_x, self.screen_y, False, True, 15, 220)

        self.current_obj = 0
        
    def check_if_share(self, row, column):
        columns = [8, 9]
        rows = [4,5]
        
        if (row in rows and column in columns):
            return True
        else:
            return False
        
    def find_share_station(self, row, column):
        print("This is the amount of share stations:", str(len(self.all_share_stations)))
        
        for station in self.all_share_stations:
            print(str(station.y) + "," + str(station.x))
            # Maybe something wrong with the way share stations are indexed?
            if ((station.x == (column - 48) or station.x == (column + 48))
                and station.y == row):
                print("Matching station at:", str(station.y), str(station.x))
                return station
            
        if (len(self.all_share_stations) == 0):
            print("NO SHARE STATIONS!!!!!!")
        
        return None
    
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
                    BackgroundObject(self, self.bun_full_1_spritesheet, 0, 0, j, i, layer, (self.all_sprites))
                elif column == '5':
                    BackgroundObject(self, self.bun_full_2_spritesheet, 0, 0, j, i, layer, (self.all_sprites))
                elif column == '6':
                    BackgroundObject(self, self.meat_2_spritesheet, 0, 0, j, i, layer, (self.all_sprites))
                elif column == '!':
                    IngredientsCounter("Tomato",self, self.kitchen_spritesheet,white_counter["!"][0],white_counter["!"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.ingredients_stands))
                elif column == '^':
                    IngredientsCounter("Lettuce",self, self.kitchen_spritesheet,white_counter["!"][0],white_counter["!"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.ingredients_stands))
                elif column == '(':
                    IngredientsCounter("Meat",self, self.kitchen_spritesheet,white_counter["!"][0],white_counter["!"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.ingredients_stands))
                elif column == ')':
                    IngredientsCounter("Bun",self, self.kitchen_spritesheet,white_counter["!"][0],white_counter["!"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.ingredients_stands))
                elif column == '\\':
                    IngredientsCounter("Meat_2",self, self.kitchen_spritesheet,white_counter["!"][0],white_counter["!"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.ingredients_stands))
                elif column == '/':
                    IngredientsCounter("Bun_2",self, self.kitchen_spritesheet,white_counter["!"][0],white_counter["!"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.ingredients_stands))
                elif column == 'E':
                    self.all_counters.append(MultiplayerCounter(self, self.kitchen_spritesheet,white_counter["E"][0],white_counter["E"][1],j,i,layer,(self.all_sprites,self.counters,self.bottom_perspective_counters)))
                elif column == '$':
                    self.all_counters.append(ChopCounter(self, self.kitchen_spritesheet,white_counter["B"][0],white_counter["B"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.chopping_stations)))
                elif column == '*':
                    self.all_counters.append(IngredientsCounter("Plate",self, self.kitchen_spritesheet,white_counter["H"][0],white_counter["H"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.plate_stations)))
                elif column == '%':
                    self.all_counters.append(CookCounter('pan',self, self.kitchen_spritesheet,white_counter["%"][0],white_counter["%"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.cooking_stations)))
                elif column == 'B':
                    self.all_counters.append(MultiplayerCounter(self, self.kitchen_spritesheet,white_counter["B"][0],white_counter["B"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters)))
                elif column == 'J':
                    self.all_counters.append(MultiplayerCounter(self, self.kitchen_spritesheet,white_counter["J"][0],white_counter["J"][1],j,i,layer,(self.all_sprites,self.counters,self.bottom_perspective_counters)))
                elif column == 'G':
                    temp = MultiplayerCounter(self, self.kitchen_spritesheet,white_counter["G"][0],white_counter["G"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.left_counters))
                    if (self.check_if_share(i, j)):
                        self.all_share_stations.append(temp)
                    self.all_counters.append(temp)
                elif column == 'H':
                    temp = MultiplayerCounter(self, self.kitchen_spritesheet,white_counter["H"][0],white_counter["H"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.right_counters))
                    if (self.check_if_share(i, j)):
                        self.all_share_stations.append(temp)
                    self.all_counters.append(temp)
                elif column == 'V':
                    BackgroundObject(self,self.inventory_spritesheet,0,0,j,i,INVENTORY_LAYER,(self.all_sprites))             
                elif column == '8':
                    BackgroundObject(self,self.cut_state_spritesheet,0,0,j,i,layer,(self.all_sprites), 9, self.player, self.cook_state_list, self.cut_state_list) 
                elif column == '9':
                    BackgroundObject(self,self.cook_state_spritesheet,0,0,j,i,layer,(self.all_sprites), 8, self.player, self.cook_state_list, self.cut_state_list)       
                elif column == 'S':
                    MultiplayerCounter(self, self.kitchen_spritesheet,white_counter["S"][0],white_counter["S"][1],j,i,layer,(self.all_sprites,self.counters,self.bottom_perspective_counters))
                elif column == 'M':
                    self.all_counters.append(SubmitStation(self, self.kitchen_spritesheet,white_counter["G"][0],white_counter["G"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.left_counters,self.submit_stations)))
                elif column == '&':
                    BackgroundObject(self, self.kitchen_spritesheet,9*48,1408/32*48, j, i, COUNTER_LAYER+1, (self.all_sprites))
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
                elif column == '<':
                    BackgroundObject(self,self.share_left_spritesheet,0,0,j,i,COUNTER_LAYER+1,(self.all_sprites)) 
                elif column == '>':
                    BackgroundObject(self,self.share_right_spritesheet,0,0,j,i,COUNTER_LAYER+1,(self.all_sprites))  
                elif column != "." and column != "P":
                    MultiplayerCounter(self, self.kitchen_spritesheet,white_counter[column][0],white_counter[column][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters))

    def new(self):
        # a new game starts
        self.playing = True

        # initialize empty sprite groups
        self.all_sprites = pygame.sprite.LayeredUpdates()   # layered updates object
        self.item_updates = pygame.sprite.LayeredUpdates()
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
        self.player = MultiplayerPlayer(self,-1,-1)
        self.timer = MultiplayerTimer(self,14,0,60,FPS)
        self.score = Score(self,0,0)
        # self.recipes = [RecipeCard(self,3*48,0)]
        self.recipes = []
        self.item_gen = CounterItemsGenerator(self,self.item_updates)
        # game, x, y

        self.animations = pygame.sprite.LayeredUpdates()


        self.createTilemap(mult_counter_tilemap_back,COUNTER_BACK_LAYER)
        self.createTilemap(mult_counter_tilemap_back_items,COUNTER_BACK_ITEMS_LAYER)
        self.createTilemap(mult_counter_tilemap,COUNTER_LAYER)
        self.createTilemap(mult_counter_tilemap_2,COUNTER_FRONT_LAYER)
        self.createTilemap(mult_counter_front_items_tilemap,COUNTER_FRONT_LAYER+1)
        # self.createTilemap(foreground_tilemap,FOREGROUND_LAYER)
        # initialize_camera()

        ProgressBar(self, self.progress_spritesheet, 13*TILE_SIZE, 12*TILE_SIZE, COUNTER_LAYER, (self.all_sprites), 3*TILE_SIZE, TILE_SIZE, self.player)

        # self.setup_audiofile()
        self.setup_mqtt()

    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if(self.player.client_ID != None): # need to get the client_ID
                    pos = pygame.mouse.get_pos()
                    self.player.dest_x = ((round(pos[0]/48)-1) * 48)
                    self.player.dest_y = ((round(pos[1]/48)-1) * 48)

                    # temp_data = [int(pos[0]/32) * 32, int(pos[1]/32) * 32]
                    # self.socket_client.send(pickle.dumps(temp_data))

                    if(self.player.action is not None):
                        self.client.publish("overcooked_mic"+str(self.player.client_ID), "Stop", qos=1)
                        self.client.publish("overcooked_imu"+str(self.player.client_ID), "Mic Stop", qos=1)
                        self.player.stop_everything()

                    # print('CLICK')
                    # print(int(pos[0]/32) * 32, int(pos[1]/32) * 32)
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        # game loop updates

        # run the update method of every sprite in the all_sprites group
        self.all_sprites.update() 
        self.item_updates.update()

    def draw(self):
        # game loop draw
        self.screen.fill((222,184,135))

        # draws the image and rect of all sprites in the all_sprites group onto the screen
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()
        self.voice_commands_button.draw(self.screen)
        if self.resign_button.draw(self.screen) and self.clicked is True:
            self.playing = False
            self.clicked = False
            # DELTA: Resign both players from the game!
            self.socket_client.send(pickle.dumps([-12345, "fill"])) # CODE: -12345 -> force quit on both players!
        if self.player.location is not None:
            if self.player.location == "Plate Station":
                self.plate_button.draw(self.screen)
            elif self.player.location == "Ingredients Stand":
                if self.player.location_sprite.ingredient == 'Meat' or self.player.location_sprite.ingredient == 'Meat_2':
                    self.meat_button.draw(self.screen)
                elif self.player.location_sprite.ingredient == 'Lettuce':
                    self.lettuce_button.draw(self.screen)
                elif self.player.location_sprite.ingredient == 'Bun' or self.player.location_sprite.ingredient == 'Bun_2':
                    self.bread_button.draw(self.screen)
                elif self.player.location_sprite.ingredient == 'Tomato':
                    self.tomato_button.draw(self.screen)
            elif self.player.location in ["Chopping Station", "Cooking Station", "Top Counter", "Left Counter", "Right Counter", "Bottom Counter"]:
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
        
    def main(self):
        # self.screen = pygame.display.set_mode((MULT_WIN_WIDTH, MULT_WIN_HEIGHT))
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        # game loop

        while self.playing:
        # if(self.playing):
            self.events()
            self.update()
            self.draw()

        self.client.publish('overcooked_mic'+str(self.player.client_ID), "stop", qos=1)
        self.client.loop_stop()
        self.client.disconnect()
        # self.speech_log.close()
        self.running = False
        self.clicked = False
        self.player.stop_sounds()

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
                    while True:
                        self.screen.blit(self.title_screen, (0,0))
                        self.ready_up_button.draw(self.screen)
                        if self.ready_button.draw(self.screen) and self.clicked is True:
                            pass
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                        self.clicked = True
                        pygame.display.update()
                        self.clock.tick(FPS)
                if self.multiplayer_button.draw(self.screen) and self.clicked is True:
                    # Connect the client online
                    try:
                        client_socket.connect((config["Host"], config["Port"]))
                        print("STATUS -> Client bound successfully!")
                        return self.player_input_screen()
                    except socket.error as e:
                        print("ERROR ->", str(e))
                        return self.no_server_found_screen()
                if self.back_button.draw(self.screen) and self.clicked is True:
                    return self.intro_screen()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                self.clicked=True
                pygame.display.update()
                self.clock.tick(FPS)
    def no_server_found_screen(self):
        self.clicked=False
        while True:
            self.screen.blit(self.title_screen, (0,0))
            self.no_srv_fnd_button.draw(self.screen)
            if self.back_button.draw(self.screen) and self.clicked is True:
                return self.gamemode_selection_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.clicked=True
            pygame.display.update()
            self.clock.tick(FPS)

    def player_input_screen(self):
            self.clicked = False
            player1_txt = font.render("Enter Your Name", True, black)
            input_box1 = InputBox((self.screen_x - player1_txt.get_width()) / 2, self.screen_y / 7 + 100, 140, 32)
        
            while True:
                self.screen.blit(self.title_screen, (0,0))
                self.enter_name.draw(self.screen)

                if self.back_button.draw(self.screen) and self.clicked is True:
                    return self.gamemode_selection_screen()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    name = input_box1.handle_event(event)
                    if name != None:
                        self.register(self.socket_client, name)
                        return self.waiting_connection_screen() 
                input_box1.update()
                input_box1.draw(self.screen)                   
                self.clicked=True
                pygame.display.update()
                self.clock.tick(FPS)

    def tutorial_screen_intro(self):
        self.clicked = False
        while True:
            if self.clicked:
                self.screen.blit(self.title_screen, (0,0))
                self.welcome_2_tut_button.draw(self.screen)
                if self.gesture_button.draw(self.screen):
                    print("gesture")
                if self.controller_button.draw(self.screen):
                    print("controller")
                if self.speech_button.draw(self.screen):
                    print("speech")
                if self.movement_button.draw(self.screen):
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

    def waiting_connection_screen(self):
        self.clicked = False
        done = False
        self.socket_client.setblocking(False)
        while not done:
            try: condition = pickle.loads(self.socket_client.recv(self.header))
            except: condition = None
            if (condition != True):
                self.screen.blit(self.title_screen, (0,0))
                self.wait_4_all_button.draw(self.screen)
                pygame.draw.rect(self.screen, black, self.r)
                self.r.move_ip(5, 0)
            else:
                self.socket_client.setblocking(True)
                self.clicked = False
                while not done:
                    self.screen.blit(self.title_screen, (0,0))
                    self.ready_up_button.draw(self.screen)
                    if self.ready_button.draw(self.screen) and self.clicked is True:
                        done = True
                        self.socket_client.send(pickle.dumps([sys.argv[1]])) # Send ready signal to game server
                        g.new()
                        ready_condition = pickle.loads(self.socket_client.recv(self.header)) # wait to recieve the ready signal from the server
                        self.socket_client.setblocking(False)
                        self.clicked = False
                        while g.running:
                            if self.clicked:
                                g.main()
                                g.game_over()
                            self.clicked = True
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    self.clicked = True
                    pygame.display.update()
                    self.clock.tick(FPS)
            if not self.screen.get_rect().contains(self.r):
                self.r.x = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            self.clock.tick(FPS)

    def game_over(self):
        self.clicked = False
        myFont = pygame.font.SysFont("Times New Roman", 18)
        scoreDisplay = myFont.render(str(self.score.score), 1, black)
        print("This is the FINAL SCORE:", str(self.score.score))
        while True:
            if self.clicked:
                self.screen.blit(self.title_screen, (0,0))
                self.game_over_button.draw(self.screen)
                self.score_button.draw(self.screen)
                self.screen.blit(scoreDisplay, (MULT_WIN_WIDTH-30, MULT_WIN_HEIGHT- 30)) # DELTA
                if self.back_button.draw(self.screen) and self.clicked is True:
                    return self.intro_screen()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            self.clicked = True
            pygame.display.update()
            self.clock.tick(FPS)

    def register(self,client_socket, name): # ACTION = 0
        client_socket.send(pickle.dumps([0, name])) # Send information to be stored

##############################################################################
import pickle
import socket
from playground_building_blocks import *

# %% Client Configuration
config = dict()
# # config["Host"] = "192.168.1.91" # IPv4 address of ENG IV lab room
# config["Host"] = "192.168.1.91"
# =======
config["Host"] = socket.gethostbyname(socket.gethostname())
config["Port"] = 4900 # Unique ID, can be any number but must match server's
config["HEADER"] = 4096 # Defines max number of byte transmission

# %% Client Setup
# Create the client socket
client_socket = socket.socket()

# Connect the client online
# try:
#     client_socket.connect((config["Host"], config["Port"]))
#     print("STATUS -> Client bound successfully!")
    
# except socket.error as e:
#     print("ERROR ->", str(e))
    
# Remove blocking synchronous clients in favor of realtime nonblocking logic
# client_socket.setblocking(False)


# %% Control Loop
# condition = False
# while (condition != True):
#     try: condition = pickle.loads(client_socket.recv(HEADER))
#     except: condition = None
#     pass

g = Game(client_socket, config["HEADER"])
g.intro_screen() # this should technically loop forever until closed out of
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
