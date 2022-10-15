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
        self.rect = self.image.get_rect(topleft = pos)
        self.vector = pygame.math.Vector2()
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

    def updateColor(self, color):
        #theme color change
        self.image.fill(color)


    #     self.powerup_end_time = pygame.time.get_ticks()
    #     if (self.powerup_end_time - self.powerup_start_time  > 7000):
    #         self.change_size(140)
    #     if self.image.get_height() == 240:
    #         self.create_powerup_text()

    # def change_size(self, size):
    #     # self.create_powerup_text()
    #     self.image = pygame.Surface((10, size))
    #     new_size = ((WIDTH - self.image.get_width()), (self.rect.top))
    #     self.rect = self.image.get_rect(topleft = new_size)
    #     self.image.fill((200, 200, 200))
    #     if size == 240:
    #         self.powerup_start_time = pygame.time.get_ticks()
    #         self.create_powerup_text()

    # def create_powerup_text(self):
    #     TEXT_COLOR = (200, 200, 200)
    #     FONT = pygame.font.Font('freesansbold.ttf', 16)
    #     player_surface = FONT.render(str("SIZE INCREASE - ACTIVE"), True, TEXT_COLOR)
    #     self.screen.blit(player_surface, (WIDTH - WIDTH / 6, 15))