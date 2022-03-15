from pickle import FALSE
import pygame
from sprites import *
from config import *
import sys
from color_mouse import *
import button
from input_box import *
import pickle
import threading
pygame.init()
font = pygame.font.SysFont("comicsansms", 40)
smallfont = pygame.font.SysFont("comicsansms", 30)
slategrey = (112, 128, 144)
lightgrey = (165, 175, 185)
blackish = (10, 10, 10)
white = (255, 255, 255)
black = (0, 0, 0)
lightblue = (173,216,230)

title_screen = pygame.image.load("../img/title_background.png")
title_screen = pygame.transform.scale(title_screen, (WIN_WIDTH, WIN_HEIGHT))
r = pygame.rect.Rect((0, WIN_HEIGHT-30, 70, 30))

class Game:
    def __init__(self, client, header):
        pygame.init()
        self.client = client
        self.header = header
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("OvercookedIRL")
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_idle_spritesheet = Spritesheet('../img/amelia_idle_32.png')
        self.character_run_spritesheet = Spritesheet('../img/amelia_run_32.png')
        self.kitchen_spritesheet = Spritesheet('../img/interiors_32.png')
        # self.cook_cloud_spritesheet = Spritesheet('../img/cloud_32.png')
        #self.mouse = ColorMouse()

        self.start_img = pygame.image.load("../img/Start.png")
        self.quit_img = pygame.image.load("../img/Quit.png")
        self.instructions_img = pygame.image.load("../img/Instructions.png")
        self.title_img = pygame.image.load("../img/Title.png")

        self.start_button = button.Button(100, 200, self.start_img, 0.8)
        self.quit_img = button.Button(450, 200, self.quit_img, 0.8)

    def createTilemap(self,tilemap):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                # if column == "P":
                #     Player(self, j, i)
                if column != "." and column != "P":
                    Counter(self, j, i, column)
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
        self.chopping = pygame.sprite.LayeredUpdates()
        #self.cursor = Cursor(self,5,2)
        self.player = Player(self, 8,8)
        # game, x, y

        self.createTilemap(counter_tilemap)
        # initialize_camera()

        #self.mouse.setupMouse()

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

    # Function to create a button
    def create_button(self, x, y, width, height, hovercolor, defaultcolor):
        mouse = pygame.mouse.get_pos()
        # Mouse get pressed can run without an integer, but needs a 3 or 5 to indicate how many buttons
        click = pygame.mouse.get_pressed(3)
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pygame.draw.rect(self.screen, hovercolor, (x, y, width, height))
            if click[0] == 1:
                return True
        else:
            pygame.draw.rect(self.screen, defaultcolor, (x, y, width, height))

    def intro_screen(self):
        startText = font.render("Overcooked IRL", True, black)
        start_buttontxt = smallfont.render("Start the Game!", True, blackish)
        done = False
        while not done:
            self.screen.blit(title_screen, (0,0))
            self.screen.blit(startText, ((WIN_WIDTH - startText.get_width()) / 2, 0))
            start_button = self.create_button((WIN_WIDTH - start_buttontxt.get_width() - 10) / 2 , (WIN_HEIGHT - 10) / 4, 235, 50, lightgrey, slategrey)
            self.screen.blit(start_buttontxt, ((WIN_WIDTH - start_buttontxt.get_width()) / 2, WIN_HEIGHT / 4))

            if start_button:
                self.player_input_screen()
                done = True
                # while g.running:
                #    g.main()
                #    g.game_over()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            self.clock.tick(FPS)

    def player_input_screen(self):
        player1_txt = font.render("Enter Your Name", True, black)
        input_box1 = InputBox((WIN_WIDTH - player1_txt.get_width()) / 2, WIN_HEIGHT / 8, 140, 32)
        done = False
        while not done:
            self.screen.blit(title_screen, (0,0))
            self.screen.blit(player1_txt, ((WIN_WIDTH - player1_txt.get_width()) / 2, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                name = input_box1.handle_event(event)
                if name != None:
                    self.register(self.client, name)
                    self.waiting_connection_screen()
                    done = True
            input_box1.update()
            input_box1.draw(self.screen)
            
            pygame.display.update()
            self.clock.tick(FPS)

    def waiting_connection_screen(self):
        waiting_txt = font.render("Waiting For Players To Connect", True, black)
        readyup_txt = font.render("Ready Up!", True, black)
        ready_buttontxt = smallfont.render("Ready!", True, blackish)
        done = False
        self.client.setblocking(False)
        while not done:
            try: condition = pickle.loads(self.client.recv(self.header))
            except: condition = None

            if (condition != True):
                self.screen.blit(title_screen, (0,0))
                self.screen.blit(waiting_txt, ((WIN_WIDTH - waiting_txt.get_width()) / 2, 0))
                pygame.draw.rect(self.screen, black, r)
                r.move_ip(5, 0)
            else:
                self.client.setblocking(True)
                while not done:
                    self.screen.blit(title_screen, (0,0))
                    self.screen.blit(readyup_txt, ((WIN_WIDTH - readyup_txt.get_width()) / 2, 0))
                    ready_button = self.create_button((WIN_WIDTH - ready_buttontxt.get_width() - 10) / 2 , (WIN_HEIGHT - 10) / 4, 100, 50, lightgrey, slategrey)
                    self.screen.blit(ready_buttontxt, ((WIN_WIDTH - ready_buttontxt.get_width()) / 2, WIN_HEIGHT / 4))
                    if ready_button:
                        done = True
                        self.client.send(pickle.dumps([1])) # Send ready signal to game server
                        ready_condition = pickle.loads(self.client.recv(self.header))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    pygame.display.update()
                    self.clock.tick(FPS)
            if not self.screen.get_rect().contains(r):
                r.x = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            self.clock.tick(FPS)

    def register(self,client_socket, name): # ACTION = 0
        client_socket.send(pickle.dumps([0, name])) # Send information to be stored