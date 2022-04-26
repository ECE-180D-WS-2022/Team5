import pygame
from sprites import *
from config import *
from ingredients import * 
from sprites import *
from player import *
from counters import *
from timer import *
from score import *
from recipe import *
import sys
from color_mouse import *
import os
import math
# import speech_recognition as sr 
import paho.mqtt.client as mqtt

def on_connect(client,userdata,flags,rc):
    client.subscribe("overcooked_game", qos=1)
    print("connection returned result:" + str(rc))

def on_disconnect(client, userdata, rc):
    if rc != 0: 
        print('Undexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, message):
    print('Received message: "' + str(message.payload) + " on topic " + message.topic + '" with QoS ' + str(message.qos)) 
    # self.speech_log.write(str(message.payload) + "/n")
    print(".:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:.")
    line = str(message.payload)[2:][:-1]
    print(line)
    # userdata.speech_log.write(line + "\n")
    
    # if(str(message.payload) == "b\'" + "tomato" + "\'"):
    #     # client.publish("tomato")
    #     # client.publish('overcooked_mic', 'tomato', qos=1)
    #     print("recieved tomato")

    # if(userdata.player.action is not None):
    #     userdata.player.message = line
    if (line == "Mic Start"):
        if(userdata.player.location is not None):
            if(userdata.player.action is None):
                userdata.client.publish('overcooked_mic', 'Start', qos=1)
                userdata.player.action = "Speak"
                userdata.player.before = True
    elif (line == "Pick Up" or line == "Put Down"):
        if(userdata.player.action is not None):
            userdata.player.message = line
    elif(line == "Gesture"):
        if(userdata.player.location == "Chopping Station" or userdata.player.location == "Cooking Station"):
            if(userdata.player.action is None):
                userdata.player.action = "Gesture"
                userdata.player.message = "Gesture"
                userdata.player.before = True
    elif(line == "Chop" or line == "Stir"):
        userdata.player.message = line
    elif(line == "Mic Stop"):
        userdata.player.stop_everything()
    elif(line == "Tomato" or line == "Bun" or line == "Lettuce" or line == "Meat"):
        userdata.player.message = line
    elif(line == "Plate"):
        # userdata.player.action == "Pick Up"
        userdata.player.message = line
    elif(line == "Stop Gesture"):
        userdata.player.stop_everything()
    else:
        userdata.player.stop_everything()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_idle_spritesheet = Spritesheet('../img/chef1/chef1_idle_32.png')
        self.character_run_spritesheet = Spritesheet('../img/chef1/chef1_run_32.png')
        self.kitchen_spritesheet = Spritesheet('../img/12_Kitchen_32x32.png')
        self.kitchen_shadowless_spritesheet = Spritesheet('../img/12_Kitchen_Shadowless_32x32.png')
        # self.cook_cloud_spritesheet = Spritesheet('../img/cloud_32.png')
        self.character_chop_spritesheet = Spritesheet('../img/chef1/chop_idle.png')
        self.character_stir_spritesheet = Spritesheet('../img/chef1/chef_stir.png')
        self.character_pickup_spritesheet = Spritesheet('../img/chef1/chef1_pickup.png')
        self.character_putdown_spritesheet = Spritesheet('../img/chef1/chef1_place.png')
        self.cursor_spritesheet = Spritesheet('../img/cursor.png')
        self.knife_animation = Spritesheet('../img/chop_knife.png')
        self.plates_stack = Spritesheet('../img/individual_tiles/dish_pile.png')
        self.inventory_spritesheet = Spritesheet('../img/inventory_tile.png')
        self.bun_spritesheet = Spritesheet('../img/recipes/bun_spritesheet.png')
        self.meat_spritesheet = Spritesheet('../img/recipes/meat_spritesheet.png')
        self.tomato_spritesheet = Spritesheet('../img/recipes/tomato_spritesheet.png')
        self.lettuce_spritesheet = Spritesheet('../img/recipes/lettuce_spritesheet.png')
        self.plate_spritesheet = Spritesheet('../img/recipes/plate_spritesheet.png')
        self.progress_spritesheet = Spritesheet('../img/progress_bar.png')
        self.knife_icon = Spritesheet('../img/knife_icon.png')
        self.cook_icon = Spritesheet('../img/cook_icon.png')
        self.speaking_animation = Spritesheet('../img/speaking_animation.png')

        self.fridge_open_animation = Spritesheet('../img/object_animations/fridge_open_spritesheet.png')
        self.fridge_close_animation = Spritesheet('../img/object_animations/fridge_close_spritesheet.png')
        self.recipe_card = Spritesheet('../img/recipe_card.png')

        self.mouse = ColorMouse()

    def createTilemap(self,tilemap,layer):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                # if column == "P":
                #     Player(self, j, i)
                if column == '0':
                    BackgroundObject(self, self.plates_stack, 0, 0, j, i, layer, (self.all_sprites))
                elif column == '!':
                    IngredientsCounter("Tomato",self, self.kitchen_spritesheet,white_counter["!"][0],white_counter["!"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.bottom_perspective_counters,self.ingredients_stands))
                elif column == '^':
                    IngredientsCounter("Lettuce",self, self.kitchen_spritesheet,white_counter["!"][0],white_counter["!"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.bottom_perspective_counters,self.ingredients_stands))
                elif column == '(':
                    IngredientsCounter("Meat",self, self.kitchen_spritesheet,white_counter["!"][0],white_counter["!"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.bottom_perspective_counters,self.ingredients_stands))
                elif column == ')':
                    IngredientsCounter("Bun",self, self.kitchen_spritesheet,white_counter["!"][0],white_counter["!"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.bottom_perspective_counters,self.ingredients_stands))
                elif column == 'E':
                    Counter(self, self.kitchen_spritesheet,white_counter["E"][0],white_counter["E"][1],j,i,layer,(self.all_sprites,self.counters,self.bottom_perspective_counters))
                elif column == '$':
                    ChopCounter(self, self.kitchen_spritesheet,white_counter["B"][0],white_counter["B"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.chopping_stations))
                elif column == '*':
                    IngredientsCounter("Plate",self, self.kitchen_spritesheet,white_counter["H"][0],white_counter["H"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.plate_stations))
                elif column == '%':
                    CookCounter('pan',self, self.kitchen_spritesheet,white_counter["%"][0],white_counter["%"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters,self.bottom_perspective_counters,self.cooking_stations))
                elif column == '&':
                    Counter(self, self.kitchen_spritesheet,white_counter["&"][0],white_counter["&"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.submit_stations))
                elif column == 'B':
                    Counter(self, self.kitchen_spritesheet,white_counter["B"][0],white_counter["B"][1],j,i,layer,(self.all_sprites,self.counters,self.top_perspective_counters))
                elif column == 'J':
                    Counter(self, self.kitchen_spritesheet,white_counter["J"][0],white_counter["J"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.bottom_perspective_counters))
                elif column == 'G':
                    Counter(self, self.kitchen_spritesheet,white_counter["G"][0],white_counter["G"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.left_counters))
                elif column == 'H':
                    Counter(self, self.kitchen_spritesheet,white_counter["H"][0],white_counter["H"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.right_counters))
                elif column == 'H':
                    Counter(self, self.kitchen_spritesheet,white_counter["H"][0],white_counter["H"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.right_counters))
                elif column == 'V':
                    BackgroundObject(self,self.inventory_spritesheet,0,0,j,i,layer,(self.all_sprites))             
                elif column == 'S':
                    Counter(self, self.kitchen_spritesheet,white_counter["S"][0],white_counter["S"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.bottom_perspective_counters))
                elif column == 'M':
                    SubmitStation(self, self.kitchen_spritesheet,white_counter["G"][0],white_counter["G"][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters,self.left_counters,self.submit_stations))
                elif column == 'Z':
                    BackgroundObject(self,self.kitchen_shadowless_spritesheet,front_items["Z"][0],front_items["Z"][1],j,i,layer,(self.all_sprites))   
                elif column == 'U':
                    BackgroundObject(self,self.kitchen_shadowless_spritesheet,front_items["U"][0],front_items["U"][1],j,i,layer,(self.all_sprites))   
                elif column == 'Y':
                    BackgroundObject(self,self.kitchen_shadowless_spritesheet,front_items["Y"][0],front_items["Y"][1],j,i,layer,(self.all_sprites))   
                elif column == 'W':
                    BackgroundObject(self,self.kitchen_shadowless_spritesheet,back_items["W"][0],back_items["W"][1],j,i,layer,(self.all_sprites))   
                elif column == 'X':
                    BackgroundObject(self,self.kitchen_shadowless_spritesheet,back_items["X"][0],back_items["X"][1],j,i,layer,(self.all_sprites))   
                elif column != "." and column != "P":
                    # self, self.kitchen_spritesheet,white_counter["G"][0],white_counter["G"][1],j,i,(self.all_sprites,self.counters,self.block_counters,self.ingredients_stands)
                    Counter(self, self.kitchen_spritesheet,white_counter[column][0],white_counter[column][1],j,i,layer,(self.all_sprites,self.counters,self.block_counters))
                    # self.image = self.game.kitchen_spritesheet.get_sprite(white_counter[type][0],white_counter[type][1],0,0,self.width,self.height)
        # print('created tilemap')

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
        self.left_counters = pygame.sprite.LayeredUpdates()
        self.right_counters = pygame.sprite.LayeredUpdates()
        self.cursor = Cursor(self,8,9)
        self.player = Player(self,10,11)
        self.timer = Timer(self,17,0,780,FPS)
        self.score = Score(self,0,0)
        self.recipes = [RecipeCard(self,3*TILE_SIZE,0)]
        # game, x, y

        self.animations = pygame.sprite.LayeredUpdates()


        self.createTilemap(counter_tilemap_back,COUNTER_BACK_LAYER)
        self.createTilemap(counter_tilemap_back_items,COUNTER_BACK_ITEMS_LAYER)
        self.createTilemap(counter_tilemap,COUNTER_LAYER)
        self.createTilemap(counter_tilemap_2,COUNTER_FRONT_LAYER)
        self.createTilemap(counter_front_items_tilemap,COUNTER_FRONT_LAYER+1)
        # self.createTilemap(foreground_tilemap,FOREGROUND_LAYER)
        # initialize_camera()

        ProgressBar(self, self.progress_spritesheet, 0*TILE_SIZE, 4*TILE_SIZE, COUNTER_LAYER, (self.all_sprites), 3*TILE_SIZE, TILE_SIZE, self.player)
        self.mouse.setupMouse()

        # self.setup_audiofile()
        self.setup_mqtt()

    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.player.dest_x = ((round(pos[0]/32)-1) * 32)
                self.player.dest_y = ((round(pos[1]/32)-1) * 32)
                if(self.player.action is not None):
                    self.client.publish('overcooked_mic', "Stop", qos=1)
                    self.client.publish('overcooked_imu', "Mic Stop", qos=1)
                    self.player.stop_everything()

                print('CLICK')
                # print(int(pos[0]/32) * 32, int(pos[1]/32) * 32)
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

    def setup_audiofile(self):
        i = 0
        while os.path.exists("speech%s.txt" % i):
            i += 1
        self.speech_log = open("speech" + str(i) + ".txt", "a")
        # self.r = sr.Recognizer()

    def setup_mqtt(self):
        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        self.client.on_message = on_message
        self.client.user_data_set(self)

        self.client.connect_async("test.mosquitto.org")
        self.client.connect("test.mosquitto.org", 1883, 60)
        self.client.loop_start()
        # self.client.publish('overcooked_mic', "t", qos=1)

    def main(self):
        font = pygame.font.Font(None,40)
        gray = pygame.Color('gray19')
        blue = pygame.Color('dodgerblue')
        timer = 120
        clock = pygame.time.Clock()
        dt = 0
        # game loop
        while self.playing:
        # if(self.playing):
            # self.mouse.mouseMovement()
            self.events()
            self.update()
            self.draw()
            # round_timer = int(math.ceil(timer))
            # min = str(int(round_timer/60))
            # sec = str(int(round_timer%60))
            # if(int(sec)<10):
            #     sec = '0'+str(sec)
            
            # txt = font.render(min+':'+sec, True, blue)
            # self.screen.blit(txt, (70, 70))
            # pygame.display.flip()
            # dt = clock.tick(30) / 1000  # / 1000 to convert to seconds.

            # if int(sec) == 0 and int(min) == 0:
            #     done = True
            # else:
            #     timer -= dt
        self.client.publish('overcooked_mic', "stop", qos=1)
        self.client.loop_stop()
        self.client.disconnect()
        # self.speech_log.close()
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