import pygame
from multiplayer_config import * 
import math
import random

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, b_x, b_y, width, height):
        sprite = pygame.Surface([width,height])
        sprite.blit(self.sheet, (b_x,b_y), (x,y,width,height))
        sprite.set_colorkey(BLACK)
        return sprite

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

        self.location = None

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

        self.cook = [self.game.character_chop_spritesheet.get_sprite(0*self.width,0,0,0,self.width, self.height),
                        self.game.character_chop_spritesheet.get_sprite(1*self.width,0,0,0,self.width, self.height),
                        self.game.character_chop_spritesheet.get_sprite(2*self.width,0,0,0,self.width, self.height),
                        self.game.character_chop_spritesheet.get_sprite(3*self.width,0,0,0,self.width, self.height),
                        self.game.character_chop_spritesheet.get_sprite(4*self.width,0,0,0,self.width, self.height),
                        self.game.character_chop_spritesheet.get_sprite(5*self.width,0,0,0,self.width, self.height)]

    def collide_counters(self, direction):
        # self.location = None
        if direction == "x":
            # checks if the rect of one sprite is inside the rect of another sprite
            # False: do not want to delete sprite upon collision
            hits = pygame.sprite.spritecollide(self, self.game.block_counters, False)
            if hits:
                if self.x_change > 0:   # moving right
                    self.rect.x = hits[0].rect.left - self.rect.width
                    if(abs(self.dest_x-self.rect.x) <= 32 and abs(self.dest_y-self.rect.y) <= 32):
                        self.x_change = 0
                        if(self.dest_y == self.rect.y):
                            if(self.dest_x > self.rect.x):
                                self.facing = 'right'
                            else:
                                self.facing = 'left'
                        else:
                            if(self.dest_y > self.rect.y):
                                self.facing = 'down'
                            else:
                                self.facing = 'up'
                        self.dest_x = self.rect.x
                        self.dest_y = self.rect.y
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    if(abs(self.dest_x-self.rect.x) <= 32 and abs(self.dest_y-self.rect.y) <= 32):
                        self.x_change = 0
                        if(self.dest_y == self.rect.y):
                            if(self.dest_x > self.rect.x):
                                self.facing = 'right'
                            else:
                                self.facing = 'left'
                        else:
                            if(self.dest_y > self.rect.y):
                                self.facing = 'down'
                            else:
                                self.facing = 'up'
                        self.dest_x = self.rect.x
                        self.dest_y = self.rect.y

                print(hits[0].groups)
                if(self.game.ingredients_stands in hits[0].groups):
                    self.location = "Ingredients Stand"
                    print(self.location)
                elif(self.game.chopping_stations in hits[0].groups):
                    self.location = "Chopping Station"
                    print(self.location)
                elif(self.game.plate_stations in hits[0].groups):
                    self.location = "Plate Station"
                    print(self.location)
                elif(self.game.cooking_stations in hits[0].groups):
                    self.location = "Cooking Station"
                    print(self.location)
                elif(self.game.submit_stations in hits[0].groups):
                    self.location = "Submit Station"
                    print(self.location)
                print('collide 1')
                print(self.dest_x, self.dest_y, self.rect.x, self.rect.y)

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.block_counters, False)
            if (hits):
                if self.y_change > 0:   # moving down
                    self.rect.y = hits[0].rect.top - self.rect.height
                    if(abs(self.dest_x-self.rect.x) <= 32 and abs(self.dest_y-self.rect.y) <= 32):
                        self.y_change = 0
                        if(self.dest_y == self.rect.y):
                            if(self.dest_x > self.rect.x):
                                self.facing = 'right'
                            else:
                                self.facing = 'left'
                        else:
                            if(self.dest_y > self.rect.y):
                                self.facing = 'down'
                            else:
                                self.facing = 'up'
                        self.dest_x = self.rect.x
                        self.dest_y = self.rect.y
                    
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    if(abs(self.dest_x-self.rect.x) <= 32 and abs(self.dest_y-self.rect.y) <= 32):
                        self.y_change = 0
                        if(self.dest_y == self.rect.y):
                            if(self.dest_x > self.rect.x):
                                self.facing = 'right'
                            else:
                                self.facing = 'left'
                        else:
                            if(self.dest_y > self.rect.y):
                                self.facing = 'down'
                            else:
                                self.facing = 'up'
                        self.dest_x = self.rect.x
                        self.dest_y = self.rect.y
                print('collide block')
                if(self.game.ingredients_stands in hits[0].groups):
                    self.location = "Ingredients Stand"
                    print(self.location)
                elif(self.game.chopping_stations in hits[0].groups):
                    self.location = "Chopping Station"
                    print(self.location)
                elif(self.game.plate_stations in hits[0].groups):
                    self.location = "Plate Station"
                    print(self.location)
                elif(self.game.cooking_stations in hits[0].groups):
                    self.location = "Cooking Station"
                    print(self.location)
                elif(self.game.submit_stations in hits[0].groups):
                    self.location = "Submit Station"
                    print(self.location)

            else:
                hits = pygame.sprite.spritecollide(self, self.game.top_perspective_counters, False)
                if(hits):
                    # if self.y_change > 0:   # moving down
                    #     if(hits[0].rect.bottom - (self.rect.y + self.height) < 7):
                    #         self.rect.y = hits[0].rect.bottom - (self.height + 7)
                    if self.y_change < 0:
                        if(hits[0].rect.bottom - (self.rect.y) > 18):
                            self.rect.y = hits[0].rect.bottom - 18
                        if(abs(self.dest_x-self.rect.x) <= 32 and abs(self.dest_y-self.rect.y) <= 32):
                            self.y_change = 0
                            if(self.dest_y == self.rect.y):
                                if(self.dest_x > self.rect.x):
                                    self.facing = 'right'
                                else:
                                    self.facing = 'left'
                            else:
                                if(self.dest_y > self.rect.y):
                                    self.facing = 'down'
                                else:
                                    self.facing = 'up'
                            self.dest_x = self.rect.x
                            self.dest_y = self.rect.y
                    print('collide top')
                else:
                    hits = pygame.sprite.spritecollide(self, self.game.bottom_perspective_counters, False)
                    if (hits):
                        
                        # if self.y_change > 0:   # moving down
                        #     if(self.rect.y - hits[0].rect.top < 1):
                        #         self.rect.y = hits[0].rect.top - self.rect.height
                        if self.y_change < 0:  # moving up
                            if(hits[0].rect.bottom - (self.rect.y + self.height)> 15):
                                self.rect.y = hits[0].rect.top + 17
                            # if (abs(self.dest_x-self.rect.x) <= 32 and abs(self.dest_y-self.rect.y) <= 32):
                            #     self.y_change = 0
                            #     if(self.dest_y == self.rect.y):
                            #         if(self.dest_x > self.rect.x):
                            #             self.facing = 'right'
                            #         else:
                            #             self.facing = 'left'
                            #     else:
                            #         if(self.dest_y > self.rect.y):
                            #             self.facing = 'down'
                            #         else:
                            #             self.facing = 'up'
                            #     self.dest_x = self.rect.x
                            #     self.dest_y = self.rect.y
                            print('collide 4')
                    else:
                        pass  


    # player's update method called b/c game's update method calls all_sprites.update()
    def update(self):
        self.movement()
        self.animate()

        # add position change to player 
        self.rect.x += self.x_change
        self.collide_counters("x")
        self.rect.y += self.y_change
        self.collide_counters("y")

        # print(self.x_change)
        # print(self.rect.x)

        self.y_change = 0
        self.x_change = 0

        # print(self.rect.x, self.rect.y)


    def movement(self):
        # get all keys that have been pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change = -1 * PLAYER_SPEED
            self.facing = 'left'
            self.location = None
        if keys[pygame.K_RIGHT]:
            self.x_change = PLAYER_SPEED
            self.facing = 'right'
            self.location = None
        if keys[pygame.K_UP]:
            self.y_change = -1 * PLAYER_SPEED
            self.facing = 'up'
            self.location = None
        if keys[pygame.K_DOWN]:
            self.y_change = PLAYER_SPEED
            self.facing = 'down'
            self.location = None
        else:
            if(self.rect.x % 32 != 0 or self.rect.y % 32 != 0):
                print('continue')
                if(self.facing == 'right'):
                    self.x_change = PLAYER_SPEED
                    self.facing = 'right'
                    self.location = None
                elif(self.facing == 'left'):
                    self.x_change = -1 * PLAYER_SPEED
                    self.facing = 'left'
                    self.location = None
                elif(self.facing == 'up'):
                    self.y_change = -1 * PLAYER_SPEED
                    self.facing = 'up'
                    self.location = None
                elif(self.facing == 'down'):
                    self.y_change = PLAYER_SPEED
                    self.facing = 'down'
                    self.location = None
            elif (self.rect.x % 32 == 0 and self.rect.y % 32 == 0):
                # compute new direction
                # print(self.rect.x, self.rect.y, self.dest_x, self.dest_y)
                if(self.rect.x != self.dest_x and self.rect.y == self.dest_y):
                    print('x not equal else here')
                    if(self.rect.x > self.dest_x):
                        self.prev_facing = self.facing
                        self.x_change = -1 * PLAYER_SPEED
                        self.facing = 'left'
                        self.location = None
                    else:
                        self.prev_facing = self.facing
                        self.x_change = PLAYER_SPEED
                        self.facing = 'right'
                        self.location = None
                elif(self.rect.x == self.dest_x and self.rect.y != self.dest_y):
                    print('y not equal else here')
                    if(self.rect.y > self.dest_y):
                        self.prev_facing = self.facing
                        self.y_change = -1 * PLAYER_SPEED
                        self.facing = 'up'
                        self.location = None
                    else:
                        self.prev_facing = self.facing
                        self.y_change = PLAYER_SPEED
                        self.facing = 'down'
                        self.location = None
                elif(self.rect.x != self.dest_x and self.rect.y != self.dest_y):  
                    new_dir = random.choice([0,1])
                    print('randomly generate new direction')
                    if(new_dir == 0):
                        print('x dir')
                        if(self.rect.x > self.dest_x):
                            self.prev_facing = self.facing
                            self.x_change = -1 * PLAYER_SPEED
                            self.facing = 'left'
                            self.location = None
                        else:
                            self.prev_facing = self.facing
                            self.x_change = PLAYER_SPEED
                            self.facing = 'right'
                            self.location = None
                    else:
                        print('y dir')
                        if(self.rect.y > self.dest_y):
                            self.prev_facing = self.facing
                            self.y_change = -1 * PLAYER_SPEED
                            self.facing = 'up'
                            self.location = None
                        else:
                            self.prev_facing = self.facing
                            self.y_change = PLAYER_SPEED
                            self.facing = 'down'
                            self.location = None

        # events = pygame.event.get()
        # if event.type == pygame.MOUSEBUTTONUP:
        #     pos = pygame.mouse.get_pos()

    def action(self):
        # get all keys that have been pressed
        keys = pygame.key.get_pressed()
        if(self.location == "Cooking Station"):
            if keys[pygame.K_g]:
                self.gesture = True
            if keys[pygame.K_b]:
                if(self.gesture):
                    pass
                    
        
    def animate(self):
        print("animate")
        print(self.location)
        if (self.location is None):
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
        elif(self.location == "Cooking Station"):
            print("at cookng state")
            self.image = self.cook[math.floor(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop >= 6:
                self.animation_loop = 1

class Counter(pygame.sprite.Sprite):
    def __init__(self, game, sprite_sheet, s_x, s_y, x, y, groups):

    # (self, game, sprite_sheet, s_x, s_y, x, y, layer, groups)

        self.game = game
        self._layer = COUNTER_LAYER
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = sprite_sheet.get_sprite(s_x, s_y,0,0,self.width,self.height)
        self.groups = groups

        # if(type == "E"):
        #     self.groups = self.game.all_sprites, self.game.counters, self.game.bottom_perspective_counters
        #     self.image = self.game.kitchen_spritesheet.get_sprite(green_counter[type][0],green_counter[type][1],0,0,self.width,self.height)
        # elif (type == "L"):
        #     self.groups = self.game.all_sprites, self.game.counters, self.game.top_perspective_counters
        #     self.image = self.game.kitchen_spritesheet.get_sprite(green_counter[type][0],green_counter[type][1],0,0,self.width,self.height)
        # else:
        #     self.groups = self.game.all_sprites, self.game.counters, self.game.block_counters
        #     self.image = self.game.kitchen_spritesheet.get_sprite(green_counter[type][0],green_counter[type][1],0,0,self.width,self.height)

        pygame.sprite.Sprite.__init__(self, self.groups)
        
        # self.image = pygame.Surface([self.width,self.height])
        # self.image.fill((0,0,255))

        # x, y, b_x, b_y, width, height        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Cursor(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = CURSOR_LAYER

        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((255,255,0,128))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def movement(self, x, y):
        # get all keys that have been pressed
        self.x = x%32
        self.y = y%32

    def update(self):
        x = random.randint(0, WIN_WIDTH)
        y = random.randint(0, WIN_HEIGHT)
        self.movement(x, y)

        # add position change to player 
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE

# class CookEffect(pygame.sprite.Sprite)
class BackgroundObject(pygame.sprite.Sprite):
    def __init__(self, game, sprite_sheet, s_x, s_y, x, y, layer, groups):
        self.game = game
        self._layer = layer
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        # self.groups = self.game.all_sprites#, group
        self.groups = groups
        self.image = sprite_sheet.get_sprite(s_x,s_y,0,0,self.width,self.height)

        pygame.sprite.Sprite.__init__(self, self.groups)
        
        # self.image = pygame.Surface([self.width,self.height])
        # self.image.fill((0,0,255))

        # x, y, b_x, b_y, width, height        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    



