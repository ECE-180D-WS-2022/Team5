from lib2to3.pgen2.token import TILDE
import pygame
from multiplayer_config import * 
from ingredients import *
import random

class RecipeCard(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = COUNTER_LAYER
        self.x = x
        self.y = y
        self.width = 2*TILE_SIZE
        self.height = 2*TILE_SIZE

        self.groups = self.game.all_sprites#, group
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.image = self.game.recipe_card.get_sprite(0,0,0,0,self.width,self.height)
        self.image_sprites = []

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.ingredient_1 = Ingredient(self.game,"Bun",self.rect.x,self.rect.y,self.layer)
        self.ingredient_2 = Ingredient(self.game,"Meat",self.rect.x+TILE_SIZE,self.rect.y,self.layer)
        self.ingredient_2.cut_state = 3
        self.ingredient_2.cook_state = 3
        self.ingredient_3 = None
        self.ingredient_4 = None

        if(random.randint(1,10) > 5):
            self.ingredient_3 = Ingredient(self.game,"Lettuce",self.rect.x,self.rect.y+TILE_SIZE,self.layer)
            self.ingredient_3.cut_state = 3

        if(random.randint(1,10) > 5):
            self.ingredient_4 = Ingredient(self.game,"Tomato",self.rect.x,self.rect.y+TILE_SIZE,self.layer)
            self.ingredient_4.cut_state = 3

    def update(self):
        self.rect.x = self.x
        self.ingredient_1.x = self.x
        self.ingredient_2.x = self.x + TILE_SIZE
        if(self.ingredient_3 != None):
            self.ingredient_3.x = self.x
        if(self.ingredient_4 != None):
            self.ingredient_4.x = self.x + TILE_SIZE