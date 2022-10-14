import pygame

HEIGHT = 800
WIDTH = 1280
FPS = 60

BG_COLOR = pygame.Color('grey12')
BALL_RADIUS = 20
LARGE_BALL_RADIUS = 40
BALL_SPEED_NORMAL = float(7)
BALL_SPEED_ENHANCED = 20
BALL_SPEED_BUNGIE = 10
BOARD_SIZE = (20, 140)
OBJ_COLOR = (200, 200, 200)

# POWERUP CONSTS
POWERUP_SIZE = (50, 50)
POWERUP1_COLOR = (200, 0, 200)
POWERUP2_COLOR = (255, 255, 0)
POWERUP3_COLOR = (0, 255, 255)
COLOR_LIST = [POWERUP1_COLOR, POWERUP2_COLOR, POWERUP3_COLOR]

# BUNGUE CONSTS
BUNGIE_SIZE = (180, 10)
BUNGUE_COLOR = (7, 143, 226)

# sounds
PONG_SOUND = pygame.mixer.Sound("./media/pong.ogg")
SCORE_SOUND = pygame.mixer.Sound("./media/score.ogg")
POWERUP_SOUND = pygame.mixer.Sound("./media/powerup.ogg")
BUNGIE_SOUND = pygame.mixer.Sound("./media/bungie.ogg")