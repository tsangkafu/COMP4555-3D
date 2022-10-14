import pygame
import random

from settings import *
from player import Player
from opponent import Opponent
from ball import Ball
from powerup import Powerup
from bungie import Bungie

FONT = pygame.font.Font('freesansbold.ttf', 32)

class Level():
    def __init__(self, screen):
        self.screen = screen
        # decide whose round it is
        self.player_round = False
        
        # timer for powerups
        self.player_speed_start_time = 0
        self.player_speed_end_time = 0
        self.opponent_speed_start_time = 0
        self.opponent_speed_end_time = 0
        self.player_size_start_time = 0
        self.player_size_end_time = 0
        self.opponent_size_start_time = 0
        self.opponent_size_end_time = 0
        self.ball_speed_start_time = 0
        self.ball_speed_end_time = 0

        self.board_sprites = pygame.sprite.Group()
        self.ball_sprites = pygame.sprite.Group()
        self.powerup_sprites = pygame.sprite.Group()
        self.bungie_sprites = pygame.sprite.Group()

        self.player = Player(
            # size
            BOARD_SIZE,
            # position of the top left of the player
            (WIDTH - BOARD_SIZE[0], (HEIGHT - BOARD_SIZE[1]) / 2),
            OBJ_COLOR,
            self.board_sprites,
            screen)

        self.opponent = Opponent(
            # size
            BOARD_SIZE,
            # position of the top left of the player
            (0, (HEIGHT - BOARD_SIZE[1]) / 2),
            OBJ_COLOR,
            self.board_sprites)

        self.powerup = Powerup(
            # size
            POWERUP_SIZE,
            # position of the top left of the player
            ((WIDTH - POWERUP_SIZE[0])/2, Powerup.randomizeHeight(self)),
            random.choice(COLOR_LIST),
            self.powerup_sprites) #sprites

        self.ball = Ball(
            # surface
            BALL_RADIUS,
            (WIDTH / 2, HEIGHT / 2),
            OBJ_COLOR,
            self.ball_sprites,
            self.player,
            self.opponent,
            self.powerup)

        self.bungueBottom = Bungie(
            BUNGIE_SIZE,
            (BUNGIE_X_POS, 0),
            BUNGUE_COLOR,
            self.bungie_sprites
        )

        self.bungueTop = Bungie(
            BUNGIE_SIZE,
            (BUNGIE_X_POS, HEIGHT-BUNGIE_SIZE[1]),
            BUNGUE_COLOR,
            self.bungie_sprites
        )


    def run(self):
        self.player_round = self.get_round()

        self.screen.fill(BG_COLOR)
        pygame.draw.aaline(self.screen, OBJ_COLOR, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))

        self.board_sprites.draw(self.screen)
        self.ball_sprites.draw(self.screen)
        self.powerup_sprites.draw(self.screen)
        self.bungie_sprites.draw(self.screen)

        self.opponent.chase_ball(self.ball)

        self.create_score()

        self.detect_powerup()

        self.detect_bungie()

        self.board_sprites.update()
        self.ball_sprites.update()
        self.powerup_sprites.update()
        self.bungie_sprites.update()


    def create_score(self):
        player_surface = FONT.render(str(self.player.score), True, OBJ_COLOR)
        self.screen.blit(player_surface, (660, 15))
        opponent_surface = FONT.render(str(self.opponent.score), True, OBJ_COLOR)
        self.screen.blit(opponent_surface, (600, 15))

    # detect if it is player's round upon collusion with ball
    def get_round(self):
        if self.player.rect.colliderect(self.ball.rect):
            return True
        if self.opponent.rect.colliderect(self.ball.rect):
            return False
        return self.player_round

    def detect_powerup(self):
        self.powerup_timer()

        if self.ball.rect.colliderect(self.powerup.rect):
            pygame.mixer.Sound.play(POWERUP_SOUND)
            # purple = change board size
            if self.powerup.color == POWERUP1_COLOR:
                if self.player_round:
                    self.change_board_size(self.player, 240)
                    self.powerup.moveOffscreen()
                else:
                    self.change_board_size(self.opponent, 240)
                    self.powerup.moveOffscreen()
            # yellow = change ball speed
            elif self.powerup.color == POWERUP2_COLOR:
                self.change_ball_size(LARGE_BALL_RADIUS)
                self.powerup.moveOffscreen()
            # blue = change board speed
            elif self.powerup.color == POWERUP3_COLOR:
                if self.player_round:
                    self.change_board_speed(self.player, BALL_SPEED_ENHANCED)
                    self.powerup.moveOffscreen()
                else:
                    self.change_board_speed(self.opponent, BALL_SPEED_ENHANCED)
                    self.powerup.moveOffscreen()

    def powerup_timer(self):
        self.player_size_end_time = pygame.time.get_ticks()
        self.opponent_size_end_time = pygame.time.get_ticks()
        self.player_speed_end_time = pygame.time.get_ticks()
        self.opponent_speed_end_time = pygame.time.get_ticks()
        self.ball_speed_end_time = pygame.time.get_ticks()

        if (self.player_size_end_time - self.player_size_start_time  > 10000):
            self.change_board_size(self.player, 140)
        if self.player.image.get_height() == 240:
            self.create_powerup_text("PLAYER SIZE INCREASE - ACTIVE")

        if (self.opponent_size_end_time - self.opponent_size_start_time  > 10000):
            self.change_board_size(self.opponent, 140)
        if self.opponent.image.get_height() == 240:
            self.create_powerup_text("OPPONENT SIZE INCREASE - ACTIVE")

        if (self.player_speed_end_time - self.player_speed_start_time > 10000):
            self.change_board_speed(self.player, 7)
        if self.player.speed == 10:
            self.create_powerup_text("PLAYER SPPED INCREASE - ACTIVE")

        if (self.opponent_speed_end_time - self.opponent_speed_start_time > 10000):
            self.change_board_speed(self.opponent, 7)
        if self.opponent.speed == 10:
            self.create_powerup_text("OPPONENT SPPED INCREASE - ACTIVE")

        if (self.ball_speed_end_time - self.ball_speed_start_time > 10000):
            self.change_ball_size(BALL_RADIUS)
        if self.ball.radius == LARGE_BALL_RADIUS:
            self.create_powerup_text("BALL SIZE INCREASE - ACTIVE")

    # change the size of the board/paddle
    def change_board_size(self, board, size):
        board.image = pygame.Surface((BOARD_SIZE[0], size))
        board.rect = board.image.get_rect(center = board.rect.center)
        board.image.fill((200, 200, 200))

        if size == 240 and board.name == "player":
            self.player_size_start_time = pygame.time.get_ticks()
        elif size == 240 and board.name == "opponent":
            self.opponent_size_start_time = pygame.time.get_ticks()

    # change the speed of the paddle
    def change_board_speed(self, board, speed):
        board.speed = speed
        if speed == BALL_SPEED_ENHANCED and board.name == "player":
            self.player_speed_start_time = pygame.time.get_ticks()
        elif speed == BALL_SPEED_ENHANCED and board.name == "opponent":
            self.opponent_speed_start_time = pygame.time.get_ticks()

    # change the speed of the ball
    def change_ball_size(self, radius):
        self.ball.radius = radius
        self.ball.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.ball.image, OBJ_COLOR, (radius, radius), radius)
        self.ball.rect = self.ball.image.get_rect(center = self.ball.rect.center)
        if self.ball.radius == LARGE_BALL_RADIUS:
            self.ball_speed_start_time = pygame.time.get_ticks()
            self.create_powerup_text("BALL SIZE INCREASE - ACTIVE")

        
    def create_powerup_text(self, text):
        TEXT_COLOR = (200, 200, 200)
        font = pygame.font.Font('freesansbold.ttf', 16)
        player_surface = font.render(str(text), True, TEXT_COLOR)
        self.screen.blit(player_surface, (WIDTH - WIDTH / 6, 15))


    def detect_bungie(self):
        if self.ball.rect.colliderect(self.bungueBottom.rect) or self.ball.rect.colliderect(self.bungueTop.rect):
            pygame.mixer.Sound.play(BUNGIE_SOUND)
            self.ball.bounce("y", "on")