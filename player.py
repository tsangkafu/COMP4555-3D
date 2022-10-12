import pygame

from settings import *

class Player(pygame.sprite.Sprite):

    # pos = position
    # group = sprite group
    def __init__(self, size, pos, color, group):
        super().__init__(group)
        self.score = 0
        self.speed = 7
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = pos)
        self.vector = pygame.math.Vector2()

    def update(self):
        # get key press and move up or down
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not self.rect.top <= 0:
            self.rect.y -= self.speed
        elif keys[pygame.K_DOWN] and not self.rect.bottom >= HEIGHT:
            self.rect.y += self.speed

    def change_size(self):
        self.image = pygame.Surface((10,240))
        new_size = ((WIDTH - self.image.get_width()), (self.rect.top))
        self.rect = self.image.get_rect(topleft = new_size)
        self.image.fill((200, 200, 200))
