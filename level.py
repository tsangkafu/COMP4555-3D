import pygame
from powerup import Powerup

from settings import *
from player import Player
from opponent import Opponent
from ball import Ball
from powerup import Powerup

BG_COLOR = pygame.Color('grey12')
BALL_RADIUS = 20
BOARD_SIZE = (10, 140)
OBJ_COLOR = (200, 200, 200)

# POWERUP CONSTS
POWERUP_SIZE = (50, 50)
POWERUP1_COLOR = (200, 0, 200)
POWERUP2_COLOR = (255, 255, 0)
POWERUP3_COLOR = (0, 255, 255)

FONT = pygame.font.Font('freesansbold.ttf', 32)

class Level():
    def __init__(self, screen):
        self.screen = screen
        self.sprites = pygame.sprite.Group()

        self.player = Player(
            # size
            BOARD_SIZE,
            # position of the top left of the player
            (WIDTH - BOARD_SIZE[0], (HEIGHT - BOARD_SIZE[1]) / 2),
            OBJ_COLOR,
            self.sprites)

        self.opponent = Opponent(
            # size
            BOARD_SIZE,
            # position of the top left of the player
            (0, (HEIGHT - BOARD_SIZE[1]) / 2),
            OBJ_COLOR,
            self.sprites)

        self.ball = Ball(
            # surface
            BALL_RADIUS,
            (WIDTH / 2, HEIGHT / 2),
            OBJ_COLOR,
            self.sprites,
            self.player,
            self.opponent)

        self.powerup = Powerup(
            # size
            POWERUP_SIZE,
            # position of the top left of the player
            ((WIDTH - POWERUP_SIZE[0])/2, Powerup.randomizeHeight()),
            POWERUP1_COLOR,
            self.sprites) #sprites

    def run(self):
        self.screen.fill(BG_COLOR)
        pygame.draw.aaline(self.screen, OBJ_COLOR,
                           (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))

        self.sprites.draw(self.screen)

        self.opponent.chase_ball(self.ball)
        self.create_score()

        self.sprites.update()

    def create_score(self):
        player_surface = FONT.render(str(self.player.score), True, OBJ_COLOR)
        self.screen.blit(player_surface, (660, 15))
        opponent_surface = FONT.render(
            str(self.opponent.score), True, OBJ_COLOR)
        self.screen.blit(opponent_surface, (600, 15))
