import pygame
from multiplayer_config_48 import * 
from ingredients import *
from sprites import *
from animations import *
from counters import *
import math
import random
import speech_recognition as sr 
from pymouse import PyMouse
import pickle
from playground_building_blocks import *
from pygame import mixer

# Player inherits from pygame.sprite.Sprite (class in pygame module)
class Partner(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        # add player to all_sprites group of game object
        self.groups = self.game.all_sprites

        # call init method for inherited class
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = 2*TILE_SIZE

        self.x_change = 0
        self.y_change = 0
        self.dest_x = self.x
        self.dest_y = self.y
        self.prev_dest_y = self.dest_y
        self.prev_x = self.x
        self.prev_y = self.y

        self.facing = 'down'
        self.prev_facing = 'down'
        self.animation_loop = 1

        self.side = "bottom"

        self.gesture = False

        self.inventory = []
        self.image = self.game.character_idle_spritesheet.get_sprite(18*self.width,0,0,0,self.width,self.height)
        self.image_name = 'down_idle'
        self.prev_image_name = 'down_idle'

        # hit box of rect and image are the same
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.right_run = [self.game.character_run_spritesheet.get_sprite(0*self.width,0,0,0,self.width, self.height),
                    self.game.character_run_spritesheet.get_sprite(1*self.width,0,0,0,self.width, self.height),
                    self.game.character_run_spritesheet.get_sprite(2*self.width,0,0,0,self.width, self.height),
                    self.game.character_run_spritesheet.get_sprite(3*self.width,0,0,0,self.width, self.height),
                    self.game.character_run_spritesheet.get_sprite(4*self.width,0,0,0,self.width, self.height),
                    self.game.character_run_spritesheet.get_sprite(5*self.width,0,0,0,self.width, self.height)]
        self.up_run = [self.game.character_run_spritesheet.get_sprite(6*self.width,0,0,0,self.width, self.height),
                self.game.character_run_spritesheet.get_sprite(7*self.width,0,0,0,self.width, self.height),
                self.game.character_run_spritesheet.get_sprite(8*self.width,0,0,0,self.width, self.height),
                self.game.character_run_spritesheet.get_sprite(9*self.width,0,0,0,self.width, self.height),
                self.game.character_run_spritesheet.get_sprite(10*self.width,0,0,0,self.width, self.height),
                self.game.character_run_spritesheet.get_sprite(11*self.width,0,0,0,self.width, self.height)]
        self.left_run = [self.game.character_run_spritesheet.get_sprite(12*self.width,0,0,0,self.width, self.height),
                self.game.character_run_spritesheet.get_sprite(13*self.width,0,0,0,self.width, self.height),
                self.game.character_run_spritesheet.get_sprite(14*self.width,0,0,0,self.width, self.height),
                self.game.character_run_spritesheet.get_sprite(15*self.width,0,0,0,self.width, self.height),
                self.game.character_run_spritesheet.get_sprite(16*self.width,0,0,0,self.width, self.height),
                self.game.character_run_spritesheet.get_sprite(17*self.width,0,0,0,self.width, self.height)]
        self.down_run = [self.game.character_run_spritesheet.get_sprite(18*self.width,0,0,0,self.width, self.height),
                    self.game.character_run_spritesheet.get_sprite(19*self.width,0,0,0,self.width, self.height),
                    self.game.character_run_spritesheet.get_sprite(20*self.width,0,0,0,self.width, self.height),
                    self.game.character_run_spritesheet.get_sprite(21*self.width,0,0,0,self.width, self.height),
                    self.game.character_run_spritesheet.get_sprite(22*self.width,0,0,0,self.width, self.height),
                    self.game.character_run_spritesheet.get_sprite(23*self.width,0,0,0,self.width, self.height)]
        self.right_idle = [self.game.character_idle_spritesheet.get_sprite(0*self.width,0,0,0,self.width, self.height),
                    self.game.character_idle_spritesheet.get_sprite(1*self.width,0,0,0,self.width, self.height),
                    self.game.character_idle_spritesheet.get_sprite(2*self.width,0,0,0,self.width, self.height),
                    self.game.character_idle_spritesheet.get_sprite(3*self.width,0,0,0,self.width, self.height),
                    self.game.character_idle_spritesheet.get_sprite(4*self.width,0,0,0,self.width, self.height),
                    self.game.character_idle_spritesheet.get_sprite(5*self.width,0,0,0,self.width, self.height)]
        self.up_idle = [self.game.character_idle_spritesheet.get_sprite(6*self.width,0,0,0,self.width, self.height),
                self.game.character_idle_spritesheet.get_sprite(7*self.width,0,0,0,self.width, self.height),
                self.game.character_idle_spritesheet.get_sprite(8*self.width,0,0,0,self.width, self.height),
                self.game.character_idle_spritesheet.get_sprite(9*self.width,0,0,0,self.width, self.height),
                self.game.character_idle_spritesheet.get_sprite(10*self.width,0,0,0,self.width, self.height),
                self.game.character_idle_spritesheet.get_sprite(11*self.width,0,0,0,self.width, self.height)]
        self.left_idle = [self.game.character_idle_spritesheet.get_sprite(12*self.width,0,0,0,self.width, self.height),
                self.game.character_idle_spritesheet.get_sprite(13*self.width,0,0,0,self.width, self.height),
                self.game.character_idle_spritesheet.get_sprite(14*self.width,0,0,0,self.width, self.height),
                self.game.character_idle_spritesheet.get_sprite(15*self.width,0,0,0,self.width, self.height),
                self.game.character_idle_spritesheet.get_sprite(16*self.width,0,0,0,self.width, self.height),
                self.game.character_idle_spritesheet.get_sprite(17*self.width,0,0,0,self.width, self.height)]
        self.down_idle = [self.game.character_idle_spritesheet.get_sprite(18*self.width,0,0,0,self.width, self.height),
                        self.game.character_idle_spritesheet.get_sprite(19*self.width,0,0,0,self.width, self.height),
                        self.game.character_idle_spritesheet.get_sprite(20*self.width,0,0,0,self.width, self.height),
                        self.game.character_idle_spritesheet.get_sprite(21*self.width,0,0,0,self.width, self.height),
                        self.game.character_idle_spritesheet.get_sprite(22*self.width,0,0,0,self.width, self.height),
                        self.game.character_idle_spritesheet.get_sprite(23*self.width,0,0,0,self.width, self.height)]

        self.chop = [self.game.character_chop_spritesheet.get_sprite(0*self.width,0,0,0,self.width, self.height),
                        self.game.character_chop_spritesheet.get_sprite(1*self.width,0,0,0,self.width, self.height),
                        self.game.character_chop_spritesheet.get_sprite(2*self.width,0,0,0,self.width, self.height),
                        self.game.character_chop_spritesheet.get_sprite(3*self.width,0,0,0,self.width, self.height),
                        self.game.character_chop_spritesheet.get_sprite(4*self.width,0,0,0,self.width, self.height),
                        self.game.character_chop_spritesheet.get_sprite(5*self.width,0,0,0,self.width, self.height)]
        self.cook = [self.game.character_stir_spritesheet.get_sprite(0*self.width,0,0,0,self.width, self.height),
                        self.game.character_stir_spritesheet.get_sprite(1*self.width,0,0,0,self.width, self.height),
                        self.game.character_stir_spritesheet.get_sprite(2*self.width,0,0,0,self.width, self.height),
                        self.game.character_stir_spritesheet.get_sprite(3*self.width,0,0,0,self.width, self.height),
                        self.game.character_stir_spritesheet.get_sprite(4*self.width,0,0,0,self.width, self.height),
                        self.game.character_stir_spritesheet.get_sprite(5*self.width,0,0,0,self.width, self.height)]
        self.pickup_right = [self.game.character_pickup_spritesheet.get_sprite(0*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(1*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(2*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(3*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(4*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(5*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(6*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(7*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(8*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(9*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(10*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(11*self.width,0,0,0,self.width, self.height)]
        self.pickup_up = [self.game.character_pickup_spritesheet.get_sprite(12*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(13*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(14*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(15*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(16*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(17*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(18*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(19*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(20*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(21*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(22*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(23*self.width,0,0,0,self.width, self.height)]
        self.pickup_left = [self.game.character_pickup_spritesheet.get_sprite(24*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(25*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(26*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(27*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(28*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(29*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(30*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(31*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(32*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(33*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(34*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(35*self.width,0,0,0,self.width, self.height)]
        self.pickup_down = [self.game.character_pickup_spritesheet.get_sprite(36*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(37*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(38*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(39*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(40*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(41*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(42*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(43*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(44*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(45*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(46*self.width,0,0,0,self.width, self.height),
                    self.game.character_pickup_spritesheet.get_sprite(47*self.width,0,0,0,self.width, self.height)]

        self.putdown_right = [self.game.character_putdown_spritesheet.get_sprite(0*self.width,0,0,0,self.width, self.height),
                    self.game.character_putdown_spritesheet.get_sprite(1*self.width,0,0,0,self.width, self.height),
                    self.game.character_putdown_spritesheet.get_sprite(2*self.width,0,0,0,self.width, self.height),
                    self.game.character_putdown_spritesheet.get_sprite(3*self.width,0,0,0,self.width, self.height),
                    self.game.character_putdown_spritesheet.get_sprite(4*self.width,0,0,0,self.width, self.height),
                    self.game.character_putdown_spritesheet.get_sprite(5*self.width,0,0,0,self.width, self.height),
                    self.game.character_putdown_spritesheet.get_sprite(6*self.width,0,0,0,self.width, self.height),
                    self.game.character_putdown_spritesheet.get_sprite(7*self.width,0,0,0,self.width, self.height),
                    self.game.character_putdown_spritesheet.get_sprite(8*self.width,0,0,0,self.width, self.height),
                    self.game.character_putdown_spritesheet.get_sprite(9*self.width,0,0,0,self.width, self.height)]

        self.putdown_up = [self.game.character_putdown_spritesheet.get_sprite(10*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(11*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(12*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(13*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(14*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(15*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(16*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(17*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(18*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(19*self.width,0,0,0,self.width, self.height)]

        self.putdown_left = [self.game.character_putdown_spritesheet.get_sprite(20*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(21*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(22*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(23*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(24*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(25*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(26*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(27*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(28*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(29*self.width,0,0,0,self.width, self.height)]

        self.putdown_down = [self.game.character_putdown_spritesheet.get_sprite(30*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(31*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(32*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(33*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(34*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(35*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(36*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(37*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(38*self.width,0,0,0,self.width, self.height),
            self.game.character_putdown_spritesheet.get_sprite(39*self.width,0,0,0,self.width, self.height)]

        self.location = None
        self.location_sprite = None
        self.message = None
        self.action = None
        self.prev_action = None
        self.before = True
        self.during = True
        self.after = True
        self.client_ID = None
        self.frame = 0
        self.effects = []


    def update(self):
        # print('partner update')
        # print(self.image_name)#, self.rect.y. self.facing, self.image_name, self.animation_loop, self.action))
        # if(self.prev_image_name == 'cook' and self.prev_image_name != self.image_name):
        #     for e in self.effects:
        #         e.kill()
        # if(self.prev_image_name == 'chop' and self.prev_image_name != self.image_name):
        #     for e in self.effects:
        #         e.kill()
        if(self.action == 'Pick Up' or self.action == 'Put Down' or self.action == None):
            # print('killing effects---------------------------------------------------------------')
            for e in self.effects:
                e.kill()

        if(self.image_name == 'right_idle'):
            self.image = self.right_idle[math.floor(self.animation_loop)%IDLE_FRAMES]
        elif(self.image_name == 'right_run'):
            self.image = self.right_run[math.floor(self.animation_loop)%RUN_FRAMES]
        elif(self.image_name == 'up_idle'):
            self.image = self.up_idle[math.floor(self.animation_loop)%IDLE_FRAMES]
        elif(self.image_name == 'up_run'):
            self.image = self.up_run[math.floor(self.animation_loop)%RUN_FRAMES]
        elif(self.image_name == 'left_idle'):
            self.image = self.left_idle[math.floor(self.animation_loop)%IDLE_FRAMES]
        elif(self.image_name == 'left_run'):
            self.image = self.left_run[math.floor(self.animation_loop)%RUN_FRAMES]
        elif(self.image_name == 'down_idle'):
            self.image = self.down_idle[math.floor(self.animation_loop)%IDLE_FRAMES]
        elif(self.image_name == 'down_run'):
            self.image = self.down_run[math.floor(self.animation_loop)%RUN_FRAMES]
        elif(self.image_name == 'pickup_right'):
            self.image = self.pickup_right[math.floor(self.animation_loop)%PICKUP_FRAMES]
        elif(self.image_name == 'pickup_up'):
            self.image = self.pickup_up[math.floor(self.animation_loop)%PICKUP_FRAMES]
        elif(self.image_name == 'pickup_left'):
            self.image = self.pickup_left[math.floor(self.animation_loop)%PICKUP_FRAMES]
        elif(self.image_name == 'pickup_down'):
            self.image = self.pickup_down[math.floor(self.animation_loop)%PICKUP_FRAMES]
        elif(self.image_name == 'putdown_right'):
            self.image = self.putdown_right[math.floor(self.animation_loop)%PUTDOWN_FRAMES]
        elif(self.image_name == 'putdown_up'):
            self.image = self.putdown_up[math.floor(self.animation_loop)%PUTDOWN_FRAMES]
        elif(self.image_name == 'putdown_left'):
            self.image = self.putdown_left[math.floor(self.animation_loop)%PUTDOWN_FRAMES]
        elif(self.image_name == 'putdown_down'):
            self.image = self.putdown_down[math.floor(self.animation_loop)%PUTDOWN_FRAMES]
        elif(self.image_name == 'chop'):
            self.image = self.chop[math.floor(self.animation_loop)%CHOP_FRAMES]
            if(self.prev_image_name != 'chop'):
                print('create effects chop')
                self.effects.append(Effects(self.game,self.game.knife_animation,self.rect.x,self.rect.y,COUNTER_FRONT_ITEMS_LAYER+TOP_BUN_LAYER+1,self.groups,0.1,CHOP_FRAMES,54,102,'during',self))
        elif(self.image_name == 'cook'):
            self.image = self.cook[math.floor(self.animation_loop)%STIR_FRAMES]
        if(self.action == 'Speak'):
            if(self.prev_action != self.action):
                print('create effects')
                self.effects.append(Effects(self.game,self.game.speaking_animation,self.rect.x,self.rect.y-2*TILE_SIZE,self._layer+1,(self.game.all_sprites),0.2,SPEAK_FRAMES,TILE_SIZE,2*TILE_SIZE,"during",self))

        self.prev_image_name = self.image_name
        self.prev_action = self.action


