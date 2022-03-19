import pygame
from config import * 
import math
# from ingredients import *
# from sprites import *
# from counters import *
# from player import *

class AnimateOnce(pygame.sprite.Sprite):
    def __init__(self, game, spritesheet, x, y, layer, groups, animation_speed, frames, width, height, player, play_next,call_back):
        print('at least here')
        self.game = game
        self._layer = layer
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_speed = animation_speed
        self.frames = []
        self.animation_loop = 1
        self.num_frames = frames
        self.player = player
        # self.play = play
        self.play_next = play_next

        # self.groups = self.game.all_sprites#, group
        self.groups = groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        print('at least here 2 ')

        for i in range(frames):
            self.frames.append(spritesheet.get_sprite(i*self.width,0,0,0,self.width,self.height))
        
        self.image = self.frames[0]     

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.call_back = call_back

        print('animate object init')

    def update(self):
        print('animate once update')
        # if not self.play:
        #     print('animate once kill')
        #     self.kill()
        if self.animation_loop >= self.num_frames:
            # self.play = False
            if(self.play_next is not None):
                # mic here
                self.play_next = True
            if (self.call_back is not None):
                print('trying to execute call back')
                self.call_back()
            else:   # part three, action should be solidified
                # if(self.player.action == "Pick Up" and self.player.message == "Pick Up"):
                #     self.player.location_sprite.pickup_item()
                # elif(self.player.action == "Put Down" and self.player.message == "Put Down"):
                #     self.player.location_sprite.pickup_item()
                pass
            print('animate once kill 2')
            self.kill()
        else:
            self.animate()

    def animate(self):
        print('animate once should be playing')
        self.image = self.frames[math.floor(self.animation_loop)]
        self.animation_loop += self.animation_speed
        print('animation loop ' + str(self.animation_loop))
        if self.animation_loop >= self.num_frames:
            pass

class Effects(pygame.sprite.Sprite):
    def __init__(self, game, spritesheet, x, y, layer, groups, animation_speed, frames, width, height, which_bool, player):
        self.game = game
        self._layer = layer
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_speed = animation_speed
        self.frames = []
        self.animation_loop = 1
        self.num_frames = frames
        self.which_bool = which_bool
        self.player = player

        # self.groups = self.game.all_sprites#, group
        self.groups = groups
        pygame.sprite.Sprite.__init__(self, self.groups)

        print('effects here')
        for i in range(frames):
            self.frames.append(spritesheet.get_sprite(i*self.width,0,0,0,self.width,self.height))
        
        self.image = self.frames[0]     
        print('effects here 2')
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        print('effects update')
        # if not self.play:
        kill = False
        if(self.which_bool == 'before'):
            kill = self.player.before
        elif(self.which_bool == 'during'):
            kill = self.player.during
        elif(self.which_bool == 'after'):
            kill = self.player.after
        if(not kill):
            print('killing myself')
            self.kill()
        else:
            self.animate()

    def animate(self):
        print('effects animate')
        self.image = self.frames[math.floor(self.animation_loop)]
        self.animation_loop += self.animation_speed
        if self.animation_loop >= self.num_frames:
            self.animation_loop = 1