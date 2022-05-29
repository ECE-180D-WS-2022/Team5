import pygame
from multiplayer_config import * 
from ingredients import *
from sprites import *
from animations import *
from multiplayer_player import *
import pickle

class MultiplayerCounter(pygame.sprite.Sprite):
    def __init__(self, game, sprite_sheet, s_x, s_y, x, y, layer, groups):

    # (self, game, sprite_sheet, s_x, s_y, x, y, layer, groups)

        self.game = game
        self._layer = layer
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = sprite_sheet.get_sprite(s_x, s_y,0,0,self.width,self.height)
        self.groups = groups

        pygame.sprite.Sprite.__init__(self, self.groups)       

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.items = []

    def player_has_plate(self):
        plate = False   # check if the player's inventory has a plate
        for item in self.game.player.inventory:
            if item.ingredient_name == 'Plate':
                plate = True
        return plate

    def counter_has_plate(self):
        plate = False
        if(len(self.items) == 1):
            if(self.items[0].ingredient_name == 'Plate'):
                plate = True
        elif(len(self.items) > 1):
            plate = True
        return plate
    
    def manually_place_one_item(self, attributes):
        item = Ingredient(self.game,attributes[0],
                                     attributes[1],attributes[2],attributes[3])
        
        item._layer = self._layer + 3
        item.x = self.x
        item.cut_state = attributes[4]
        item.cook_state = attributes[5]
        if(not self.game.top_perspective_counters in self.groups):
            item.y = self.y + TILE_SIZE
        else:
            item.y = self.y
        self.items.append(item)

    def place_all_items(self):
        item_attrs = [99, ]
        for item in self.game.player.inventory:
            item._layer = self._layer + 3
            item.x = self.x
            if(not self.game.top_perspective_counters in self.groups):
                item.y = self.y + TILE_SIZE
            else:
                item.y = self.y
            self.items.append(item)
            useful_attributes = item.get_characteristic_attributes() # length = 7
            useful_attributes.append(self.x)
            useful_attributes.append(self.y)
            item_attrs.append(useful_attributes)
        self.game.player.inventory.clear()

        print("Station coordinates below in row,column:")
        print(str(self.y), str(self.x))
        # self.game.socket_client.send(pickle.dumps(item_attrs))
        
        # DELTA: if share station, remove item and send over
        if (self.game.find_share_station(self.y, self.x) != None):
            print("SENDING DATA FROM PLAYER:", str(self.game.player.client_ID))
            self.game.socket_client.send(pickle.dumps(item_attrs))
            print("Data:", str(item_attrs))
            
            # Delete the item, is this done correctly?
            while self.items:
                temp = self.items.pop()
                # temp.x = -100000
                # temp.y = -100000
                temp.deep_kill()
                # # temp.kill()
                # del temp
            # self.game.player.inventory.extend(self.items)
            # self.items.clear()
            
            print(len(self.game.player.inventory))
            pass

        # self.game.socket_client.send(pickle.dumps(item_attrs))

    def place_all_but_plate(self):
        # move everything from inventory to counter that isn't a plate
        temp = []
        for item in self.game.player.inventory:
            if item.ingredient_name != 'Plate':
                item._layer = self._layer + 3
                item.x = self.x
                if(not self.game.top_perspective_counters in self.groups):
                    item.y = self.y + TILE_SIZE
                else:
                    item.y = self.y
                temp.append(item)
                self.items.append(item)
        for item in temp:
            self.game.player.inventory.remove(item)
        temp.clear()

    def counter_has_raw(self):
        raw = False
        if(len(self.items) == 1):
            if(self.items[0].cut_state < CHOP_TIMES and self.items[0].cook_state == 0):
                raw = True
        return raw
    
    def counter_has_chopped(self):
        chopped = False
        if(len(self.items) == 1):
            if(self.items[0].cut_state >= CHOP_TIMES):
                chopped = True
        return chopped

    def counter_has_cooked(self):
        cooked = False
        if(len(self.items) == 1):
            if(self.items[0].cook_state >= STIR_TIMES):
                cooked = True
        return cooked

    def player_has_raw(self):
        raw = False
        if(len(self.game.player.inventory) == 1):
            if(self.game.player.inventory[0].cut_state + self.game.player.inventory[0].cook_state == 0):
                raw = True
        return raw

    def player_has_chopped(self):
        chopped = False
        if(len(self.game.player.inventory) == 1):
            if(self.game.player.inventory[0].cut_state >= CHOP_TIMES):
                chopped = True
        return chopped

    def player_has_cooked(self):
        cooked = False
        if(len(self.game.player.inventory) == 1):
            if(self.game.player.inventory[0].cook_state >= STIR_TIMES):
                cooked = True
        return cooked

    def pick_up_all(self):
        for item in self.items:
            item._layer = INVENTORY_LAYER
            item.x = INVENTORY_X
            item.y = INVENTORY_Y
        self.game.player.inventory.extend(self.items)
        self.items.clear()

    def pick_up_all_but_plate(self):
        # if the player has a plate, all items on the counter (except for the plate) can be transfered to the inventory 
        temp = []
        for item in self.items:
            if(item.ingredient_name != 'Plate'):
                item._layer = INVENTORY_LAYER
                item.x = INVENTORY_X
                item.y = INVENTORY_Y
                self.game.player.inventory.append(item)
                temp.append(item)
        for item in temp:
            self.items.remove(item)
        temp.clear()

    def place_item(self):
        print('reg counter place item')
        if(len(self.items) == 0):
            self.place_all_items()
        elif(not self.counter_has_raw()):
            if(self.counter_has_plate()):       # if the single item on the counter is a plate
                if (not self.player_has_raw()): # move all items from player inventory that isn't plate or raw
                    self.place_all_but_plate()
            else: # the item on the counter is a prepared ingredient
                if(self.player_has_plate()):    # if the player has a plate, all aitems can be moved to counter
                    self.place_all_items()

    def pickup_item(self):
        if (len(self.game.player.inventory) == 0):
            self.pick_up_all()
        elif(not self.player_has_raw()):
            if(self.player_has_plate()):
                if(not self.counter_has_raw()):
                    self.pick_up_all_but_plate()
            else:
                if(self.counter_has_plate()):
                    self.pick_up_all()
