import pygame

HEIGHT = 800
WIDTH = 1280
FPS = 60

BG_COLOR = pygame.Color('grey12')
BALL_RADIUS = 20
BOARD_SIZE = (10, 140)
OBJ_COLOR = (200, 200, 200)

# POWERUP CONSTS
POWERUP_SIZE = (50, 50)
POWERUP1_COLOR = (200, 0, 200)
POWERUP2_COLOR = (255, 255, 0)
POWERUP3_COLOR = (0, 255, 255)
COLOR_LIST = [POWERUP1_COLOR, POWERUP2_COLOR, POWERUP3_COLOR]

# sounds
PONG_SOUND = pygame.mixer.Sound("./lecture_code/media/pong.ogg")
SCORE_SOUND = pygame.mixer.Sound("./lecture_code/media/score.ogg")