import pygame
from multiplayer_config_48 import * 
from ingredients import *
from recipe import RecipeCard
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
from partner import *

# Player inherits from pygame.sprite.Sprite (class in pygame module)
class MultiplayerPlayer(pygame.sprite.Sprite):
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

        # hit box of rect and image are the same
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.prev_code = 0

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
        self.before = False
        self.during = False
        self.after = False
        self.client_ID = None
        self.frame = 0

        self.partner = None

    def check_set_location(self, hit_top, hit_bottom, hit_block):
        if(hit_top):
            if(self.game.ingredients_stands in hit_top[0].groups):
                self.location = "Ingredients Stand"
                self.location_sprite = hit_top[0]
                if(self.x_change == 0 and self.y_change == 0):
                    self.facing = 'up'
            elif(self.game.cooking_stations in hit_top[0].groups):
                self.location = "Cooking Station"
                self.location_sprite = hit_top[0]
                if(self.x_change == 0 and self.y_change == 0):
                    self.facing = 'up'
            else:
                if(hit_bottom):
                    if(self.game.top_perspective_counters in hit_top[0].groups and self.game.bottom_perspective_counters in hit_bottom[0].groups):
                        self.location = "Top Counter"
                        self.location_sprite = hit_top[0]
                    if(self.x_change == 0 and self.y_change == 0):
                        self.facing = 'up'
                else:
                    if(self.game.chopping_stations in hit_top[0].groups):
                        self.location = "Chopping Station"
                        self.location_sprite = hit_top[0]
                        if(self.x_change == 0 and self.y_change == 0):
                            self.facing = 'down'
                    else:
                        self.location = "Bottom Counter"
                        self.location_sprite = hit_top[0]
                        if(self.x_change == 0 and self.y_change == 0):
                            self.facing = 'down'
        elif(hit_block):
            if(self.game.submit_stations in hit_block[0].groups):
                self.location = "Submit Station"
                self.facing = 'left'
                self.location_sprite = hit_block[0]
            elif(self.game.left_counters in hit_block[0].groups):
                self.location = "Left Counter"
                self.location_sprite = hit_block[0]
                self.facing = 'left'
            elif(self.game.plate_stations in hit_block[0].groups):
                self.location = "Plate Station"
                self.location_sprite = hit_block[0]
                self.facing = 'right'
            elif(self.game.right_counters in hit_block[0].groups):
                self.location = "Right Counter"
                self.location_sprite = hit_block[0]
                self.facing = 'right'

        # if(self.location != None):
        #     print(self.location)
        # if(self.action != None):
        #     print(self.action)

    def stop_everything(self):
        self.action = None
        self.message = None
        self.before = False
        self.during = False
        self.after = False


    def collide_counters(self, direction):
        hits_top = pygame.sprite.spritecollide(self, self.game.top_perspective_counters, False)
        hits_bottom = pygame.sprite.spritecollide(self, self.game.bottom_perspective_counters, False)
        hits_block = pygame.sprite.spritecollide(self, self.game.block_counters, False)

        # self.location = None
        if direction == "x":
            # checks if the rect of one sprite is inside the rect of another sprite
            # False: do not want to delete sprite upon collision

            if(hits_block):
                if self.x_change > 0:   # moving right
                    # if(abs(self.dest_x-self.rect.x) <= TILE_SIZE and self.rect.y == self.dest_y):
                    if(self.rect.y == self.dest_y):
                        self.x_change = 0
                        # self.dest_x = self.dest_x - TILE_SIZE
                        self.dest_x = self.dest_x
                        # print(str(self.dest_x), hits[0].rect.left, self.rect.x)
                        self.dest_x = hits_block[0].rect.left - TILE_SIZE
                        self.prev_x =  self.rect.x
                    self.rect.x = hits_block[0].rect.left - self.rect.width
                    
                if self.x_change < 0:
                    # print('left here')
                    # if(abs(self.dest_x-self.rect.x) <= TILE_SIZE and self.rect.y == self.dest_y):
                    if(self.rect.y == self.dest_y):
                        self.x_change = 0
                        # self.dest_x = self.dest_x + TILE_SIZE
                        # print(str(self.dest_x), hits[0].rect.right, self.rect.x)
                        self.dest_x = hits_block[0].rect.right
                        self.dest_x = self.dest_x
                        self.prev_x =  self.rect.x
                    self.rect.x = hits_block[0].rect.right

        if direction == "y":
            # checks if the rect of one sprite is inside the rect of another sprite
            # False: do not want to delete sprite upon collision

            if(hits_top):
                if(hits_bottom):
                    if(self.y_change < 0):
                        if (self.rect.y + self.height < hits_bottom[0].rect.bottom):
                            self.rect.y = hits_bottom[0].rect.bottom - self.height
                            if(self.dest_x == self.rect.x):
                                self.prev_dest_y = self.dest_y
                                self.dest_y = self.rect.y
                            self.y_change = 0
                else:
                    if (self.y_change >= 0): 
                        # print('yahoo3')
                        if (self.rect.y + self.height >= hits_top[0].rect.top + cover_height):
                            self.rect.y = hits_top[0].rect.top + cover_height - self.height
                            # print('yahoo2')
                            # if (abs(self.dest_y - self.rect.y) < TILE_SIZE + cover_height):
                            # if(self.dest_x == self.rect.x):
                            self.prev_dest_y = self.dest_y
                            self.dest_y = self.rect.y
                            self.y_change = 0
                            # print('yahoo')

        self.check_set_location(hits_top,hits_bottom,hits_block)


    # player's update method called b/c game's update method calls all_sprites.update()
    def update(self):
        self.movement()
        self.user_action()
        self.animate()
        if (self.x_change != 0 or self.y_change != 0):
            self.location = None
            self.location_sprite = None
            self.message = None
            self.action = None

        self.rect.x += self.x_change
        self.collide_counters("x")
        self.rect.y += self.y_change
        self.collide_counters("y")

        # print(self.x_change)
        # print(self.rect.x)

        self.y_change = 0
        self.x_change = 0            

        self.frame += 1
        data = get_unblocked_data(self.game.socket_client)
        
        # if (self.client_ID == 0):
        #     if (data != None and data[0] != 77):
        #         print(data)

        if(data != None):
            print(data)
        
        # data = None
        if (data != None and type(data) == list and data[0] == 99):
            for test_item in data[1:]:
                # test_item = data[1] # list of item's attributes
                print("This is test item:")
                print(test_item)
                print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                # coords = (data[1][-2], data[1][-1])
                coords = (test_item[-2], test_item[-1])
                print("Original coords:", str(coords[0]), str(coords[1]))
                station_test = self.game.find_share_station(coords[1], coords[0])
                
                # Code copied from counter.place_all_items()
                station_test.manually_place_one_item(test_item)
            self.game.socket_client.send(pickle.dumps([999, data[-1]]))
            
        if (data != None and type(data) == list and data[0] == 88):
            # This means we are retrieving updated scores from other players!
            updated_scores = data[1]
            self.game.score.set_score(updated_scores)
            self.game.score.del_recipe_at_index(data[2])
            self.game.socket_client.send(pickle.dumps([888, data[-1]]))
            # Don't know what to do with it though?
            
        if (data != None and type(data) == list and data[0] == 77):
            # We need to update the timer!
            self.game.timer.set_time(data[1])

            # If the timer has reached the end, quit the game!
            if (data[2] == True):
                self.game.game_over()
            # self.game.socket_client.send(pickle.dumps([777, data[-1]]))
            pass
        
        if (data != None and type(data) == list and data[0] == 66):
            print("Received notification to set share station to be free!")
            print("Received station coords:", str(data[1][0]), str(data[1][1]))
            # We need to set that station to be unoccupied!
            countertop = self.game.find_share_station(data[1][0], data[1][1])
            countertop = self.game.find_share_station(countertop.y, countertop.x)
            countertop.occupied = False
            self.game.socket_client.send(pickle.dumps([666, data[-1]]))

        if (data != None and type(data) == list and data[0] == 33):
            # We need to update the timer!
            if(len(self.game.recipes) < 5):
                self.game.recipes.append(RecipeCard(self.game,3*TILE_SIZE+(len(self.game.recipes))*2*TILE_SIZE,0,data[1],data[2],data[3]))
                
            print('recieved 33, sending 333 back!-------------------------------------' + str(self.frame))
            self.game.socket_client.send(pickle.dumps([333, data[-1]]))
            
            
            
        # Print received data, if it exists
        elif (data != None and type(data) == list and data[0] == 22):
            prev_message = data
            self.partner.rect.x = data[1][2]
            self.partner.rect.y = data[1][3]
            self.partner.image_name = data[1][5]
            self.partner.animation_loop = data[1][6]
            self.partner.action = data[1][7]
            self.prev_code = data[0]
            self.game.item_gen.gen_items(data[2])
            #print("SERVER SENDS -> " + str(data))
        elif(data != None and type(data)==str):
            print('my client id: ' + data[10:])
            self.client_ID = int(data[10:])
            if(self.client_ID == 0):
                self.x = 6*TILE_SIZE
                self.y = 7*TILE_SIZE
                self.rect.x = self.x
                self.rect.y = self.y
                self.dest_x = self.x
                self.dest_y = self.y
                self.partner = Partner(self.game,15,7)
            elif(self.client_ID == 1):
                self.x = 15*TILE_SIZE
                self.y = 7*TILE_SIZE
                self.rect.x = self.x
                self.rect.y = self.y
                self.dest_x = self.x
                self.dest_y = self.y
                self.partner = Partner(self.game,6,7)
        elif (data != None and type(data) == float):
            pass

        # temp_data = [22, self.client_ID, self.frame, self.rect.x,self.rect.y,self.facing,self.image_name,self.animation_loop,self.action]
        # self.game.socket_client.send(pickle.dumps(temp_data))
        # elif (data != None):
        #     print(data)
            # temp_data = [self.client_ID, self.frame, 
            # 2-self.rect.x,
            # 3-self.rect.y,
            # 4-self.facing,
            # 5-self.image_name,
            # 6-self.animation_loop,
            # 7-self.action]


            
            # print("TIMER -> " + str(data))

        # print('update')
        # print(self.rect.x, self.rect.y)
    def movement(self):
        # get all keys that have been pressed
        if(self.action is None):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.x_change = -1 * PLAYER_SPEED
                self.facing = 'left'
            if keys[pygame.K_RIGHT]:
                self.x_change = PLAYER_SPEED
                self.facing = 'right'
            if keys[pygame.K_UP]:
                self.y_change = -1 * PLAYER_SPEED
                self.facing = 'up'
            if keys[pygame.K_DOWN]:
                self.y_change = PLAYER_SPEED
                self.facing = 'down'
            else:
                if ((self.rect.x != self.dest_x or self.rect.y != self.dest_y)):
                    if((self.rect.x % TILE_SIZE != 0 or (self.rect.y % TILE_SIZE != 0 and self.rect.y != self.dest_y))):
                        # print('continue')
                        # print(self.rect.x, self.rect.y)
                        if(self.prev_dest_y % TILE_SIZE != 0 and (self.dest_y < self.prev_dest_y)):
                        # if(self.location == 'Top Counter'):
                            self.y_change = -1 * PLAYER_SPEED
                            self.facing = 'up'
                            self.prev_dest_y = self.dest_y
                        elif(self.prev_dest_y % TILE_SIZE != 0 and (self.dest_y > self.prev_dest_y)):
                        # elif(self.location == 'Bottom Counter'):
                            self.y_change = PLAYER_SPEED
                            self.facing = 'down'
                        elif(self.dest_y == self.rect.y):
                            if(self.dest_x > self.rect.x):
                                self.x_change = PLAYER_SPEED
                                self.facing = 'right'
                            elif(self.dest_x < self.rect.x):
                                self.x_change = -1 * PLAYER_SPEED
                                self.facing = 'left'
                        else:
                            if(self.facing == 'right'):
                                self.x_change = PLAYER_SPEED
                                self.facing = 'right'
                                # print('it here 1')
                            elif(self.facing == 'left'):
                                self.x_change = -1 * PLAYER_SPEED
                                self.facing = 'left'
                            elif(self.facing == 'up'):
                                self.y_change = -1 * PLAYER_SPEED
                                self.facing = 'up'
                            elif(self.facing == 'down'):
                                self.y_change = PLAYER_SPEED
                                self.facing = 'down'
                    elif ((self.rect.x % TILE_SIZE == 0) and (self.rect.y % TILE_SIZE == 0 or self.rect.y == self.dest_y)):
                        # compute new direction
                        # print('compute new direction')
                        # print(self.rect.x, self.rect.y, self.dest_x, self.dest_y)
                        if(self.rect.x != self.dest_x and self.rect.y == self.dest_y):
                            # print('x not equal else here')
                            if(self.rect.x > self.dest_x):
                                self.prev_facing = self.facing
                                self.x_change = -1 * PLAYER_SPEED
                                self.facing = 'left'
                            else:
                                self.prev_facing = self.facing
                                self.x_change = PLAYER_SPEED
                                self.facing = 'right'
                                # print('it here 2')
                        elif(self.rect.x == self.dest_x and self.rect.y != self.dest_y):
                            # print('y not equal else here')
                            if(self.rect.y > self.dest_y):
                                self.prev_facing = self.facing
                                self.y_change = -1 * PLAYER_SPEED
                                self.facing = 'up'
                            else:
                                self.prev_facing = self.facing
                                self.y_change = PLAYER_SPEED
                                self.facing = 'down'
                        elif(self.rect.x != self.dest_x and self.rect.y != self.dest_y):  
                            new_dir = random.choice([0,1])
                            # print('randomly generate new direction')
                            if(new_dir == 0):
                                # print('x dir')
                                if(self.rect.x > self.dest_x):
                                    self.prev_facing = self.facing
                                    self.x_change = -1 * PLAYER_SPEED
                                    self.facing = 'left'
                                else:
                                    self.prev_facing = self.facing
                                    self.x_change = PLAYER_SPEED
                                    self.facing = 'right'
                                    # print('it here 3')
                            else:
                                # print('y dir')
                                if(self.rect.y > self.dest_y):
                                    self.prev_facing = self.facing
                                    self.y_change = -1 * PLAYER_SPEED
                                    self.facing = 'up'
                                else:
                                    self.prev_facing = self.facing
                                    self.y_change = PLAYER_SPEED
                                    self.facing = 'down'


    def user_action(self):
        # get all keys that have been pressed
        if(self.location is not None):
            # events = pygame.event.get()
            # print(events)
            # for event in events:
                # if event.type == pygame.KEYDOWN:    # check if a key press occurs in that frame
            keys = pygame.key.get_pressed()
            # if keys[pygame.K_a]:
            # print('key pressed')
            # print(".:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:.")
            if keys[pygame.K_a]:
                if(self.location is not None):
                    if(self.action is None):
                        self.action = "Speak"
                        self.before = True
            # if keys[pygame.K_u]:
            if keys[pygame.K_u]:
                if(self.location is not None):
                    if(self.action is None):
                        self.action = "Speak"
                        if(self.location == "Plate Station"):
                            self.message = "p"
                        else:
                            self.message = "u"
                        self.before = True
            # if keys[pygame.K_d]:
            if keys[pygame.K_d]:
                if(self.location is not None):
                    if(self.action is None):
                        self.action = "Speak"
                        self.message = "d"
                        self.before = True
            if keys[pygame.K_c]:
                if(self.location == "Chopping Station"):
                    # print(self.action)
                    if(self.action is None):
                        self.action = "Gesture"
                        self.message = "cd"
                        self.before = True
                elif(self.location == "Cooking Station"):
                    if(self.action is None):
                        self.action = "Gesture"
                        self.message = "sd"
                        self.before = True
            if keys[pygame.K_q]:
                if(self.location is not None):
                    if(self.action is not None):
                        self.stop_everything()
                        self.game.client.publish('overcooked_mic'+str(self.client_ID), "Stop", qos=1)
                        self.game.client.publish('overcooked_imu'+str(self.client_ID), "Mic Stop", qos=1)

            # print(self.action)
                    
    def stand_or_walk(self):
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.right_idle[math.floor(self.animation_loop)%IDLE_FRAMES]
                self.image_name = 'right_idle'
                self.animation_loop += 0.1
                if self.animation_loop >= 6:
                    self.animation_loop = 1
            else:
                self.image = self.right_run[math.floor(self.animation_loop)%RUN_FRAMES]
                self.image_name = 'right_run'
                self.animation_loop += 0.1
                if self.animation_loop >= 6:
                    self.animation_loop = 1
        elif self.facing == "up":
            if self.y_change == 0:
                self.image = self.up_idle[math.floor(self.animation_loop)%IDLE_FRAMES]
                self.image_name = 'up_idle'
                self.animation_loop += 0.1
                if self.animation_loop >= 6:
                    self.animation_loop = 1
            else:
                self.image = self.up_run[math.floor(self.animation_loop)%RUN_FRAMES]
                self.image_name = 'up_run'
                self.animation_loop += 0.1
                if self.animation_loop >= 6:
                    self.animation_loop = 1
        elif self.facing == "left":
            if self.x_change == 0:
                self.image = self.left_idle[math.floor(self.animation_loop)%IDLE_FRAMES]
                self.image_name = 'left_idle'
                self.animation_loop += 0.1
                if self.animation_loop >= 6:
                    self.animation_loop = 1
            else:
                self.image = self.left_run[math.floor(self.animation_loop)%RUN_FRAMES]
                self.image_name = 'left_run'
                self.animation_loop += 0.1
                if self.animation_loop >= 6:
                    self.animation_loop = 1
        elif self.facing == "down":
            if self.y_change == 0:
                self.image = self.down_idle[math.floor(self.animation_loop)%IDLE_FRAMES]
                self.image_name = 'down_idle'
                self.animation_loop += 0.1
                if self.animation_loop >= 6:
                    self.animation_loop = 1
            else:
                self.image = self.down_run[math.floor(self.animation_loop)%RUN_FRAMES]
                self.image_name = 'down_run'
                self.animation_loop += 0.1
                if self.animation_loop >= 6:
                    self.animation_loop = 1

    def animate_mic_sequence(self):
        if(self.before):
            # send message to pub 
            if(self.message is not None or self.message is None):
                # uncomment for keyboard:
                self.game.client.publish('overcooked_mic'+str(self.client_ID), self.message, qos=1)
                self.message = None
                # create thinking bubble
                self.before = False
                self.during = True
                # Effects(self, game, spritesheet, x, y, layer, groups, animation_speed, frames, width, height, play, player)
                Effects(self.game,self.game.speaking_animation,self.rect.x,self.rect.y-2*TILE_SIZE,self._layer+1,(self.game.all_sprites),0.2,SPEAK_FRAMES,TILE_SIZE,2*TILE_SIZE,"during",self)
        elif(self.during):
            if(self.message == "Pick Up" or self.message == "Put Down"):
                # kill during animation by setting the boolean to false
                self.during = False
                self.after = True
                self.animation_loop = 1 # set animation loop to beginning frame
                self.action = self.message
                self.message = None
            elif(self.message == "Plate"):
                self.during = False
                self.after = True
                self.animation_loop = 1 # set animation loop to beginning frame
                self.action = "Pick Up"
            else:
                self.stand_or_walk()
        elif(self.after):
            if(self.action == "Pick Up"): 
                if self.facing == 'right':
                    self.image = self.pickup_right[math.floor(self.animation_loop)%PICKUP_FRAMES]
                    self.image_name = 'pickup_right'
                elif self.facing == 'up':
                    self.image = self.pickup_up[math.floor(self.animation_loop)%PICKUP_FRAMES]
                    self.image_name = 'pickup_up'
                elif self.facing == 'left':
                    self.image = self.pickup_left[math.floor(self.animation_loop)%PICKUP_FRAMES]
                    self.image_name = 'pickup_left'
                elif self.facing == 'down':
                    self.image = self.pickup_down[math.floor(self.animation_loop)%PICKUP_FRAMES]
                    self.image_name = 'pickup_down'
                self.animation_loop += 0.1
            
                if self.animation_loop >= PICKUP_FRAMES:
                    self.location_sprite.pickup_item()
                    self.animation_loop = 1
                    self.action = None
                    self.after = False
                    self.message = None
            elif(self.action == "Put Down"):
                if self.facing == 'right':
                    self.image = self.putdown_right[math.floor(self.animation_loop)%PUTDOWN_FRAMES]
                    self.image_name = 'putdown_right'
                elif self.facing == 'up':
                    self.image = self.putdown_up[math.floor(self.animation_loop)%PUTDOWN_FRAMES]
                    self.image_name = 'putdown_up'
                elif self.facing == 'left':
                    self.image = self.putdown_left[math.floor(self.animation_loop)%PUTDOWN_FRAMES]
                    self.image_name = 'putdown_left'
                elif self.facing == 'down':
                    self.image = self.putdown_down[math.floor(self.animation_loop)%PUTDOWN_FRAMES]
                    self.image_name = 'putdown_down'
                self.animation_loop += 0.1
            
                if self.animation_loop >= PUTDOWN_FRAMES:
                    self.location_sprite.place_item()
                    self.animation_loop = 1
                    self.action = None
                    self.after = False
        
    def animate(self):
        # print("action: ")
        # print(self.action)
        # print("----------------")
        # print("location: ")
        # print(self.location)
        # print("----------------")
        if (self.action is None):
            self.stand_or_walk()
        elif(self.action == "Speak" or self.action == "Pick Up" or self.action == "Put Down"):
            if (self.location[-7:] == "Counter"or self.location == "Submit Station"):
                self.animate_mic_sequence()
            if (self.location == "Plate Station"):
                self.animate_mic_sequence()
            elif(self.location == 'Ingredients Stand'):
                if(self.before):
                    # play open fridge animation, pass mic callback
                    # self, game, spritesheet, x, y, layer, groups, animation_speed, frames, width, height, player, play, play_next,call_back):
                    self.before = False
                    AnimateOnce(self.game,self.game.fridge_open_animation,self.location_sprite.x,(self.location_sprite.y-TILE_SIZE),COUNTER_LAYER+1,(self.game.all_sprites),0.1,FRIDGE_OPEN_FRAMES,TILE_SIZE*2,TILE_SIZE*3,self,None,self.send_message)
                elif(self.during):
                    if(self.message == "Tomato" or self.message == "Bun" or self.message == "Lettuce" or self.message == "Meat"):
                        # kill during animation by setting the boolean to false
                        self.location_sprite.pickup_item()
                        self.animation_loop = 1 # set animation loop to beginning frame
                        self.message = None
                        # play close firdge animation 
                        AnimateOnce(self.game,self.game.fridge_close_animation,self.location_sprite.x,(self.location_sprite.y-TILE_SIZE),COUNTER_LAYER+1,(self.game.all_sprites),0.1,FRIDGE_CLOSE_FRAMES,TILE_SIZE*2,TILE_SIZE*3,self,None,None)
                        self.during = False
                        self.after = True
                    else:
                        self.stand_or_walk()
                elif(self.after):
                    # self.stand_or_walk()
                    self.after = False
                    self.action = None

            elif(self.location == 'Chopping Station'):
                self.animate_mic_sequence()
            elif(self.location == 'Cooking Station'):
                self.animate_mic_sequence()

        elif(self.action == "Gesture" or self.action == "Chop" or self.action == "Stir"):
            if(self.location == "Chopping Station"):
                if(self.action == "Gesture"):
                    if(self.before):
                        if(self.message is not None):

                            # uncomment for keyboard:
                            self.game.client.publish('overcooked_mic'+str(self.client_ID), self.message, qos=1)

                            self.before = False
                            self.during = True
                            # self, game, spritesheet, x, y, layer, groups, animation_speed, frames, width, height, which_bool, player
                            Effects(self.game,self.game.knife_animation,self.rect.x,self.rect.y,COUNTER_FRONT_ITEMS_LAYER+TOP_BUN_LAYER+1,self.groups,0.1,CHOP_FRAMES,54,102,'during',self)
                    elif(self.during):
                        self.image = self.chop[math.floor(self.animation_loop)%CHOP_FRAMES]
                        self.image_name = 'chop'
                        self.animation_loop += 0.1
                        
                        if self.animation_loop >= CHOP_FRAMES:
                            self.animation_loop = 1
                        
                        if(self.message == "Chop"):
                            print("I will chop")
                            self.message = None
                            self.location_sprite.chop()
                            # print("chop times" + str(self.location_sprite.items[0].cut_state))

                        if(self.location_sprite.chopped()):
                            self.game.client.publish('overcooked_imu'+str(self.client_ID), "Gesture Complete", qos=1)
                            self.during = False
                            self.action = None

            elif(self.location == "Cooking Station"):
                if(self.action == "Gesture"):
                    if(self.before):
                        if(self.message is not None):

                            # uncomment for keyboard:
                            self.game.client.publish('overcooked_mic'+str(self.client_ID), self.message, qos=1)

                            self.before = False
                            self.during = True
                            # self, game, spritesheet, x, y, layer, groups, animation_speed, frames, width, height, which_bool, player
                            # Effects(self.game,self.game.knife_animation,self.rect.x,self.rect.y,COUNTER_FRONT_ITEMS_LAYER+TOP_BUN_LAYER+1,self.groups,0.1,CHOP_FRAMES,36,68,'during',self)
                    elif(self.during):
                        self.image = self.cook[math.floor(self.animation_loop)%STIR_FRAMES]
                        self.image_name = 'cook'
                        self.animation_loop += 0.1
                        
                        if self.animation_loop >= STIR_FRAMES:
                            self.animation_loop = 1
                        
                        if(self.message == "Stir"):
                            # print(".:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:.")
                            self.message = None
                            self.location_sprite.cook()
                            # print("cook times" + str(self.location_sprite.items[0].cook_state))

                        if(self.location_sprite.cooked()):
                            self.game.client.publish('overcooked_imu'+str(self.client_ID), "Gesture Complete", qos=1)
                            self.during = False
                            self.action = None
                        
                    
    
    def send_message(self):
        # send message to pub 
        # uncomment for keyboard:
        
        if(self.location_sprite.ingredient == 'Tomato'):
            self.game.client.publish('overcooked_mic'+str(self.client_ID), "t", qos=1)
        elif(self.location_sprite.ingredient == 'Bun' or self.location_sprite.ingredient == 'Bun_2'):
            self.game.client.publish('overcooked_mic'+str(self.client_ID), "b", qos=1)
        elif(self.location_sprite.ingredient == 'Lettuce'):
            self.game.client.publish('overcooked_mic'+str(self.client_ID), "l", qos=1)
        elif(self.location_sprite.ingredient == 'Meat' or self.location_sprite.ingredient == 'Meat_2'):
            self.game.client.publish('overcooked_mic'+str(self.client_ID), "m", qos=1)
        
        self.during = True
        Effects(self.game,self.game.speaking_animation,self.rect.x,self.rect.y-2*TILE_SIZE,self._layer+1,(self.game.all_sprites),0.2,SPEAK_FRAMES,TILE_SIZE,2*TILE_SIZE,"during",self)
        self.message = None

        print('done with send message')




        # elif(self.location == "Cooking Station"):
        #     # print("at cookng state")
        #     self.image = self.cook[math.floor(self.animation_loop)]
        #     self.animation_loop += 0.1
        #     if self.animation_loop >= 6:
        #         self.animation_loop = 1