class IngredientsCounter(MultiplayerCounter):
    def __init__(self, ingredient, *args, **kw):
        super().__init__(*args, **kw) 
        self.ingredient = ingredient

    def place_item(self):
        pass

    def pickup_item(self):
        if(self.game.player.message == self.ingredient):
            if(len(self.game.player.inventory) == 0):
                self.game.player.inventory.append(Ingredient(self.game,self.ingredient,INVENTORY_X,INVENTORY_Y,INVENTORY_LAYER))

class ChopCounter(MultiplayerCounter):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw) 

    def place_item(self):
        if (len(self.game.player.inventory) == 1):
            if(self.player_has_raw() or self.player_has_chopped()):
                self.place_all_items()
        elif(len(self.game.player.inventory) == 2):
            if(self.player_has_chopped(self.game.player.inventory[:1]) or self.player_has_chopped(self.game.player.inventory[:-1])):
                self.place_all_but_plate()

    def chop(self):
        if(self.counter_has_raw()):
            self.items[0].cut_state += 1

    def chopped(self):
        if(len(self.items) > 0):
            if(self.items[0].cut_state >= 3):
                return True
            else:
                return False
        else:
            return False

class CookCounter(MultiplayerCounter):
    def __init__(self, type, *args, **kw):
        super().__init__(*args, **kw) 
        self.type = type

    def place_item(self):
        if self.type == 'pan':
            if(self.player_has_chopped()):
                self.place_all_items()
            if (len(self.game.player.inventory) == 2):
                if(self.game.player.inventory[0].ingredient_name != 'Plate' and self.game.player.inventory[0].cut_state >= CHOP_TIMES):
                    self.place_all_but_plate()
                elif(self.game.player.inventory[1].ingredient_name != 'Plate' and self.game.player.inventory[1].cut_state >= CHOP_TIMES):
                    self.place_all_but_plate()
        else:
            for item in self.game.player.inventory:
                if item.cut_state >= CHOP_TIMES:
                    self.items.append(item)
                    self.game.player.inventory.remove(item)

    def pickup_item(self):
        if(len(self.items) <= 1):
            if(not self.player_has_raw() and not self.player_has_chopped()):
                if(self.player_has_cooked):
                    if(self.player_has_plate):
                        self.pick_up_all()  # player's inventory either contains a plated item or nothing
    
    def cook(self):
        if(self.counter_has_chopped()):
            self.items[0].cook_state += 1

    def cooked(self):
        if(len(self.items) > 0):
            if(self.items[0].cook_state >= 3):
                return True
            else:
                return False
        else:
            return False

