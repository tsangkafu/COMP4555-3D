import random
import pygame
import globals
import os

class Powerup(pygame.sprite.Sprite):
    def __init__(self, groups, center):
        super().__init__(groups)
        #available powerups: heal, twin, heart, shield, laser, plasma 
        self.type = random.choice(['heal','twin','shield'])


        path = f".//media//image//bullet + fx + powerup + coin//powerups//{str(self.type)}"
        num_of_img = globals.count_image(path)
        self.animation = []

        for i in range(num_of_img):
            self.animation.append(pygame.image.load(os.path.join(path, str(i) + ".png")).convert_alpha())

        self.current_frame = random.randint(0, len(self.animation) - 1)
        self.image = self.animation[self.current_frame]
        
        self.rect = self.image.get_rect(center = center)
        self.speed = 5

    
    def update(self):
        self.current_frame += 0.2

        if self.current_frame >= len(self.animation):
            self.current_frame = 0
        self.image = self.animation[int(self.current_frame)]

        # fall speed
        self.rect.y += self.speed

        # kill the powerup if it goes off the bottom of the screen
        if self.rect.top > globals.DISPLAY_HEIGHT:
            self.kill()


