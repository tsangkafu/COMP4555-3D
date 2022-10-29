import pygame
import globals
import sprites

#################################################################

pygame.init()
screen = pygame.display.set_mode((globals.DISPLAY_WIDTH, globals.DISPLAY_HEIGHT)) 
pygame.display.set_caption("Space Invaders")

sprites = sprites.Sprites(screen)

while 1==1: sprites.animate()