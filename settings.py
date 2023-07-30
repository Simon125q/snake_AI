import pygame
from collections import namedtuple

pygame.init()

# basic settings
CELL_SIZE = 40
ROWS = 22
COLUMNS = 30
WINDOW_SIZE = WIDTH, HEIGHT = (COLUMNS * CELL_SIZE, ROWS * CELL_SIZE)
FPS = 100

screen = pygame.display.set_mode(WINDOW_SIZE)

# colors
GREEN = (175, 215, 70)
DARK_GREEN = (185, 225, 80)
RED = (255, 0, 0)
BLUE = '#0021f3'
DARK_BLUE = '#05014a'

# movement directions
RIGHT = [1, 0]
LEFT = [-1, 0]
UP = [0, -1]
DOWN = [0, 1]

# actions
STRAIGHT = [1, 0, 0]
RIGHT_TURN = [0, 1, 0]
LEFT_TURN = [0, 0 ,1]

# agent settings
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001

# point
Point = namedtuple('point', 'x, y')

# apple sprites
APPLE_RED = pygame.image.load('./graphics/apple_red.png').convert_alpha()
APPLE_RED = pygame.transform.scale(APPLE_RED, (CELL_SIZE, CELL_SIZE))
APPLE_GOLD = pygame.image.load('./graphics/apple_goldv2.png').convert_alpha()
APPLE_GOLD = pygame.transform.scale(APPLE_GOLD, (CELL_SIZE, CELL_SIZE))