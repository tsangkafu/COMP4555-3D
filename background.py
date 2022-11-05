import pygame
import os

class Background():
    
    def __init__(self):
        self.image = pygame.image.load(os.path.join(".//media//image//background", "bg.png")).convert_alpha()
        self.x = 0
        self.y = 0