import pygame
from multiplayer_config_48 import * 
class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_sprite(self, x, y, b_x, b_y, width, height):
        sprite = pygame.Surface([width,height],pygame.SRCALPHA).convert_alpha()
        sprite.blit(self.sheet, (b_x,b_y), (x,y,width,height))
        sprite.set_colorkey(BLACK)
        return sprite

        # pygame.Surface([width,height]).blit(s,(,),(,,,)).set_colorkey(BLACK)
class BackgroundObject(pygame.sprite.Sprite):
    def __init__(self, game, spritesheet, s_x, s_y, x, y, layer, groups):
        self.game = game
        self._layer = layer
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        # self.groups = self.game.all_sprites#, group
        self.groups = groups
        self.image = spritesheet.get_sprite(s_x,s_y,0,0,self.width,self.height)

        pygame.sprite.Sprite.__init__(self, self.groups)
        
        # self.image = pygame.Surface([self.width,self.height])
        # self.image.fill((0,0,255))

        # x, y, b_x, b_y, width, height        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # print('background object created')

    def update(self):
        # print(self.rect.x, self.rect.y)
        # print("background " + str(self._layer))
        pass

class Inventory(BackgroundObject):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw) 

    def update(self):
        self.animate()

    def animate(self):
        pass
class ProgressBar(pygame.sprite.Sprite):
    def __init__(self, game, spritesheet, x, y, layer, groups, width, height, player):
        self.game = game
        self._layer = layer
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.player = player

        # self.groups = self.game.all_sprites#, group
        self.groups = groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.image = spritesheet.get_sprite(0,0,0,0,self.width,self.height)
        self.image_sprites = []

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()

    def animate(self):
        # print('animate of progress bar.................')
        # print(len(self.image_sprites))
        if(self.player.location == "Chopping Station"):
            if(len(self.player.location_sprite.items) > 0):
                num = min(CHOP_TIMES, self.player.location_sprite.items[0].cut_state)
                curren_len = len(self.image_sprites)
                for n in range (num - curren_len):
                    # print(self.x, curren_len, n)
                    # print('create knife icon' + str(self.x+((curren_len+n)*TILE_SIZE)))
                    # print(".:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:.")
                    self.image_sprites.append(BackgroundObject(self.game,self.game.knife_icon,0,0,(self.x)/TILE_SIZE+((curren_len+n)),self.y/TILE_SIZE,self._layer+1,(self.game.all_sprites)))
            elif(len(self.player.location_sprite.items) == 0):
                for image in self.image_sprites:
                    image.kill()
                self.image_sprites.clear()
        elif(self.player.location == "Cooking Station"):
            if(len(self.player.location_sprite.items) > 0):
                num = min(STIR_TIMES, self.player.location_sprite.items[0].cook_state)
                curren_len = len(self.image_sprites)
                for n in range (num - curren_len):
                    self.image_sprites.append(BackgroundObject(self.game,self.game.cook_icon,0,0,(self.x)/TILE_SIZE+((curren_len+n)),self.y/TILE_SIZE,self._layer+1,(self.game.all_sprites)))
            elif(len(self.player.location_sprite.items) == 0):
                for image in self.image_sprites:
                    image.kill()
                self.image_sprites.clear()
            