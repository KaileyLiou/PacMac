import pygame
import math
import random

pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Project 2: Arcade Game")
clock = pygame.time.Clock()

score = 0
font = pygame.font.Font(None, 40)

cat_image = pygame.image.load("assets/cat.png").convert_alpha()
dog_image = pygame.image.load("assets/dog.png").convert_alpha()
fish_image = pygame.image.load("assets/fish.png").convert_alpha()