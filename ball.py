import pygame
from settings import *

class Ball(pygame.sprite.Sprite):
    # pos = position
    # group = sprite group
    def __init__(self, radius, pos, color, group):
        super().__init__(group)
        self.radius = radius
        self.speed = 7
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.rect = self.image.get_rect(topleft = pos)
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)

    def update(self):
        pass