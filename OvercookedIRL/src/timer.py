'''
import pygame as pg
import math


def main():
    pg.init()
    screen = pg.display.set_mode((640, 480))
    font = pg.font.Font(None, 40)
    gray = pg.Color('gray19')
    blue = pg.Color('dodgerblue')
    # The clock is used to limit the frame rate
    # and returns the time since last tick.
    clock = pg.time.Clock()
    timer = 120  # Decrease this to count down.
    dt = 0  # Delta time (time since last tick).

    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        screen.fill(gray)

        round_timer = int(math.ceil(timer))
        min = str(int(round_timer/60))
        sec = str(int(round_timer%60))
        if(int(sec)<10):
            sec = '0'+str(sec)
        
        txt = font.render(min+':'+sec, True, blue)
        screen.blit(txt, (70, 70))
        pg.display.flip()
        dt = clock.tick(30) / 1000  # / 1000 to convert to seconds.

        if int(sec) == 0 and int(min) == 0:
            done = True
        else:
            timer -= dt


if __name__ == '__main__':
    main()
    pg.quit()
'''
import pygame
import math
from config import *
from recipe import RecipeCard 
from playground_building_blocks import *

class Timer(pygame.sprite.Sprite):
    def __init__(self, game, x, y, timer, fps):
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
        self.txt = self.font.render('', 1, self.color)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255,255,255))
        self.image.blit(self.txt, [self.width/2 - self.txt.get_width()/2, self.height/2 - self.txt.get_height()/2])

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.timer = timer
        self.min = self.timer/60
        self.sec = self.timer%60
        self.fps = fps
        self.count = 1

        # print('background object created')

    def update(self):
        #### DELTA ####
        server_time = get_unblocked_data(self.game.socket_client)
        #### END DELTA ####
        
        
        round_timer = int(math.ceil(self.timer))
        min = str(int(round_timer/60))
        sec = str(int(round_timer%60))
        if(int(sec)<10):
            sec = '0'+str(sec)

        if(self.count%2700 == 0):
            if(len(self.game.recipes) < 5):
                self.game.recipes.append(RecipeCard(self.game,3*TILE_SIZE+(len(self.game.recipes))*2*TILE_SIZE,0))
        
        self.txt = self.font.render(min+':'+sec, True, self.color)

        if int(sec) == 0 and int(min) == 0:
            done = True
            self.game.client.disconnect()
        else:
            self.timer -= (1/60)

        W = self.txt.get_width()
        H = self.txt.get_height()
        if(self.min != min or self.sec != sec): 
            self.image.fill((222,184,135))
            self.image.blit(self.txt, [self.width/2 - W/2, self.height/2 - H/2])
        
        self.min = min
        self.sec = sec
        self.count += 1