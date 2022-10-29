import pygame
import os

class Background():
    
    def __init__(self):
        self.image = pygame.image.load(os.path.join(".//media//image//background", "bg.png"))
        self.x = 0
        self.y = 0