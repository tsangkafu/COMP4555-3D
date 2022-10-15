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

        if self.player.color_setting == 1:
            BG_COLOR = BG_DEF
            OBJ_COLOR = OBJ_DEF
        elif self.player.color_setting == 2:
            BG_COLOR = BG_GRN
            OBJ_COLOR = OBJ_GRN
        elif self.player.color_setting == 3:
            BG_COLOR = BG_BLU
            OBJ_COLOR = OBJ_BLU
        elif self.player.color_setting == 4:
            BG_COLOR = BG_RED
            OBJ_COLOR = OBJ_RED


        self.screen.fill(BG_COLOR)
        pygame.draw.aaline(self.screen, OBJ_COLOR, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))

        self.board_sprites.draw(self.screen)
        self.ball_sprites.draw(self.screen)
        self.powerup_sprites.draw(self.screen)

        self.opponent.chase_ball(self.ball)

        self.create_score(OBJ_COLOR)

        self.detect_powerup(OBJ_COLOR)

        self.board_sprites.update()
        self.ball_sprites.update(OBJ_COLOR)
        self.powerup_sprites.update()

        self.opponent.updateColor(OBJ_COLOR)
        self.player.updateColor(OBJ_COLOR)

        self.create_theme_text(OBJ_COLOR, self.player.color_setting)

    def create_score(self, color):
        player_surface = FONT.render(str(self.player.score), True, color)
        self.screen.blit(player_surface, (660, 15))
        opponent_surface = FONT.render(str(self.opponent.score), True, color)
        self.screen.blit(opponent_surface, (600, 15))

    # detect if it is player's round upon collusion with ball
    def get_round(self):
        if self.player.rect.colliderect(self.ball.rect):
            return True
        if self.opponent.rect.colliderect(self.ball.rect):
            return False
        return self.player_round

    def detect_powerup(self, color):
        self.powerup_timer(color)

        if self.ball.rect.colliderect(self.powerup.rect):
            pygame.mixer.Sound.play(POWERUP_SOUND)
            if self.player_round:
                self.change_size(self.player, 240, color)
                self.powerup.moveOffscreen()
            else:
                self.change_size(self.opponent, 240, color)
                self.powerup.moveOffscreen()

    def powerup_timer(self, color):
        self.player_powerup_end_time = pygame.time.get_ticks()
        self.opponent_powerup_end_time = pygame.time.get_ticks()

        if (self.player_powerup_end_time - self.player_powerup_start_time  > 7000):
            self.change_size(self.player, 140, color)
        if self.player.image.get_height() == 240:
            self.create_powerup_text(color)

        if (self.opponent_powerup_end_time - self.opponent_powerup_start_time  > 7000):
            self.change_size(self.opponent, 140, color)
        if self.opponent.image.get_height() == 240:
            self.create_powerup_text(color)

    def change_size(self, board, size, color):
        # self.create_powerup_text()
        board.image = pygame.Surface((10, size))

        new_pos = ((board.rect.left), (board.rect.top))

        board.rect = board.image.get_rect(topleft = new_pos)
        board.image.fill(color)

        if size == 240 and board.name == "player":
            self.player_powerup_start_time = pygame.time.get_ticks()
            self.create_powerup_text(color)
        elif size == 240 and board.name == "opponent":
            self.opponent_powerup_start_time = pygame.time.get_ticks()
            self.create_powerup_text(color)
        
    def create_powerup_text(self, color):
        TEXT_COLOR = color
        font = pygame.font.Font('freesansbold.ttf', 16)
        player_surface = font.render(str("SIZE INCREASE - ACTIVE"), True, TEXT_COLOR)
        self.screen.blit(player_surface, (WIDTH - WIDTH / 6, 15))

    def create_theme_text(self, color, opt):
        TEXT_COLOR = color
        if opt == 1:
            theme = "DEFAULT GREY"
        elif opt == 2:
            theme = "RETRO GREEN"
        elif opt == 3:
            theme = "COOL BLUE"
        elif opt == 4:
            theme = "FIERY RED"
        font = pygame.font.Font('freesansbold.ttf', 16)
        opponent_surface = font.render(str("CURRENT THEME: " + theme + " (USE NUMBER KEYS 1-4 TO CHANGE)"), True, TEXT_COLOR)
        self.screen.blit(opponent_surface, (WIDTH - WIDTH / 1, 15))