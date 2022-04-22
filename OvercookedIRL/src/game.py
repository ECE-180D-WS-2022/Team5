from pickle import FALSE
from numpy import False_
import pygame
from sprites import *
from config import *
import sys
from color_mouse import *
import button
import new_button
from input_box import *
import pickle
import pronouncing
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
        self.clicked = False
        self.character_idle_spritesheet = Spritesheet('../img/amelia_idle_32.png')
        self.character_run_spritesheet = Spritesheet('../img/amelia_run_32.png')
        self.kitchen_spritesheet = Spritesheet('../img/interiors_32.png')
        # self.cook_cloud_spritesheet = Spritesheet('../img/cloud_32.png')
        #self.mouse = ColorMouse()


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
        start_button_img = pygame.image.load('Game_Texts/Start_the_game.png').convert_alpha()
        start_button_alt_img = pygame.image.load('Game_Texts/Start_the_game_alt.png').convert_alpha()
        tutorial_button_img = pygame.image.load('Game_Texts/tutorial.png').convert_alpha()
        tutorial_button_alt_img = pygame.image.load('Game_Texts/tutorial_alt.png').convert_alpha()
        title_img = pygame.image.load('Game_Texts/new_title.png').convert_alpha()
        exit_img = pygame.image.load('Game_Texts/exit.png').convert_alpha()
        exit_alt_img = pygame.image.load('Game_Texts/exit_alt.png').convert_alpha()
        exit_button = new_button.Button(exit_img, exit_alt_img, 0.35, WIN_WIDTH, WIN_HEIGHT, False, True, WIN_WIDTH - 80, WIN_HEIGHT-80)
        new_start_button = new_button.Button(start_button_img, start_button_alt_img, 0.45, WIN_WIDTH, WIN_HEIGHT, True, True, 0, -90)
        new_tutorial_button = new_button.Button(tutorial_button_img, tutorial_button_alt_img, 0.45, WIN_WIDTH, WIN_HEIGHT, True, True, 0, 10)
        new_title = new_button.Button(title_img, None, 0.6, WIN_WIDTH, WIN_HEIGHT, True, False, 0, -250)
        while True:
            self.screen.blit(title_screen, (0,0))
            new_title.draw(self.screen)
            if new_start_button.draw(self.screen):
                self.player_input_screen()
            if new_tutorial_button.draw(self.screen):
                self.tutorial_screen_intro()
            if exit_button.draw(self.screen) and self.clicked is True:
                print("exit")
                input("lol")
                pygame.quit()
                sys.exit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True
            pygame.display.update()
            self.clock.tick(FPS)

    def player_input_screen(self):
        player1_txt = font.render("Enter Your Name", True, black)
        input_box1 = InputBox((WIN_WIDTH - player1_txt.get_width()) / 2, WIN_HEIGHT / 7 + 50, 140, 32)
        enter_name_img = pygame.image.load('Game_Texts/enter_name.png').convert_alpha()
        enter_name = new_button.Button(enter_name_img, None, 0.6, WIN_WIDTH, WIN_HEIGHT, True, False, 0, -250)
        back_img = pygame.image.load('Game_Texts/back.png').convert_alpha()
        back_alt_img = pygame.image.load('Game_Texts/back_alt.png').convert_alpha()
        back_button = new_button.Button(back_img, back_alt_img, 0.35, WIN_WIDTH, WIN_HEIGHT, False, True, WIN_WIDTH - 80, WIN_HEIGHT-80)
    
        while True:
            self.screen.blit(title_screen, (0,0))
            enter_name.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                name = input_box1.handle_event(event)
                if name != None:
                    self.register(self.client, name)
                    self.waiting_connection_screen()
            if back_button.draw(self.screen):
                self.intro_screen()
            input_box1.update()
            input_box1.draw(self.screen)
            
            pygame.display.update()
            self.clock.tick(FPS)

    def tutorial_screen_intro(self):
        back_img = pygame.image.load('Game_Texts/back.png').convert_alpha()
        back_alt_img = pygame.image.load('Game_Texts/back_alt.png').convert_alpha()
        back_button = new_button.Button(back_img, back_alt_img, 0.35, WIN_WIDTH, WIN_HEIGHT, False, True, WIN_WIDTH - 80, WIN_HEIGHT-80)
        welcome_2_tut_img = pygame.image.load('Game_Texts/welcome_2_tut.png').convert_alpha()
        welcome_2_tut_button = new_button.Button(welcome_2_tut_img, None, 0.55, WIN_WIDTH, WIN_HEIGHT, True, False, 0, -250)
        gesture_img = pygame.image.load('Game_Texts/gesture.png').convert_alpha()
        gesture_alt_img = pygame.image.load('Game_Texts/gesture_alt.png').convert_alpha()
        gesture_button = new_button.Button(gesture_img, gesture_alt_img, 0.35, WIN_WIDTH, WIN_HEIGHT, False, True, 15, 80)
        controller_img = pygame.image.load('Game_Texts/controller.png').convert_alpha()
        controller_alt_img = pygame.image.load('Game_Texts/controller_alt.png').convert_alpha()
        controller_button = new_button.Button(controller_img, controller_alt_img, 0.35, WIN_WIDTH, WIN_HEIGHT, False, True, 15, 160)
        speech_img = pygame.image.load('Game_Texts/speech.png').convert_alpha()
        speech_alt_img = pygame.image.load('Game_Texts/speech_alt.png').convert_alpha()
        speech_button = new_button.Button(speech_img, speech_alt_img, 0.35, WIN_WIDTH, WIN_HEIGHT, False, True, 15, 240)
        movement_img = pygame.image.load('Game_Texts/movement.png').convert_alpha()
        movement_alt_img = pygame.image.load('Game_Texts/movement_alt.png').convert_alpha()
        movement_button = new_button.Button(movement_img, movement_alt_img, 0.35, WIN_WIDTH, WIN_HEIGHT, False, True, 15, 320)
        
        while True:
            self.screen.blit(title_screen, (0,0))
            welcome_2_tut_button.draw(self.screen)
            if gesture_button.draw(self.screen):
                print("gesture")
            if controller_button.draw(self.screen):
                print("controller")
            if speech_button.draw(self.screen):
                print("speech")
            if movement_button.draw(self.screen):
                print("movement")
            if back_button.draw(self.screen):
                print("back")
                self.intro_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            self.clock.tick(FPS)

    def waiting_connection_screen(self):
        wait_4_all_img = pygame.image.load('Game_Texts/wait_4_all.png').convert_alpha()
        wait_4_all_button = new_button.Button(wait_4_all_img, None, 0.55, WIN_WIDTH, WIN_HEIGHT, True, False, 0, -250)
        ready_img = pygame.image.load('Game_Texts/ready.png').convert_alpha()
        ready_alt_img = pygame.image.load('Game_Texts/ready_alt.png').convert_alpha()
        ready_button = new_button.Button(ready_img, ready_alt_img, 0.45, WIN_WIDTH, WIN_HEIGHT, True, True, 0, -90)
        ready_up_img = pygame.image.load('Game_Texts/ready_up.png').convert_alpha()
        ready_up_button= new_button.Button(ready_up_img, None, 0.55, WIN_WIDTH, WIN_HEIGHT, True, False, 0, -250)
        done = False
        self.client.setblocking(False)
        while not done:
            try: condition = pickle.loads(self.client.recv(self.header))
            except: condition = None
            if (condition != True):
                self.screen.blit(title_screen, (0,0))
                wait_4_all_button.draw(self.screen)
                pygame.draw.rect(self.screen, black, r)
                r.move_ip(5, 0)
            else:
                self.client.setblocking(True)
                while not done:
                    self.screen.blit(title_screen, (0,0))
                    ready_up_button.draw(self.screen)
                    if ready_button.draw(self.screen):
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