import pygame
import random
from powerup import Powerup

from settings import *
from player import Player
from opponent import Opponent
from ball import Ball
from powerup import Powerup

FONT = pygame.font.Font('freesansbold.ttf', 32)

class Level():
    def __init__(self, screen):
        self.screen = screen
        # decide whose round it is
        self.player_round = False
        
        self.player_powerup_start_time = 0
        self.player_powerup_end_time = 0
        self.opponent_powerup_start_time = 0
        self.opponent_powerup_end_time = 0


        self.board_sprites = pygame.sprite.Group()
        self.ball_sprites = pygame.sprite.Group()
        self.powerup_sprites = pygame.sprite.Group()

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


    def run(self):
        self.player_round = self.get_round()

        self.screen.fill(BG_COLOR)
        pygame.draw.aaline(self.screen, OBJ_COLOR, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))

        self.board_sprites.draw(self.screen)
        self.ball_sprites.draw(self.screen)
        self.powerup_sprites.draw(self.screen)

        self.opponent.chase_ball(self.ball)

        self.create_score()

        self.detect_powerup()

        self.board_sprites.update()
        self.ball_sprites.update()
        self.powerup_sprites.update()



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
            pygame.mixer.Sound.play(PONG_SOUND)
            if self.player_round:
                self.change_size(self.player, 240)
                self.powerup.moveOffscreen()
            else:
                self.change_size(self.opponent, 240)
                self.powerup.moveOffscreen()

    def powerup_timer(self):
        self.player_powerup_end_time = pygame.time.get_ticks()
        self.opponent_powerup_end_time = pygame.time.get_ticks()

        if (self.player_powerup_end_time - self.player_powerup_start_time  > 7000):
            self.change_size(self.player, 140)
        if self.player.image.get_height() == 240:
            self.create_powerup_text()

        if (self.opponent_powerup_end_time - self.opponent_powerup_start_time  > 7000):
            self.change_size(self.opponent, 140)
        if self.opponent.image.get_height() == 240:
            self.create_powerup_text()

    def change_size(self, board, size):
        # self.create_powerup_text()
        board.image = pygame.Surface((10, size))

        new_pos = ((board.rect.left), (board.rect.top))

        board.rect = board.image.get_rect(topleft = new_pos)
        board.image.fill((200, 200, 200))

        if size == 240 and board.name == "player":
            self.player_powerup_start_time = pygame.time.get_ticks()
            self.create_powerup_text()
        elif size == 240 and board.name == "opponent":
            self.opponent_powerup_start_time = pygame.time.get_ticks()
            self.create_powerup_text()
        
    def create_powerup_text(self):
        TEXT_COLOR = (200, 200, 200)
        font = pygame.font.Font('freesansbold.ttf', 16)
        player_surface = font.render(str("SIZE INCREASE - ACTIVE"), True, TEXT_COLOR)
        self.screen.blit(player_surface, (WIDTH - WIDTH / 6, 15))