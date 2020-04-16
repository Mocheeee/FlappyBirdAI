import pygame
from constants import *
WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(IMG_PATH['bird']['bird1'])) ,
    pygame.transform.scale2x(pygame.image.load(IMG_PATH['bird']['bird2'])) ,
    pygame.transform.scale2x(pygame.image.load(IMG_PATH['bird']['bird3']))
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(IMG_PATH['pipe']))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(IMG_PATH['base']))
BACKGOURD_IMG = pygame.transform.scale2x(pygame.image.load(IMG_PATH['backgroud']))

STAT_FONT = pygame.font.SysFont('comicsans', 50)

MUTATE_RATE = 0.8
POPULATION_SIZE = 50
POOL_SIZE = 100
MAX_GENERATIONS = 100
MAX_SCORE = 100

WEIGHT_STDEV = 0
WEIGHT_MEAN = 1

BIAS_STDEV = 0
BIAS_MEAN = 1