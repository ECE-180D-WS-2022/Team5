# from matplotlib.pyplot imsport xscale
import pygame
from config import * 
from sprites import *

# class Ingredient(pygame.sprite.Sprite):
#     def __init__(self, game, name, x, y, layer):
#         self.ingredient_name = name

#         self.game = game
#         self.image_sprites = [] 
#         self.x = x
#         self.y = y
#         self.ingredient_layer = 0
        
#         if(self.ingredient_name == "Tomato"):
#             self.cut_state = 0
#             self.cook_state = 0
#             # (self, game, spritesheet, s_x, s_y, x, y, layer, groups):
#             self.image_sprites.append(BackgroundObject(self.game, self.game.tomato_spritesheet,0,0,x,y,layer,self.game.all_sprites))

        
#     def compare(self, ingred2):
#         # Compare two ingredients' by similarity
#         cut = abs(self.cut_state - ingred2.cut_state)
#         cook = abs(self.cook_state - ingred2.cook_state)
#         return cut + cook

class Ingredient(pygame.sprite.Sprite):
    def __init__(self, game, name, x, y, layer):
        self.game = game
        self._layer = layer
        # add player to all_sprites group of game object
        self.groups = (self.game.all_sprites)
        # call init method for inherited class
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.ingredient_name = name

        self.x = x
        self.y = y

        self.image = pygame.Surface([TILE_SIZE,TILE_SIZE])
        self.image.fill(BLACK)
        self.image.set_alpha(0) 


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.image_sprites = []

        # print(self.ingredient_name)

        if(self.ingredient_name == "Tomato"):
            self.spritesheet = self.game.tomato_spritesheet
            self.cut_state = 0
            self.cook_state = 0
            self.states = 2
            self.ingredient_layers = [TOMATO_LAYER]
            self.image_sprites.append(BackgroundObject(self.game,self.spritesheet,0,0,self.x,self.y,self._layer+self.ingredient_layers[0],(self.game.all_sprites)))
            self.score = 20
            print('created tomato')
        elif(self.ingredient_name == "Lettuce"):
            self.spritesheet = self.game.lettuce_spritesheet
            self.cut_state = 0
            self.cook_state = 0
            self.states = 2
            self.ingredient_layers = [LETTUCE_LAYER]
            self.image_sprites.append(BackgroundObject(self.game,self.spritesheet,0,0,self.x,self.y,self._layer+self.ingredient_layers[0],(self.game.all_sprites)))   
            self.score = 20
        elif(self.ingredient_name == "Meat"):
            self.spritesheet = self.game.meat_spritesheet
            self.cut_state = 0
            self.cook_state = 0
            self.states = 3
            self.ingredient_layers = [MEAT_LAYER]
            self.image_sprites.append(BackgroundObject(self.game,self.spritesheet,0,0,self.x,self.y,self._layer+self.ingredient_layers[0],(self.game.all_sprites)))     
            self.score = 30
        elif(self.ingredient_name == "Bun"):
            self.spritesheet = self.game.bun_spritesheet
            self.cut_state = 0
            self.cook_state = STIR_TIMES
            self.states = 1
            self.ingredient_layers = [TOP_BUN_LAYER, BOTTOM_BUN_LAYER]
            self.image_sprites.append(BackgroundObject(self.game,self.spritesheet,0,0,self.x,self.y,self._layer+self.ingredient_layers[0],(self.game.all_sprites)))
            self.image_sprites.append(BackgroundObject(self.game,self.spritesheet,TILE_SIZE,0,self.x,self.y,self._layer+self.ingredient_layers[1],(self.game.all_sprites)))
            self.score = 10
        elif(self.ingredient_name == "Plate"):
            self.spritesheet = self.game.plate_spritesheet
            self.cut_state = 0
            self.cook_state = STIR_TIMES
            self.states = 1
            self.ingredient_layers = [PLATE_LAYER]
            self.image_sprites.append(BackgroundObject(self.game,self.spritesheet,0,0,self.x,self.y,self._layer+self.ingredient_layers[0],(self.game.all_sprites)))
            self.score = 0
            print(".:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:.")
            print('created plate')
        # def __init__(self, game, spritesheet, s_x, s_y, x, y, layer, groups):
        # self.image = self.game.spritesheet.get_sprite(0,0,0,0,self.width,self.height)

    def get_characteristic_attributes(self):
        attributes = [self.ingredient_name, self.x, self.y, 
                      self._layer, self.cut_state, self.cook_state, self.states]
        return attributes
    
    def update_image(self):
        if(self.cut_state > 0):
            state = int(self.cut_state/CHOP_TIMES) + int(self.cook_state/CHOP_TIMES)
            if(state < self.states):
                self.image_sprites[0].image = self.spritesheet.get_sprite(state*self.width,0,0,0,self.width,self.height)
   
    def update(self):
        self.animate()

    def animate(self):
        # print('animate ingredeint')
        for i in range (len(self.image_sprites)):
            self.image_sprites[i].rect.x = self.x
            self.image_sprites[i].rect.y = self.y
            self.image_sprites[i]._layer = self._layer + self.ingredient_layers[i]
            # print(self._layer, self.image_sprites[i]._layer)
            self.game.all_sprites.change_layer(self.image_sprites[i],self.image_sprites[i]._layer)
        if(len(self.image_sprites) == 1):
            self.update_image()
        
        


class Plate:
    # def __init__(self, ID_number):
    def __init__(self, game, name, cut_state, cook_state, x, y, layer, states, spritesheet):
        self.game = game
        self._layer = layer
        # add player to all_sprites group of game object
        self.groups = self.game.all_sprites
        # call init method for inherited class
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y

        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.spritesheet = spritesheet

        self.image = self.game.spritesheet.get_sprite(0,0,0,0,self.width,self.height)

        # hit box of rect and image are the same
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # self.ID_number = ID_number # Identifier
        self.contents = []
        
    def plate_item(self, item):
        item.rect.x = self.rect.x
        item.rect.y = self.rect.y
        self.contents.append(item)
