import pygame
import math
from multiplayer_config import * 
import pickle

class Score(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = COUNTER_LAYER
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = 3*TILE_SIZE
        self.height = 2*TILE_SIZE

        self.groups = self.game.all_sprites#, group
        # self.groups = groups

        pygame.sprite.Sprite.__init__(self, self.groups)
        self.color = pygame.Color('dodgerblue')
        self.font = pygame.font.SysFont("Arial", 40)
        self.txt = self.font.render('0', 1, self.color)
        self.image = pygame.Surface((self.width, self.height))
        # self.image.fill((255,255,255))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.score = 0

        # print('background object created')

    def update_score(self, num, index):
        self.score += num
        self.txt = self.font.render(str(self.score), True, self.color)
        
        # Edits! 88 -> code for updating score!
        self.game.socket_client.send(pickle.dumps([88, self.score, index]))

        W = self.txt.get_width()
        H = self.txt.get_height()
        self.image.fill((222,184,135))
        self.image.blit(self.txt, [self.width/2 - W/2, self.height/2 - H/2])

    def set_score(self, num):
        self.score = num
        self.txt = self.font.render(str(self.score), True, self.color)

        W = self.txt.get_width()
        H = self.txt.get_height()
        self.image.fill((222,184,135))
        self.image.blit(self.txt, [self.width/2 - W/2, self.height/2 - H/2])

        # self.del_recipe_at_index(index)

    def del_recipe_at_index(self, del_index):
        self.game.recipes[del_index].ingredient_1.deep_kill()
        self.game.recipes[del_index].ingredient_2.deep_kill()
        if(self.game.recipes[del_index].ingredient_3 != None):
            self.game.recipes[del_index].ingredient_3.deep_kill()
        if(self.game.recipes[del_index].ingredient_4 != None):
            self.game.recipes[del_index].ingredient_4.deep_kill()
        self.game.recipes[del_index].kill()
        del self.game.recipes[del_index]
        for i in range(len(self.game.recipes)):
            # if(i > del_index):
            self.game.recipes[i].x = 3*TILE_SIZE + ((i) * 2 * TILE_SIZE)
