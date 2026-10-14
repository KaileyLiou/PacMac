import pygame
import math
import random
import sys

pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Project 2: Arcade Game")
clock = pygame.time.Clock()

#Variables
score = 0
lives = 9
numWalls = 10
font = pygame.font.Font(None, 40)

#IMAGE LINKING
cat_image = pygame.image.load("assets/cat.png").convert_alpha()
cat_image = pygame.transform.scale(cat_image, (100, 100))
dog_image = pygame.image.load("assets/dog.png").convert_alpha()
dog_image = pygame.transform.scale(dog_image, (80, 80))
fish_image1 = pygame.image.load("assets/salmonNigiri.png").convert_alpha()
fish_image2 = pygame.image.load("assets/tunaNigiri.png").convert_alpha()
wall_image = pygame.image.load("assets/wallBlock.png").convert_alpha()
wall_image = pygame.transform.scale(wall_image, (25, 25))

#CLASSESSSSSS
class Cat:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.image = cat_image
        self.acceleration_strength = 0.8
        self.drag = 0.9
        self.max_speed = 6

    def get_rect(self):
        return self.image.get_rect(topleft=(self.position.x, self.position.y))

    def update(self, keys):
        acceleration = pygame.Vector2(0, 0)
        if keys[pygame.K_LEFT]:
            acceleration.x -= 1
        if keys[pygame.K_RIGHT]:
            acceleration.x += 1
        if keys[pygame.K_UP]:
            acceleration.y -= 1
        if keys[pygame.K_DOWN]:
            acceleration.y += 1

        if acceleration.length() > 0:
            acceleration = acceleration.normalize() * self.acceleration_strength

        self.velocity += acceleration
        self.velocity *= self.drag
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.position += self.velocity
        self.position.x = max(0, min(self.position.x, 1200 - self.image.get_width()))
        self.position.y = max(0, min(self.position.y, 800 - self.image.get_height()))

    def draw(self, screen):
        screen.blit(self.image, (self.position.x, self.position.y))
class Dog:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.direction = pygame.Vector2(1, 0)
        self.image = dog_image
        self.speed = 2
        self.chase_range = 300
        self.state = "patrol"
        self.patrol_timer = 0

    def get_rect(self):
        return self.image.get_rect(topleft=(self.position.x, self.position.y))

    def update(self, cat):
        cat_center = pygame.Vector2(cat.get_rect().center)
        dog_center = pygame.Vector2(self.get_rect().center)

        difference = cat_center - dog_center
        distance = dog_center.distance_to(cat_center)

        if distance > 0:
            direction_to_cat = difference.normalize()
            dot_product = self.direction.dot(direction_to_cat)
        else:
            direction_to_cat = pygame.Vector2(0, 0)
            dot_product = 1

        if distance < self.chase_range and dot_product > 0.5:
            self.state = "chase"
        else:
            self.state = "patrol"

        if self.state == "chase":
            self.velocity = direction_to_cat * self.speed

            if distance > 0:
                self.direction = direction_to_cat

        else:
            self.patrol_timer += 1

            if self.patrol_timer >= 90:
                angle = random.uniform(0, 2 * math.pi)

                self.direction = pygame.Vector2(
                    math.cos(angle),
                    math.sin(angle)
                )

                self.patrol_timer = 0

            self.velocity = self.direction * self.speed

        self.position += self.velocity

        max_x = max(0, 1200 - self.image.get_width())
        max_y = max(0, 800 - self.image.get_height())

        if self.position.x < 0 or self.position.x > max_x:
            self.position.x = max(0, min(self.position.x, max_x))
            self.direction.x *= -1

        if self.position.y < 0 or self.position.y > max_y:
            self.position.y = max(0, min(self.position.y, max_y))
            self.direction.y *= -1

        return self.get_rect().colliderect(cat.get_rect())

    def draw(self, screen):
        screen.blit(self.image, (self.position.x, self.position.y))
class Walls:
    def __init__ (self):
        self.position_X = 25 * random.randint(0, 47)
        self.position_Y = 25 * random.randint(0, 31)
        self.image = wall_image
        self.VectorWall = pygame.math.Vector2(self.position_X, self.position_Y)

    def get_rect(self):
            return self.image.get_rect(topleft=(self.VectorWall))

    def draw(self, screen):
        screen.blit(self.image, self.VectorWall)

#GAME OBJECT CREATION
#Cat
cat = Cat(100, 100)
#dog
dogs = [Dog(300, 100),
        Dog(800, 150),
        Dog(400, 600),
        Dog(1000, 600)]
#Walls
walls = []
for w in range(10):
    wall = Walls()
    walls.append(wall)

invincibility_timer = 0

#Game Start
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    
    #player updates
    cat.update(keys)
    
    #wall-cat collision
    for wall in walls:
        if wall.get_rect().colliderect(cat.get_rect()):
            #check x vel
            if cat.velocity.x > 0:
                cat.get_rect().right = wall.get_rect().left
            if cat.velocity.x < 0:
                cat.get_rect().left = wall.get_rect().right

            #check y vel
            if cat.velocity.y > 0:
                cat.get_rect().top = wall.get_rect().bottom
            if cat.velocity.y < 0:
                cat.get_rect().bottom = wall.get_rect().top

    #dog-cat collision (attack)
    for dog in dogs:
        touched_cat = dog.update(cat)

        if touched_cat and invincibility_timer == 0:
            lives -= 1
            invincibility_timer = 120

            cat.position = pygame.Vector2(100, 100)
            cat.velocity = pygame.Vector2(0, 0)

    #invincibility Cooldown
    if invincibility_timer > 0:
        invincibility_timer -= 1
    
    #game over if lives r out
    if lives <= 0:
        running = False

    #RENDERING
    screen.fill((255, 255, 255))
    #cat render
    cat.draw(screen)  
    #dog render
    for dog in dogs:
        dog.draw(screen)
    #wall render
    for wall in walls:
        wall.draw(screen)
    #TEXTT
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
