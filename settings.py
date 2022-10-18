import pygame
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)

HEIGHT = 800
WIDTH = 1280
FPS = 60
ROUND = 5

# Color Themes
# Default
BG_DEF = pygame.Color('grey12')
OBJ_DEF = (200, 200, 200)
# Green
BG_GRN = (22, 46, 20)
OBJ_GRN = (0, 184, 49)
# Blue
BG_BLU = (17, 28, 56)
OBJ_BLU = (0, 68, 242)
# Red
BG_RED = (56, 24, 24)
OBJ_RED = (176, 2, 2)

BALL_RADIUS = 20
LARGE_BALL_RADIUS = 40
BOARD_SPEED_NORMAL = 10
BOARD_SPEED_ENHANCED = 20
BALL_SPEED_NORMAL = 13
BALL_SPEED_BUNGIE = 20
BOARD_SIZE = (20, 140)
BG_COLOR = BG_DEF
OBJ_COLOR = OBJ_DEF

# POWERUP CONSTS
POWERUP_SIZE = (80, 80)
POWERUP1_COLOR = (200, 0, 200)
POWERUP2_COLOR = (255, 255, 0)
POWERUP3_COLOR = (0, 255, 255)
COLOR_LIST = [POWERUP1_COLOR, POWERUP2_COLOR, POWERUP3_COLOR]

# BUNGUE CONSTS
BUNGIE_SIZE = (180, 10)
BUNGIE_COLOR = (7, 143, 226)

# SOUNDS
PONG_SOUND = pygame.mixer.Sound("./media/pong.ogg")
SCORE_SOUND = pygame.mixer.Sound("./media/score.ogg")
POWERUP_SOUND = pygame.mixer.Sound("./media/powerup.ogg")
BUNGIE_SOUND = pygame.mixer.Sound("./media/bungie.ogg")
CRITICAL_SOUND = pygame.mixer.Sound("./media/smash.ogg")
CRITICAL_SOUND.set_volume(0.55)