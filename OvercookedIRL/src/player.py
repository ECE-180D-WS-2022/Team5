import pygame
from config import * 
from ingredients import *
from sprites import *
from animations import *
from counters import *
import math
import random
import speech_recognition as sr 
from pymouse import PyMouse

# Player inherits from pygame.sprite.Sprite (class in pygame module)
class Player(pygame.sprite.Sprite):
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
        self.before = False
        self.during = False
        self.after = False

    def check_set_location(self, hit):
        # print(hit_groups)
        if(self.game.bottom_perspective_counters in hit.groups and self.game.bottom_perspective_counters):
            print(".:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:.")

        if(self.game.ingredients_stands in hit.groups):
            self.location = "Ingredients Stand"
            self.location_sprite = hit
            print(self.location)
        elif(self.game.chopping_stations in hit.groups):
            self.location = "Chopping Station"
            self.location_sprite = hit
            print(self.location)
        elif(self.game.plate_stations in hit.groups):
            self.location = "Plate Station"
            self.location_sprite = hit
            print(self.location)
        elif(self.game.cooking_stations in hit.groups):
            self.location = "Cooking Station"
            self.location_sprite = hit
            print(self.location)
        elif(self.game.submit_stations in hit.groups):
            self.location = "Submit Station"
            self.location_sprite = hit
            print(self.location)
        elif(self.game.top_perspective_counters in hit.groups):
            # if(self.rect.y == self.dest_y and self.)
            self.location = "Top Counter"
            self.location_sprite = hit
            print(self.location)
        elif(self.game.left_counters in hit.groups):
            self.location = "Left Counter"
            self.location_sprite = hit
            print(self.location)
        elif(self.game.right_counters in hit.groups):
            self.location = "Right Counter"
            self.location_sprite = hit
            print(self.location)

    def collide_counters(self, direction):
        # self.location = None
        if direction == "x":
            # checks if the rect of one sprite is inside the rect of another sprite
            # False: do not want to delete sprite upon collision

            hits = pygame.sprite.spritecollide(self, self.game.top_perspective_counters, False)
            if hits:
                print("hits1")
                self.check_set_location(hits[0])
                    
            else: 
                hits = hits = pygame.sprite.spritecollide(self, self.game.bottom_perspective_counters, False)
                if hits:
                    print("hits2")
                    self.check_set_location(hits[0])
                else:
                    hits = pygame.sprite.spritecollide(self, self.game.block_counters, False)
                    if hits:
                        print('block!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        if self.x_change > 0:   # moving right
                            if(abs(self.dest_x-self.rect.x) <= TILE_SIZE and self.rect.y == self.dest_y):
                                self.x_change = 0
                                self.dest_x = self.dest_x - TILE_SIZE
                                self.prev_x =  self.rect.x
                            self.rect.x = hits[0].rect.left - self.rect.width
                            
                        if self.x_change < 0:
                            # print('left here')
                            if(abs(self.dest_x-self.rect.x) <= TILE_SIZE and self.rect.y == self.dest_y):
                                self.x_change = 0
                                self.dest_x = self.dest_x + TILE_SIZE
                                self.prev_x =  self.rect.x
                            self.rect.x = hits[0].rect.right

                        self.check_set_location(hits[0])

                        # print('collide 1')
                        # print(self.dest_x, self.dest_y, self.rect.x, self.rect.y)

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.top_perspective_counters, False)
            if(hits):
                if (pygame.sprite.spritecollide(self, self.game.bottom_perspective_counters, False)):
                    if(self.y_change < 0):
                        if (self.rect.y + self.height < hits[0].rect.bottom):
                            self.rect.y = hits[0].rect.bottom - self.height
                            # self.prev_dest_y = self.dest_y
                            # self.dest_y = self.rect.y
                            self.y_change = 0
                            # print('yahoo2')
                            # print(self.rect.y, self.dest_y)
                    print('collide bottom counter')
                    self.check_set_location(hits[0])
                else:
                    if (self.y_change >= 0): 
                        if (self.rect.y + self.height >= hits[0].rect.top + cover_height):
                            self.rect.y = hits[0].rect.top + cover_height - self.height
                            if (abs(self.dest_y - self.rect.y) < TILE_SIZE):
                                self.prev_dest_y = self.dest_y
                                self.dest_y = self.rect.y
                                self.y_change = 0
                                # print('yahoo')
                                # print(self.rect.y, self.dest_y)
                                # print(self.rect.x, self.dest_x)
                            else:
                                # print('yahpp')
                                # print(self.rect.y, self.dest_y)
                                # print(self.rect.x, self.dest_x)
                                pass
                    else:
                        # if (self.rect.y < hits[0].rect.top):
                        #     self.rect.y = hits[0].rect.top
                        pass

                    self.check_set_location(hits[0])
                            

                self.check_set_location(hits[0])
                # print(self.y_change, self.x_change)

            else:
                hits = pygame.sprite.spritecollide(self, self.game.bottom_perspective_counters, False)
                if (hits):
                    # if(self.y_change < 0):
                    #     if (self.rect.y + self.height < hits[0].rect.bottom):
                    #         self.rect.y = hits[0].rect.bottom - self.height
                    #         # self.prev_dest_y = self.dest_y
                    #         # self.dest_y = self.rect.y
                    #         self.y_change = 0
                    #         # print('yahoo2')
                    #         # print(self.rect.y, self.dest_y)
                    self.check_set_location(hits[0])
                    pass
                    # if(self.y_change < 0):
                    #     if (self.rect.y + self.height < hits[0].rect.bottom):
                    #         self.rect.y = hits[0].rect.bottom - self.height
                    #         # self.prev_dest_y = self.dest_y
                    #         # self.dest_y = self.rect.y
                    #         self.y_change = 0
                    #         # print('yahoo2')
                    #         # print(self.rect.y, self.dest_y)
                    # self.check_set_location(hits[0])

                else:
                    hits = pygame.sprite.spritecollide(self, self.game.block_counters, False)
                    if (hits):
                        # print('block')
                        if self.y_change > 0:   # moving down
                            if (self.rect.y + self.height > hits[0].rect.bottom):
                                self.rect.y = hits[0].rect.bottom - self.height
                                self.prev_dest_y = self.dest_y
                                self.dest_y = self.rect.y
                                self.y_change = 0
                                # print('yahoo3')
                                # print(self.rect.y, self.dest_y)

                        self.check_set_location(hits[0])


    # player's update method called b/c game's update method calls all_sprites.update()
    def update(self):
        self.movement()
        self.user_action()
        self.animate()

        # add position change to player 
        # if(self.x_change != 0):
        #     self.prev_x = self.rect.x
        # if(self.y_change != 0):
        #     self.prev_x = self.rect.y
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
                    if((self.rect.x % 32 != 0 or (self.rect.y % 32 != 0 and self.rect.y != self.dest_y))):
                        # print('continue')
                        # print(self.rect.x, self.rect.y)
                        if(self.prev_dest_y % 32 != 0 and (self.dest_y < self.prev_dest_y)):
                        # if(self.location == 'Top Counter'):
                            self.y_change = -1 * PLAYER_SPEED
                            self.facing = 'up'
                            self.prev_dest_y = self.dest_y
                        elif(self.prev_dest_y % 32 != 0 and (self.dest_y > self.prev_dest_y)):
                        # elif(self.location == 'Bottom Counter'):
                            self.y_change = PLAYER_SPEED
                            self.facing = 'down'
                        elif(self.facing == 'right'):
                            self.x_change = PLAYER_SPEED
                            self.facing = 'right'
                            print('it here 1')
                        elif(self.facing == 'left'):
                            self.x_change = -1 * PLAYER_SPEED
                            self.facing = 'left'
                        elif(self.facing == 'up'):
                            self.y_change = -1 * PLAYER_SPEED
                            self.facing = 'up'
                        elif(self.facing == 'down'):
                            self.y_change = PLAYER_SPEED
                            self.facing = 'down'
                    elif ((self.rect.x % 32 == 0) and (self.rect.y % 32 == 0 or self.rect.y == self.dest_y)):
                        # compute new direction
                        print('compute new direction')
                        print(self.rect.x, self.rect.y, self.dest_x, self.dest_y)
                        if(self.rect.x != self.dest_x and self.rect.y == self.dest_y):
                            print('x not equal else here')
                            if(self.rect.x > self.dest_x):
                                self.prev_facing = self.facing
                                self.x_change = -1 * PLAYER_SPEED
                                self.facing = 'left'
                            else:
                                self.prev_facing = self.facing
                                self.x_change = PLAYER_SPEED
                                self.facing = 'right'
                                print('it here 2')
                        elif(self.rect.x == self.dest_x and self.rect.y != self.dest_y):
                            print('y not equal else here')
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
                            print('randomly generate new direction')
                            if(new_dir == 0):
                                print('x dir')
                                if(self.rect.x > self.dest_x):
                                    self.prev_facing = self.facing
                                    self.x_change = -1 * PLAYER_SPEED
                                    self.facing = 'left'
                                else:
                                    self.prev_facing = self.facing
                                    self.x_change = PLAYER_SPEED
                                    self.facing = 'right'
                                    print('it here 3')
                            else:
                                print('y dir')
                                if(self.rect.y > self.dest_y):
                                    self.prev_facing = self.facing
                                    self.y_change = -1 * PLAYER_SPEED
                                    self.facing = 'up'
                                else:
                                    self.prev_facing = self.facing
                                    self.y_change = PLAYER_SPEED
                                    self.facing = 'down'
                else:
                    print("equal")
                    print(self.location)
                    if (self.location == None):
                        print("3")
                    if(self.location == "Left Counter"):
                        self.facing = 'left'
                    elif(self.location == 'Right Counter'):
                        self.facing = 'right'
                        print('print it here 4')
                    elif(self.location == 'Bottom Counter'):
                        self.facing = 'up'
                    elif(self.location == 'Top Counter'):
                        print('its happening')
                        self.facing = 'down'
                    elif(self.location == 'Chopping Station'):
                        self.facing = 'down'
                    # if (self.prev_x != self.dest_x):
                    #     print(self.prev_x, self.dest_x)
                    # if(self.prev_x < self.dest_x):
                    #     self.facing = 'left'
                    # elif(self.prev_x > self.dest_x):
                    #     self.facing = 'right'
                    # self.prev_x = self.dest_x


            # events = pygame.event.get()
            # if event.type == pygame.MOUSEBUTTONUP:
            #     pos = pygame.mouse.get_pos()

    def user_action(self):
        # get all keys that have been pressed
        if(self.location is not None):
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYUP:    # check if a key press occurs in that frame
                # keys = pygame.key.get_pressed()
                # if keys[pygame.K_a]:
                    print('key pressed')
                    print(".:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:.")
                    if event.key == pygame.K_a:
                        if(self.location is not None):
                            if(self.action is None):
                                self.action = "Speak"
                                self.before = True
                                print('true again')
                    # if keys[pygame.K_u]:
                    if event.key == pygame.K_u:
                        if(self.location is not None):
                            if(self.action is None):
                                self.action = "Speak"
                                if(self.location == "Plate Station"):
                                    self.message = "p"
                                else:
                                    self.message = "u"
                                self.before = True
                    # if keys[pygame.K_d]:
                    if event.key == pygame.K_d:
                        if(self.location is not None):
                            if(self.action is None):
                                self.action = "Speak"
                                self.message = "d"
                                self.before = True
                    if event.key == pygame.K_c:
                        if(self.location == "Chopping Station"):
                            if(self.action is None):
                                self.action = "Gesture"
                                self.message = "c"
                                self.before = True
                        if(self.location == "Cooking Station"):
                            if(self.action is None):
                                self.action = "Gesture"
                                self.message = "s"
                                self.before = True

            print(self.action)
                    
    def stand_or_walk(self):
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.right_idle[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 6:
                    self.animation_loop = 1
            else:
                self.image = self.right_run[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 6:
                    self.animation_loop = 1
        elif self.facing == "up":
            if self.y_change == 0:
                self.image = self.up_idle[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 6:
                    self.animation_loop = 1
            else:
                self.image = self.up_run[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 6:
                    self.animation_loop = 1
        elif self.facing == "left":
            if self.x_change == 0:
                self.image = self.left_idle[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 6:
                    self.animation_loop = 1
            else:
                self.image = self.left_run[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 6:
                    self.animation_loop = 1
        elif self.facing == "down":
            if self.y_change == 0:
                self.image = self.down_idle[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 6:
                    self.animation_loop = 1
            else:
                self.image = self.down_run[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 6:
                    self.animation_loop = 1

    def animate_mic_sequence(self):
        if(self.before):
            # send message to pub 
            if(self.message is not None):
                self.game.client.publish('overcooked_mic', self.message, qos=1)
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
                    self.image = self.pickup_right[math.floor(self.animation_loop)]
                elif self.facing == 'up':
                    self.image = self.pickup_up[math.floor(self.animation_loop)]
                elif self.facing == 'left':
                    self.image = self.pickup_left[math.floor(self.animation_loop)]
                elif self.facing == 'down':
                    self.image = self.pickup_down[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
            
                if self.animation_loop >= PICKUP_FRAMES:
                    self.location_sprite.pickup_item()
                    self.animation_loop = 1
                    self.action = None
                    self.after = False
                    self.message = None
            elif(self.action == "Put Down"):
                if self.facing == 'right':
                    self.image = self.putdown_right[math.floor(self.animation_loop)]
                elif self.facing == 'up':
                    self.image = self.putdown_up[math.floor(self.animation_loop)]
                elif self.facing == 'left':
                    self.image = self.putdown_left[math.floor(self.animation_loop)]
                elif self.facing == 'down':
                    self.image = self.putdown_down[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
            
                if self.animation_loop >= PUTDOWN_FRAMES:
                    self.location_sprite.place_item()
                    self.animation_loop = 1
                    self.action = None
                    self.after = False
        
    def animate(self):
        # print("animate")
        # print(self.location)
        if (self.action is None):
            self.stand_or_walk()
        elif(self.action == "Speak" or self.action == "Pick Up" or self.action == "Put Down"):
            print(self.action)
            print(self.before,self.during,self.after)
            print(self.message)
            print(self.location[-7:])

            if (self.location[-7:] == "Counter"):
                self.animate_mic_sequence()
            if (self.location == "Plate Station"):
                self.animate_mic_sequence()
            elif(self.location == 'Ingredients Stand'):
                print(self.location_sprite.ingredient)
                if(self.before):
                    # play open fridge animation, pass mic callback
                    # self, game, spritesheet, x, y, layer, groups, animation_speed, frames, width, height, player, play, play_next,call_back):
                    self.before = False
                    AnimateOnce(self.game,self.game.fridge_open_animation,self.location_sprite.x,(self.location_sprite.y-TILE_SIZE),COUNTER_LAYER+1,(self.game.all_sprites),0.1,FRIDGE_OPEN_FRAMES,TILE_SIZE*2,TILE_SIZE*3,self,None,self.send_message)
                    print('animate crated')
                elif(self.during):
                    if(self.message is not None):
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
                            self.game.client.publish('overcooked_mic', self.message, qos=1)
                            self.before = False
                            self.during = True
                            # self, game, spritesheet, x, y, layer, groups, animation_speed, frames, width, height, which_bool, player
                            Effects(self.game,self.game.knife_animation,self.rect.x,self.rect.y,COUNTER_FRONT_ITEMS_LAYER+TOP_BUN_LAYER+1,self.groups,0.1,CHOP_FRAMES,36,68,'during',self)
                    elif(self.during):
                        self.image = self.chop[math.floor(self.animation_loop)]
                        self.animation_loop += 0.1
                        
                        if self.animation_loop >= CHOP_FRAMES:
                            self.animation_loop = 1
                        
                        if(self.message == "Chop"):
                            print(".:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:.")
                            self.message = None
                            self.location_sprite.chop()
                            print("chop times" + str(self.location_sprite.items[0].cut_state))

                        if(self.location_sprite.chopped()):
                            self.during = False
                            self.action = None

            elif(self.location == "Cooking Station"):
                if(self.action == "Gesture"):
                    if(self.before):
                        if(self.message is not None):
                            self.game.client.publish('overcooked_mic', self.message, qos=1)
                            self.before = False
                            self.during = True
                            # self, game, spritesheet, x, y, layer, groups, animation_speed, frames, width, height, which_bool, player
                            # Effects(self.game,self.game.knife_animation,self.rect.x,self.rect.y,COUNTER_FRONT_ITEMS_LAYER+TOP_BUN_LAYER+1,self.groups,0.1,CHOP_FRAMES,36,68,'during',self)
                    elif(self.during):
                        self.image = self.cook[math.floor(self.animation_loop)]
                        self.animation_loop += 0.1
                        
                        if self.animation_loop >= STIR_FRAMES:
                            self.animation_loop = 1
                        
                        if(self.message == "Stir"):
                            print(".:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:.")
                            self.message = None
                            self.location_sprite.cook()
                            print("cook times" + str(self.location_sprite.items[0].cook_state))

                        if(self.location_sprite.cooked()):
                            self.during = False
                            self.action = None
                        
                    
    
    def send_message(self):
        # send message to pub 
        if(self.location_sprite.ingredient == 'Tomato'):
            self.game.client.publish('overcooked_mic', "t", qos=1)
        elif(self.location_sprite.ingredient == 'Bun'):
            self.game.client.publish('overcooked_mic', "b", qos=1)
        elif(self.location_sprite.ingredient == 'Lettuce'):
            self.game.client.publish('overcooked_mic', "l", qos=1)
        elif(self.location_sprite.ingredient == 'Meat'):
            self.game.client.publish('overcooked_mic', "m", qos=1)
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
        self.x = x%32
        self.y = y%32

    def update(self):
        # x = random.randint(0, WIN_WIDTH)
        # y = random.randint(0, WIN_HEIGHT)
        # self.movement(x, y)

        # # add position change to player 
        x,y = pygame.mouse.get_pos()
        self.rect.x = x-TILE_SIZE
        self.rect.y = y
        print("pymouse coord: " + str(x-TILE_SIZE) + ", " + str(y))

        self.dest_cursor.rect.x = self.game.player.dest_x
        self.dest_cursor.rect.y= (self.game.player.dest_y + TILE_SIZE)

        