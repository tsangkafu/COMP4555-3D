import pygame

from settings import *
from player import Player
from opponent import Opponent
from ball import Ball

BALL_RADIUS = 20
BOARD_SIZE = (10, 140)
COLOR = (200, 200, 200)

class Level():
    def __init__(self):
        self.surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()

        self.player = Player(
            # size
            BOARD_SIZE,
            # position of the top left of the player
            (WIDTH - BOARD_SIZE[0], (HEIGHT - BOARD_SIZE[1]) / 2),
            COLOR,
            self.sprites)

        self.opponent = Opponent(
            # size
            BOARD_SIZE,
            # position of the top left of the player
            (0, (HEIGHT - BOARD_SIZE[1]) / 2),
            COLOR,
            self.sprites)

        self.ball = Ball(
            # surface
            BALL_RADIUS,
            (WIDTH / 2 - BALL_RADIUS, (HEIGHT - BALL_RADIUS) / 2),
            COLOR,
            self.sprites
        )


    def run(self):
        pygame.draw.aaline(self.surface, COLOR, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))
        self.sprites.draw(self.surface)