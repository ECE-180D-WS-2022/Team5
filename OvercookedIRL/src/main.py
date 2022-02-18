import pygame
from sprites import *
from config import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_idle_spritesheet = Spritesheet('../img/amelia_idle_32.png')
        self.character_run_spritesheet = Spritesheet('../img/amelia_run_32.png')
        self.kitchen_spritesheet = Spritesheet('../img/interiors_32.png')

    def createTilemap(self,tilemap):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                if column == "P":
                    Player(self, j, i)
                elif column != ".":
                    Counter(self, j, i, column)

    def new(self):
        # a new game starts
        self.playing = True

        # initialize empty sprite groups
        self.all_sprites = pygame.sprite.LayeredUpdates()   # layered updates object
        self.counters = pygame.sprite.LayeredUpdates()
        self.block_counters = pygame.sprite.LayeredUpdates()
        self.perspective_counters = pygame.sprite.LayeredUpdates()
        self.chopping = pygame.sprite.LayeredUpdates()
        # game, x, y

        self.createTilemap(counter_tilemap)
        Cursor(self,5,2)

    def events(self):
        # game loop events
        for event in pygame.event.get():
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