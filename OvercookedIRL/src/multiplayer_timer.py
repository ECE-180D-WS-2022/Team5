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
import datetime
from config import *
from recipe import RecipeCard 
from playground_building_blocks import *
import random

class MultiplayerTimer(pygame.sprite.Sprite):
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
        
    def set_time(self, time_delta):
        '''
        Assumes input is of the type string with format MM:SS
        '''
        t1 = datetime.datetime.strptime(time_delta, "%M:%S")
        t1 = datetime.timedelta(minutes=t1.minute, seconds=t1.second)
        t1 = t1.total_seconds()
        self.timer = t1
        pass

    def update(self):
        # #### DELTA ####
        # server_time = get_unblocked_data(self.game.socket_client)
        # print(server_time)
        # if (type(server_time)==str):
        #     self.game.player.client_ID = int(server_time[10:])
        #     return
        
        # if (server_time != None and server_time[0] == 77):
        #     temp_time = server_time[1]
            
        #     t1 = datetime.datetime.strptime(temp_time, "%M:%S")
        #     t1 = datetime.timedelta(minutes=t1.minute, seconds=t1.second)
            
        #     if (len(self.game.recipes) < 3 and 
        #         t1 < self.temp_time - datetime.timedelta(seconds=30.0)):
        #         self.game.recipes.append(RecipeCard(self.game,3*TILE_SIZE+(len(self.game.recipes))*2*TILE_SIZE,0))
        
        #     self.txt = self.font.render(temp_time, True, self.color)
        #     W = self.txt.get_width()
        #     H = self.txt.get_height()
        #     if (self.min != temp_time[0:2] or self.sec != temp_time[-2:]):
        #         self.image.fill((222,184,135))
        #         self.image.blit(self.txt, [self.width/2 - W/2, self.height/2 - H/2])
            
        #     self.min = temp_time[0:2]
        #     self.sec = temp_time[-2:]
        #     return
        # #### END DELTA ####
        round_timer = int(math.ceil(self.timer))
        min = str(int(round_timer/60))
        sec = str(int(round_timer%60))
        if(int(sec)<10):
            sec = '0'+str(sec)

        # if(self.count%2700 == 0):
        #     if(len(self.game.recipes) < 5):
        #         self.game.recipes.append(RecipeCard(self.game,3*TILE_SIZE+(len(self.game.recipes))*2*TILE_SIZE,0))

        if(self.game.player.client_ID == 0):
            # print(time_left.total_seconds())
            if((self.count-5) % 1200 == 0):
                if(len(self.game.recipes) < 5):                
                    three = (random.randint(1,10) > 5)
                    four = (random.randint(1,10) > 5)
                    self.game.socket_client.send(pickle.dumps([33, three, four]))
                    self.game.recipes.append(RecipeCard(self.game,3*TILE_SIZE+(len(self.game.recipes))*2*TILE_SIZE,0,three,four))
        
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