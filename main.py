import pygame
import math
import random
import sys

pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Project 2: Arcade Game")
clock = pygame.time.Clock()

score = 0
font = pygame.font.Font(None, 40)

cat_image = pygame.image.load("assets/cat.png").convert_alpha()
dog_image = pygame.image.load("assets/dog.png").convert_alpha()
fish_image1 = pygame.image.load("assets/salmonNigiri.png").convert_alpha()
fish_image2 = pygame.image.load("assets/tunaNigiri.png").convert_alpha()

class Cat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = cat_image

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Walls:
    def __init__ (self):
        self.width = ""
        self.height = ""
        
        

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    screen.blit(cat_image, (100, 100))
    screen.blit(dog_image, (300, 100))
    screen.blit(fish_image1, (500, 100))

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