class SubmitStation(MultiplayerCounter):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw) 
        self.frames = 120

    def place_item(self):
        if(len(self.items) == 0):
            if(self.player_has_plate()):
                self.place_all_items()
        print('placed item in submit station')

    def pickup_item(self):
        print('pick up from submit station')
        pass

    def update(self):
        if(len(self.items) > 0):
            print('counting down')
            self.frames -= 1
            if(self.frames == 0):
                # check if matches any recipecard
                print('stop')

                # list of 4 0's
                submitted = [0] * 4
                bun_i = 0
                meat_i = 1
                let_i = 2
                tom_i = 3

                score = 0

                for item in self.items:
                    print('item: ' + item.ingredient_name)
                    if(item.ingredient_name == "Bun"):
                        if(item.cut_state == 0 and item.cook_state >= STIR_TIMES):
                            score += item.score
                            submitted[bun_i] = 1
                    if(item.ingredient_name == "Meat"):
                        if(item.cut_state >= CHOP_TIMES and item.cook_state >= STIR_TIMES):
                            score += item.score
                            submitted[meat_i] = 1
                    if(item.ingredient_name == "Lettuce"):
                        if(item.cut_state >= CHOP_TIMES and item.cook_state == 0):
                            score += item.score
                            submitted[let_i] = 1
                    if(item.ingredient_name == "Tomato"):
                        if(item.cut_state >= CHOP_TIMES and item.cook_state == 0):
                            score += item.score
                            submitted[tom_i] = 1

                if(submitted[bun_i] == 0 or submitted[meat_i] == 0):
                    # every submission should have bun and meat
                    pass
                else:
                    del_index = -1
                    for i in range(len(self.game.recipes)):
                        recipe = self.game.recipes[i]
                        if(recipe.ingredient_3 == None and recipe.ingredient_4 == None):
                            if(submitted[let_i] == 0 and submitted[tom_i] == 0):
                                del_index = i
                                break
                        elif(recipe.ingredient_3 != None and recipe.ingredient_4 == None):
                            if(submitted[let_i] == 1 and submitted[tom_i] == 0):
                                del_index = i
                                break
                        elif(recipe.ingredient_3 == None and recipe.ingredient_4 != None):
                            if(submitted[let_i] == 0 and submitted[tom_i] == 1):
                                del_index = i
                                break

                    if(del_index > -1):
                        self.game.score.update_score(score)
                        print('del index' + str(del_index))
                        del self.game.recipes[del_index]
                        for i in range(len(self.game.recipes)):
                            # if(i > del_index):
                            self.game.recipes[i].x = 3*TILE_SIZE + ((i) * 2 * TILE_SIZE)

                print(self.items)
                # remove all items from counter regardless
                for item in self.items:
                    print('killing ' + item.ingredient_name)
                    item.deep_kill()
                self.items.clear()
                print('complete')

                self.frames = 120

                '''
                del_index = -1
                index = -1
                for recipe in self.game.recipes:
                    score = 0
                    index += 1
                    dont_count_score = False
                    for item in self.items:
                        # if match, then add to score
                        print('ingredient: ' + item.ingredient_name)
                        if(item.ingredient_name == 'Lettuce' and recipe.ingredient_3 == None):
                            dont_count_score = True
                            break
                        if(item.ingredient_name == 'Tomato' and recipe.ingredient_4 == None):
                            dont_count_score = True
                            break
                        if(item.ingredient_name == 'Lettuce' and recipe.ingredient_3 != None):
                            if(item.cut_state != recipe.ingredient_3.cut_state or item.cook_state != recipe.ingredient_3.cook_state):
                                dont_count_score = True
                                break
                            elif(item.cut_state == recipe.ingredient_3.cut_state and item.cook_state == recipe.ingredient_3.cook_state):
                                score += item.score
                        if(item.ingredient_name == 'Tomato' and recipe.ingredient_4 != None):
                            if(item.cut_state != recipe.ingredient_4.cut_state or item.cook_state != recipe.ingredient_4.cook_state):
                                dont_count_score = True
                                break
                            elif(item.cut_state == recipe.ingredient_4.cut_state and item.cook_state == recipe.ingredient_4.cook_state):
                                score += item.score
                        if(item.ingredient_name == 'Bun'): 
                            if(item.cut_state == recipe.ingredient_1.cut_state and item.cook_state == recipe.ingredient_1.cook_state):
                                score += item.score
                        if(item.ingredient_name == 'Meat'):
                            if(item.cut_state == recipe.ingredient_2.cut_state and item.cook_state == recipe.ingredient_2.cook_state):
                                score += item.score
                    if(dont_count_score == False):
                        if(recipe.ingredient_3 == None and recipe.ingredient_4 == None and score == 40):
                            self.game.score.update_score(score)
                            del_index = index
                            break
                        if(recipe.ingredient_3 != None and recipe.ingredient_4 == None and score == 60):
                            self.game.score.update_score(score)
                            del_index = index
                            break
                        if(recipe.ingredient_3 == None and recipe.ingredient_4 != None and score == 60):
                            self.game.score.update_score(score)
                            del_index = index
                            break
                        if(recipe.ingredient_3 != None and recipe.ingredient_4 != None and score == 80):
                            self.game.score.update_score(score)
                            del_index = index
                            break

                if(del_index != -1):
                    print('del index' + str(del_index))
                    del self.game.recipes[del_index]
                    for i in range(len(self.game.recipes)):
                        # if(i > del_index):
                        self.game.recipes[i].x = 3*TILE_SIZE + ((i) * 2 * TILE_SIZE)
                    # del self.game.recipes[del_index]
                    # self.game.recipes[del_index]
                for item in self.items:
                    item.deep_kill()
                self.items.clear()
                print('complete')
                '''

class IngredientsCounter(MultiplayerCounter):
    def __init__(self, ingredient, *args, **kw):
        super().__init__(*args, **kw) 
        self.ingredient = ingredient

    def place_item(self):
        pass

    def pickup_item(self):
        if(self.game.player.message == self.ingredient):
            if(len(self.game.player.inventory) == 0):
                self.game.player.inventory.append(Ingredient(game=self.game, name=self.ingredient, x=INVENTORY_X, y=INVENTORY_Y, layer=INVENTORY_LAYER))
