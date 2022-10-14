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
            ((WIDTH - BUNGIE_SIZE[0])/2, 0),
            BUNGUE_COLOR,
            self.bungie_sprites
        )

        self.bungueTop = Bungie(
            BUNGIE_SIZE,
            ((WIDTH - BUNGIE_SIZE[0])/2, HEIGHT-BUNGIE_SIZE[1]),
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
            if self.powerup.color == POWERUP1_COLOR:
                if self.player_round:
                    self.change_board_size(self.player, 240)
                    self.powerup.moveOffscreen()
                else:
                    self.change_board_size(self.opponent, 240)
                    self.powerup.moveOffscreen()

    def powerup_timer(self):
        self.player_speed_end_time = pygame.time.get_ticks()
        self.opponent_speed_end_time = pygame.time.get_ticks()

        if (self.player_speed_end_time - self.player_speed_start_time  > 7000):
            self.change_board_size(self.player, 140)
        if self.player.image.get_height() == 240:
            self.create_powerup_text()

        if (self.opponent_speed_end_time - self.opponent_speed_start_time  > 7000):
            self.change_board_size(self.opponent, 140)
        if self.opponent.image.get_height() == 240:
            self.create_powerup_text()

    # change the size of the board/paddle
    def change_board_size(self, board, size):
        board.image = pygame.Surface((10, size))
        board.rect = board.image.get_rect(center = board.rect.center)
        board.image.fill((200, 200, 200))

        if size == 240 and board.name == "player":
            self.player_speed_start_time = pygame.time.get_ticks()
            self.create_powerup_text()
        elif size == 240 and board.name == "opponent":
            self.opponent_speed_start_time = pygame.time.get_ticks()
            self.create_powerup_text()

    # change the speed of the ball
    def change_ball_speed(self):
        self.ball.speed *= float(random.randint(1, 9)) * 0.1

    # change the size of the ball
    def change_ball_size(self):
        pass

    # change the speed of the paddle
    def change_board_speed(self, board):
        pass

        
    def create_powerup_text(self):
        TEXT_COLOR = (200, 200, 200)
        font = pygame.font.Font('freesansbold.ttf', 16)
        player_surface = font.render(str("SIZE INCREASE - ACTIVE"), True, TEXT_COLOR)
        self.screen.blit(player_surface, (WIDTH - WIDTH / 6, 15))


    def detect_bungie(self):
        if self.ball.rect.colliderect(self.bungueBottom.rect) or self.ball.rect.colliderect(self.bungueTop.rect):
            pygame.mixer.Sound.play(BUNGIE_SOUND)
            self.ball.bounce("y", "on")