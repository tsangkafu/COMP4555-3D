import pygame
import os
import globals


class Background():

    def __init__(self, level):
        self.image = pygame.image.load(os.path.join(
            ".//media//image//background", f"bg-{str(level)}.png")).convert()
        self.image = pygame.transform.scale(
            self.image, (globals.DISPLAY_WIDTH, globals.DISPLAY_HEIGHT))
        self.x = 0
        self.y = 0
