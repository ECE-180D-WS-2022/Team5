import pygame
from multiplayer_config_48 import *
from ingredients import *
import pickle

class CounterItemsGenerator(pygame.sprite.Sprite):
    def __init__(self, game, groups):
        self.game = game

        # self.groups = self.game.all_sprites#, group
        self.groups = groups
        self.item_copies = []
        
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        counter_items = []
        for counter in self.game.all_counters:
            for item in counter.items:
                useful_attributes = item.get_characteristic_attributes() # length = 7
                counter_items.append(useful_attributes)
        
        message = [22,]
        temp_data = [self.game.player.client_ID, self.game.player.frame, self.game.player.rect.x,self.game.player.rect.y,self.game.player.facing,self.game.player.image_name,self.game.player.animation_loop,self.game.player.action]
        message.append(temp_data)
        message.append(counter_items)
        if self.game.gamemode == "multiplayer":
            self.game.socket_client.send(pickle.dumps(message))

        
    def gen_items(self, recv_items):
        #print('item_copies lne: ' + str(len(self.item_copies)))
        for item in self.item_copies:
            if(item.y != 10 * TILE_SIZE):
                print('deleteing: ' + item.ingredient_name + ' ' + str(self.game.player.frame))
                item.deep_kill()

        self.item_copies = [item for item in self.item_copies if not (item.y != 10 * TILE_SIZE)]
        for item in self.item_copies:
            print('deleteing: ' + item.ingredient_name + ' ' + str(self.game.player.frame))
            item.deep_kill()
            
        self.item_copies.clear()

        for attributes in recv_items:
            # attributes = [self.ingredient_name, self.x, self.y, 
            #   self._layer, self.cut_state, self.cook_state]
            print('creatingL ' + attributes[0])
            item = Ingredient(self.game,attributes[0],
                                     attributes[1],attributes[2],attributes[3])
        
            item.cut_state = attributes[4]
            item.cook_state = attributes[5]
            self.item_copies.append(item)
            # item.groups = (self.game.item_updates)
    
                
            