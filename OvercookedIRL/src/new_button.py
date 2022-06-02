# original button class from: https://github.com/russs123/pygame_tutorials/blob/main/Button/button.py

import pygame
from pygame import mixer

mixer.init()
knife_sharpen_sound = mixer.Sound("Sounds/knife_sharpen.wav")
knife_sharpen_sound.set_volume(0.1)

#button class
class Button():
    def __init__(self, image, alt_image, scale, win_width, win_height, middle, is_button, x=0, y=0):
        width = image.get_width()
        height = image.get_height()
        self.is_button = is_button
        self.win_width = win_width
        self.win_height = win_height
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        if alt_image is not None:
            self.alt_image = pygame.transform.scale(alt_image, (int(width * scale), int(height * scale)))
        else:
            self.alt_image = alt_image
        self.rect = self.image.get_rect()
        if middle is True:
            self.rect.midtop = (int(win_width/2) + x, int(win_height/2) + y)
        else:
            self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.is_button:
            if self.rect.collidepoint(pos) and self.alt_image is not None:
                surface.blit(self.alt_image, (self.rect.x, self.rect.y))
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    knife_sharpen_sound.play()
                    self.clicked = True
                    action = True
            else:
                #draw button on screen
                surface.blit(self.image, (self.rect.x, self.rect.y))
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y))

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action