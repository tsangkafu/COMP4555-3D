import pygame

class Opponent(pygame.sprite.Sprite):
    # pos = position
    # group = sprite group
    def __init__(self, size, pos, color, group):
        super().__init__(group)
        self.speed = 7
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = pos)

    def update(self):
        pass