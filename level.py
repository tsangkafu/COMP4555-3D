from re import X
from turtle import width
import pygame
import random
from settings import *
from player import Player
from opponent import Opponent
from ball import Ball
from powerup import Powerup
from bungie import Bungie

pygame.font.init()

FONT = pygame.font.Font('freesansbold.ttf', 32)
END_GAME_FONT = pygame.font.Font('freesansbold.ttf', 70)


class Level():
    def __init__(self, screen):
        self.screen = screen
        # decide whose round it is
        self.player_round = False

        self.end_game = False
        self.fader = pygame.Surface((WIDTH, HEIGHT))
        self.fader.fill((0, 0, 0))
        self.fader.set_alpha(150)

        # timer for paddle speed-up powerups
        self.player_speed_start_time = 0
        self.player_speed_end_time = 0
        self.opponent_speed_start_time = 0
        self.opponent_speed_end_time = 0
        # timer for paddle size-up powerups
        self.player_size_start_time = 0
        self.player_size_end_time = 0
        self.opponent_size_start_time = 0
        self.opponent_size_end_time = 0
        # timer for ball speed powerups
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
            self.powerup_sprites)  # sprites

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
            BUNGIE_COLOR,
            self.bungie_sprites
        )

        self.bungueTop = Bungie(
            BUNGIE_SIZE,
            ((WIDTH - BUNGIE_SIZE[0])/2, HEIGHT-BUNGIE_SIZE[1]),
            BUNGIE_COLOR,
            self.bungie_sprites
        )

    def run(self):
        # determine when to end game
        if self.player.score >= ROUND or self.opponent.score >= ROUND:
            self.end_game = True

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

        self.create_logo(OBJ_COLOR)
        
        self.player_round = self.get_round()
        pygame.draw.aaline(self.screen, OBJ_COLOR,
                           (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))

        self.board_sprites.draw(self.screen)

        self.powerup_sprites.draw(self.screen)
        self.bungie_sprites.draw(self.screen)

        self.create_score(OBJ_COLOR)

        self.opponent.updateColor(OBJ_COLOR)
        self.player.updateColor(OBJ_COLOR)

        self.create_theme_text(OBJ_COLOR, self.player.color_setting)

        if self.end_game:
            self.end_screen(OBJ_COLOR)
        else:
            # booleans for powerup text
            self.pl_sizeEfct = False
            self.pl_ballEfct = False
            self.pl_speedEfct = False
            self.op_sizeEfct = False
            self.op_ballEfct = False
            self.op_speedEfct = False

            self.ball_sprites.draw(self.screen)
            self.opponent.chase_ball(self.ball)
            self.detect_powerup(OBJ_COLOR)
            self.detect_bungie()
            self.board_sprites.update()
            self.ball_sprites.update(OBJ_COLOR)
            self.powerup_sprites.update()
            self.bungie_sprites.update()

    def create_score(self, color):
        player_surface = FONT.render(str(self.player.score), True, color)
        self.screen.blit(player_surface, (660, 15))
        opponent_surface = FONT.render(str(self.opponent.score), True, color)
        self.screen.blit(opponent_surface, (600, 15))

    # detect if it is player's round upon collision with ball
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
            # purple = change board size
            if self.powerup.color == POWERUP1_COLOR:
                if self.player_round:
                    self.change_board_size(self.player, 240, color)
                    self.powerup.moveOffscreen()
                else:
                    self.change_board_size(self.opponent, 240, color)
                    self.powerup.moveOffscreen()
            # yellow = change ball speed
            elif self.powerup.color == POWERUP2_COLOR:
                self.change_ball_size(LARGE_BALL_RADIUS)
                self.powerup.moveOffscreen()
            # blue = change board speed
            elif self.powerup.color == POWERUP3_COLOR:
                if self.player_round:
                    self.change_board_speed(self.player, BOARD_SPEED_ENHANCED)
                    self.powerup.moveOffscreen()
                else:
                    self.change_board_speed(
                        self.opponent, BOARD_SPEED_ENHANCED)
                    self.powerup.moveOffscreen()

    def powerup_timer(self, color):
        self.player_size_end_time = pygame.time.get_ticks()
        self.opponent_size_end_time = pygame.time.get_ticks()
        self.player_speed_end_time = pygame.time.get_ticks()
        self.opponent_speed_end_time = pygame.time.get_ticks()
        self.ball_speed_end_time = pygame.time.get_ticks()

        if (self.player_size_end_time - self.player_size_start_time > 10000):
            self.change_board_size(self.player, 140, color)

        if (self.opponent_size_end_time - self.opponent_size_start_time > 10000):
            self.change_board_size(self.opponent, 140, color)

        if (self.player_speed_end_time - self.player_speed_start_time > 10000):
            self.change_board_speed(self.player, BOARD_SPEED_NORMAL)

        if (self.opponent_speed_end_time - self.opponent_speed_start_time > 10000):
            self.change_board_speed(self.opponent, BOARD_SPEED_NORMAL)

        if (self.ball_speed_end_time - self.ball_speed_start_time > 10000):
            self.change_ball_size(BALL_RADIUS)

        self.create_powerup_text(color)

    # change the size of the board/paddle
    def change_board_size(self, board, size, color):
        board.image = pygame.Surface((BOARD_SIZE[0], size))
        board.rect = board.image.get_rect(center=board.rect.center)
        board.image.fill(color)

        if size == 240 and board.name == "player":
            self.player_size_start_time = pygame.time.get_ticks()
        elif size == 240 and board.name == "opponent":
            self.opponent_size_start_time = pygame.time.get_ticks()

    # change the speed of the paddle
    def change_board_speed(self, board, speed):
        board.speed = speed
        if speed == BOARD_SPEED_ENHANCED and board.name == "player":
            self.player_speed_start_time = pygame.time.get_ticks()
        elif speed == BOARD_SPEED_ENHANCED and board.name == "opponent":
            self.opponent_speed_start_time = pygame.time.get_ticks()

    # change the size of the ball
    def change_ball_size(self, radius):
        self.ball.radius = radius
        self.ball.image = pygame.Surface(
            (radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.ball.image, OBJ_COLOR,
                           (radius, radius), radius)
        self.ball.rect = self.ball.image.get_rect(center=self.ball.rect.center)
        if self.ball.radius == LARGE_BALL_RADIUS:
            self.ball_speed_start_time = pygame.time.get_ticks()

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
        font = pygame.font.Font('freesansbold.ttf', 12)
        opponent_surface = font.render(str(
            "CURRENT THEME: " + theme + " (CHANGE W/ 1-4)"), True, TEXT_COLOR)
        self.screen.blit(opponent_surface, (WIDTH - WIDTH + 25, 770))

    def create_powerup_text(self, color):
        TEXT_COLOR = color
        font = pygame.font.Font('freesansbold.ttf', 16)

       # SPEED TEXT LOCATION LOGIC --> RIGHTSIDE FOR PLAYER, LEFTSIDE FOR OPP, TOP LOCATION
        if self.player.image.get_height() == 240:
            self.pl_sizeEfct = True
            text = "PLAYER SIZE INCREASE - ACTIVE"
            player_surface = font.render(str(text), True, TEXT_COLOR)
            self.screen.blit(player_surface, (WIDTH - WIDTH / 4, 15))
        if self.opponent.image.get_height() == 240:
            self.op_sizeEfct = True
            text = "OPPONENT SIZE INCREASE - ACTIVE"
            player_surface = font.render(str(text), True, TEXT_COLOR)
            self.screen.blit(player_surface, (25, 15))

       # SPEED TEXT LOCATION LOGIC --> RIGHTSIDE FOR PLAYER, MIDDLE LOCATION IF 2 EFFECTS ACTIVE
        if self.player.speed > BOARD_SPEED_NORMAL and not self.pl_sizeEfct:
            self.pl_speedEfct = True
            text = "PLAYER SPEED INCREASE - ACTIVE"
            player_surface = font.render(str(text), True, TEXT_COLOR)
            self.screen.blit(player_surface, (WIDTH - WIDTH / 4, 15))
        elif self.player.speed > BOARD_SPEED_NORMAL and self.pl_sizeEfct:
            self.pl_speedEfct = True
            text = "PLAYER SPEED INCREASE - ACTIVE"
            player_surface = font.render(str(text), True, TEXT_COLOR)
            self.screen.blit(player_surface, (WIDTH - WIDTH / 4, 35))

       # SPEED TEXT LOCATION LOGIC --> LEFTSIDE FOR OPP, MIDDLE LOCATION IF 2 EFFECTS ACTIVE
        if self.opponent.speed > BOARD_SPEED_NORMAL and not self.op_sizeEfct:
            self.op_speedEfct = True
            text = "OPPONENT SPEED INCREASE - ACTIVE"
            player_surface = font.render(str(text), True, TEXT_COLOR)
            self.screen.blit(player_surface, (25, 15))
        elif self.opponent.speed > BOARD_SPEED_NORMAL and self.op_sizeEfct:
            self.pl_speedEfct = True
            text = "OPPONENT SPEED INCREASE - ACTIVE"
            player_surface = font.render(str(text), True, TEXT_COLOR)
            self.screen.blit(player_surface, (25, 35))

        # BALL SIZE TEXT LOCATION LOGIC --> BOTTOM LOCATION IF ALL 3 EFFECTS ACTIVE, ALWAYS RIGHT SIDE
        if self.ball.radius == LARGE_BALL_RADIUS and not self.pl_sizeEfct and not self.pl_speedEfct:
            self.pl_ballEfct = True
            text = "BALL SIZE INCREASE - ACTIVE"
            player_surface = font.render(str(text), True, TEXT_COLOR)
            self.screen.blit(player_surface, (WIDTH - WIDTH / 4, 15))
        elif self.ball.radius == LARGE_BALL_RADIUS and self.pl_sizeEfct and not self.pl_speedEfct:
            self.pl_ballEfct = True
            text = "BALL SIZE INCREASE - ACTIVE"
            player_surface = font.render(str(text), True, TEXT_COLOR)
            self.screen.blit(player_surface, (WIDTH - WIDTH / 4, 35))
        elif self.ball.radius == LARGE_BALL_RADIUS and not self.pl_sizeEfct and self.pl_speedEfct:
            self.pl_ballEfct = True
            text = "BALL SIZE INCREASE - ACTIVE"
            player_surface = font.render(str(text), True, TEXT_COLOR)
            self.screen.blit(player_surface, (WIDTH - WIDTH / 4, 35))
        elif self.ball.radius == LARGE_BALL_RADIUS and self.pl_sizeEfct and self.pl_speedEfct:
            self.pl_ballEfct = True
            text = "BALL SIZE INCREASE - ACTIVE"
            player_surface = font.render(str(text), True, TEXT_COLOR)
            self.screen.blit(player_surface, (WIDTH - WIDTH / 4, 55))

    def detect_bungie(self):
        if self.ball.rect.colliderect(self.bungueBottom.rect):
            pygame.mixer.Sound.play(BUNGIE_SOUND)
            # the ball went past the bungue, hit the wall and was bounced already, so I we just need to change the speed
            if self.ball.velocity[1] > 0:
                self.ball.toggle_bungie_speed("on")
            else:
                self.ball.bounce("y", "on", "off")
        elif self.ball.rect.colliderect(self.bungueTop.rect):
            pygame.mixer.Sound.play(BUNGIE_SOUND)
            if self.ball.velocity[1] < 0:
                self.ball.toggle_bungie_speed("on")
            else:
                self.ball.bounce("y", "on", "off")

    def end_screen(self, color):
        def get_center_pos(text, font):
            surface = font.render(text, True, color)
            x = WIDTH / 2 - surface.get_size()[0] // 2
            y = HEIGHT / 2 - surface.get_size()[1] // 2
            return (x, y)

        self.screen.blit(self.fader, (0, 0))
        text = "YOU WIN!" if self.player.score >= ROUND else "YOU LOSE!"
        text_surface = END_GAME_FONT.render(text, True, color)
        self.screen.blit(text_surface, get_center_pos(text, END_GAME_FONT))
        # interpret the continuous key-stroke
        pygame.time.delay(100)

        text = "Press any key to continue"
        text_surface = FONT.render(text, True, color)
        self.screen.blit(text_surface, (get_center_pos(text, FONT)[
                         0], get_center_pos(text, FONT)[1] + 60))

    def create_logo(self, color):
        #Background image
        bg_img = pygame.image.load("media/bgrImage.png")
        bg_img = pygame.transform.scale(bg_img,(200,200))
        bg_img.set_alpha(80)
        self.screen.blit(bg_img, (WIDTH / 2 - 100, HEIGHT / 2 - 100))

        txt_surface = END_GAME_FONT.render("3D", True, color)
        txt_surface.set_alpha(80)
        self.screen.blit(txt_surface, (WIDTH/2 - 39, HEIGHT/2 - 20))
