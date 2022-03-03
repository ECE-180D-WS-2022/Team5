import pygame
from sprites import *
from config import *
import sys
from color_mouse import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_idle_spritesheet = Spritesheet('../img/amelia_idle_32.png')
        self.character_run_spritesheet = Spritesheet('../img/amelia_run_32.png')
        self.kitchen_spritesheet = Spritesheet('../img/interiors_32.png')
        # self.cook_cloud_spritesheet = Spritesheet('../img/cloud_32.png')
        self.character_chop = Spritesheet('../img/chef_32.png')
        self.plates_stack = Spritesheet('../img/individual_tiles/dish_pile.png')
        self.mouse = ColorMouse()

    def createTilemap(self,tilemap):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                # if column == "P":
                #     Player(self, j, i)
                if column == '0':
                    BackgroundObject(self, self.plates_stack, 0, 0, j, i, COUNTERTOP_LAYER, (self.all_sprites))
                elif column == '!':
                    # (self, game, sprite_sheet, s_x, s_y, x, y, groups):
                    Counter(self, self.kitchen_spritesheet,green_counter["G"][0],green_counter["G"][1],j,i,(self.all_sprites,self.counters,self.block_counters,self.ingredients_stands))
                elif column == '$':
                    Counter(self, self.kitchen_spritesheet,green_counter["H"][0],green_counter["H"][1],j,i,(self.all_sprites,self.counters,self.block_counters,self.chopping_stations))
                elif column == '*':
                    Counter(self, self.kitchen_spritesheet,green_counter["H"][0],green_counter["H"][1],j,i,(self.all_sprites,self.counters,self.block_counters,self.plate_stations))
                elif column == '%':
                    Counter(self, self.kitchen_spritesheet,green_counter["G"][0],green_counter["G"][1],j,i,(self.all_sprites,self.counters,self.block_counters,self.cooking_stations))
                elif column == '&':
                    Counter(self, self.kitchen_spritesheet,green_counter["G"][0],green_counter["G"][1],j,i,(self.all_sprites,self.counters,self.block_counters,self.submit_stations))
                elif column != "." and column != "P":
                    # self, self.kitchen_spritesheet,green_counter["G"][0],green_counter["G"][1],j,i,(self.all_sprites,self.counters,self.block_counters,self.ingredients_stands)
                    Counter(self, self.kitchen_spritesheet,green_counter[column][0],green_counter[column][1],j,i,(self.all_sprites,self.counters,self.block_counters))
                    # self.image = self.game.kitchen_spritesheet.get_sprite(green_counter[type][0],green_counter[type][1],0,0,self.width,self.height)
        print('created tilemap')

    def new(self):
        # a new game starts
        self.playing = True

        # initialize empty sprite groups
        self.all_sprites = pygame.sprite.LayeredUpdates()   # layered updates object
        self.counters = pygame.sprite.LayeredUpdates()
        self.block_counters = pygame.sprite.LayeredUpdates()
        self.bottom_perspective_counters = pygame.sprite.LayeredUpdates()
        self.top_perspective_counters = pygame.sprite.LayeredUpdates()
        self.chopping_stations = pygame.sprite.LayeredUpdates()
        self.plate_stations = pygame.sprite.LayeredUpdates()
        self.ingredients_stands = pygame.sprite.LayeredUpdates()
        self.cooking_stations = pygame.sprite.LayeredUpdates()
        self.submit_stations = pygame.sprite.LayeredUpdates()
        self.cursor = Cursor(self,5,2)
        self.player = Player(self,8,8)
        # game, x, y

        self.createTilemap(counter_tilemap)
        self.createTilemap(counter_tilemap_2)
        # initialize_camera()

        self.mouse.setupMouse()

    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.player.dest_x = (int(pos[0]/32) * 32)
                self.player.dest_y = (int(pos[1]/32) * 32)
                print('CLICK')
                print(int(pos[0]/32) * 32, int(pos[1]/32) * 32)
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        # game loop updates

        # run the update method of every sprite in the all_sprites group
        self.all_sprites.update() 

    def draw(self):
        # game loop draw
        self.screen.fill((0,0,0))

        # draws the image and rect of all sprites in the all_sprites group onto the screen
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        # game loop
        while self.playing:
            # self.mouse.mouseMovement()
            self.events()
            self.update()
            self.draw()

        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()