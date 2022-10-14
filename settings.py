import pygame

HEIGHT = 800
WIDTH = 1280
FPS = 60


# Color Themes
# Default
BG_DEF = pygame.Color('grey12')
OBJ_DEF = (200, 200, 200)
# Green
BG_GRN = (22, 46, 20)
OBJ_GRN = (23, 92, 17)
# Blue
BG_BLU = (17, 28, 56)
OBJ_BLU = (5, 46, 150)
# Red
BG_RED = (56, 24, 24)
OBJ_RED = (138, 7, 7)

BALL_RADIUS = 20
BOARD_SIZE = (10, 140)
BG_COLOR = BG_DEF
OBJ_COLOR = OBJ_DEF

# POWERUP CONSTS
POWERUP_SIZE = (50, 50)
POWERUP1_COLOR = (200, 0, 200)
POWERUP2_COLOR = (255, 255, 0)
POWERUP3_COLOR = (0, 255, 255)
COLOR_LIST = [POWERUP1_COLOR, POWERUP2_COLOR, POWERUP3_COLOR]

# sounds
PONG_SOUND = pygame.mixer.Sound("./media/pong.ogg")
SCORE_SOUND = pygame.mixer.Sound("./media/score.ogg")
POWERUP_SOUND = pygame.mixer.Sound("./media/powerup.ogg")