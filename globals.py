import os
import pygame

pygame.init() # <- ? does this go here
pygame.mixer.pre_init(44100, -16, 2, 512)

DISPLAY_WIDTH = 1440
DISPLAY_HEIGHT = 890
IMAGE_SCALE = 0.7
TILE = 90

# SOUNDS
POWERUP_SOUND = pygame.mixer.Sound("./Audio/sfx/forceField_003.ogg")
# PLAYER SOUNDS
NORMAL_LASER_SOUND = pygame.mixer.Sound("./Audio/sfx/laserSmall_002.ogg")
TWIN_LASER_SOUND = pygame.mixer.Sound("./Audio/sfx/laserSmall_003.ogg")
PLAYER_EXPLOSION_SOUND = pygame.mixer.Sound("./Audio/sfx/explosionCrunch_004.ogg")
PLAYER_HIT_SOUND = pygame.mixer.Sound("./Audio/sfx/impactPlate_medium_002.ogg")
# ENEMY SOUNDS
SMALL_ENEMY_LASER_SOUND = pygame.mixer.Sound("./Audio/sfx/laserSmall_004.ogg")
SMALL_ENEMY_EXPLOSION_SOUND = pygame.mixer.Sound("./Audio/sfx/explosionCrunch_000.ogg")
ENEMY_HIT_SOUND = pygame.mixer.Sound("./Audio/sfx/impactPlate_medium_001.ogg")
# EXPLOSION
EXPLOSION_SOUND = pygame.mixer.Sound("./Audio/sfx/explosionCrunch_000.ogg")
# MUSIC
LEVEL_1_MUSIC = "./Audio/music/level1.mp3"
LEVEL_2_MUSIC = "./Audio/music/level2.mp3"
LEVEL_3_MUSIC = "./Audio/music/level3.mp3"

# SET VOLUME
pygame.mixer.music.set_volume(0.5)

NORMAL_LASER_SOUND.set_volume(0.20)
TWIN_LASER_SOUND.set_volume(0.25)
SMALL_ENEMY_LASER_SOUND.set_volume(0.25)
POWERUP_SOUND.set_volume(0.12)
EXPLOSION_SOUND.set_volume(0.04)
PLAYER_EXPLOSION_SOUND.set_volume(0.15)
PLAYER_HIT_SOUND.set_volume(0.20)
ENEMY_HIT_SOUND.set_volume(0.15)

def count_image(path):
    count = 0
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)): count += 1
    return count

def scale_image(image):
    return pygame.transform.smoothscale(image, (image.get_width() * IMAGE_SCALE, image.get_height() * IMAGE_SCALE)).convert_alpha()