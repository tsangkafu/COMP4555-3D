import pygame

from settings import *


class Bungie(pygame.sprite.Sprite):

    # pos = position
    # group = sprite group
    def __init__(self, size, pos, color, group):
        super().__init__(group)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.color = color
        self.rect = self.image.get_rect(topleft=pos)
        self.vector = pygame.math.Vector2()