class Cursor(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = COUNTER_FRONT_ITEMS_LAYER

        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.cursor_spritesheet.get_sprite(0,0,0,0,self.width, self.height)
        self.dest_cursor = BackgroundObject(self.game,self.game.cursor_spritesheet,0,0,self.x,self.y,CURSOR_LAYER,self.groups)

        # game, spritesheet, s_x, s_y, x, y, layer, groups
                            
        # self.image.fill((255,255,0,128))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.m = PyMouse()
        # pos = m.position()


    def movement(self, x, y):
        # get all keys that have been pressed
        self.x = x%TILE_SIZE
        self.y = y%TILE_SIZE

    def update(self):
        # x = random.randint(0, WIN_WIDTH)
        # y = random.randint(0, WIN_HEIGHT)
        # self.movement(x, y)

        # # add position change to player 
        x,y = pygame.mouse.get_pos()
        # self.rect.x = x-TILE_SIZE
        # self.rect.y = y
        # print("pymouse coord: " + str(x-TILE_SIZE) + ", " + str(y))

        self.rect.x = ((round(x/TILE_SIZE)-1) * TILE_SIZE)
        self.rect.y = ((round(y/TILE_SIZE)) * TILE_SIZE)

        self.dest_cursor.rect.x = self.game.player.dest_x
        self.dest_cursor.rect.y= (self.game.player.dest_y + TILE_SIZE)
