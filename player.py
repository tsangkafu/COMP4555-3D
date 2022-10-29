import pygame

from settings import *


class Player(pygame.sprite.Sprite):

    # pos = position
    # group = sprite group
    def __init__(self, size, pos, color, group, screen):
        super().__init__(group)
        self.name = "player"
        self.score = 0
        self.speed = 7
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)
        self.vector = pygame.math.Vector2()
        self.start = 0
        self.criticalCD = 0
        self.critical_end = 0
        self.deactivatestart = 0
        self.active = 0
        self.powerup_start_time = 0
        self.powerup_end_time = 0
        self.screen = screen
        self.color_setting = 1

    def update(self):
        # get key press and move up or down
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not self.rect.top <= 0:
            self.rect.y -= self.speed
        elif keys[pygame.K_DOWN] and not self.rect.bottom >= HEIGHT:
            self.rect.y += self.speed
        elif keys[pygame.K_1]:
            self.color_setting = 1
        elif keys[pygame.K_2]:
            self.color_setting = 2
        elif keys[pygame.K_3]:
            self.color_setting = 3
        elif keys[pygame.K_4]:
            self.color_setting = 4

        self.critical_end = pygame.time.get_ticks()
        if keys[pygame.K_SPACE]:
            if (self.critical_end - self.criticalCD > 2500) or self.start == 0:
                self.start = 1
                self.criticalHitactive()

        if (self.critical_end - self.criticalCD > 300 and self.active == 1):
            self.criticalDeactivate()

    def updateColor(self, color):
        # theme color change
        self.image.fill(color)

    def criticalHitactive(self):
        while self.rect.right != WIDTH - 56:
            self.rect.x -= 1
        self.criticalCD = pygame.time.get_ticks()
        self.active = 1

    def criticalDeactivate(self):
        while self.rect.right != WIDTH:
            self.rect.x += 1
        self.deactivatestart = pygame.time.get_ticks()
        self.active = 0
