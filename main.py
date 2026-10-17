# ==========================================
# Project 2 PacMac Explanation
# ==========================================
# Vectors:
# The cat, dogs, and fish store their position and velocity as pygame.Vector2 objects

# Distance:
# Each dog uses distance_to() to measure how far away the cat is
# A dog only starts chasing when the cat is within the range

# Normalization:
# A dog subtracts its position from the cat's position to get a vector pointing at the cat
# normalize() removes the distance so the dog always chases at the same speed
# Fish do the same with the mouse position

# Angles:
# When a dog picks a new direction, it picks a random angle and turns it into a direction vector with cosine and sine

# Velocity and acceleration:
# The arrow keys create an acceleration vector for the cat
# In every frame velocity += acceleration and velocity *= drag
# Speed is capped at max_speed and position += velocity
# The cat slides a bit before stopping because of the drag

# Dot product:
# Each dog compares the direction it is facing with the direction to the cat
# If the dot product is above the threshold,the cat is inside the dog's field of view

# AI decision-making:
# Perception: distance to the cat + dot product of facing vs. cat direction
# Decision: if distance < range and dot > threshold then "chase", else "patrol"
# Action: chase = move toward the cat, patrol = go in random directions
# ==========================================

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
time_left = 5400
game_state = "start"
font = pygame.font.Font(None, 40)
big_font = pygame.font.Font(None, 100)

#IMAGE LINKING
cat_image = pygame.image.load("assets/cat.png").convert_alpha()
dog_image = pygame.image.load("assets/dog.png").convert_alpha()
fish_image1 = pygame.image.load("assets/salmonNigiri.png").convert_alpha()
fish_image2 = pygame.image.load("assets/tunaNigiri.png").convert_alpha()
fish_image3 = pygame.image.load("assets/sushiRoll1.png").convert_alpha()
fish_image4 = pygame.image.load("assets/sushiRoll2.png").convert_alpha()
wall_image = pygame.image.load("assets/wallBlock.png").convert_alpha()
portal_image = pygame.image.load("assets/portal.png").convert_alpha()
bg_image = pygame.image.load("assets/bg_image.png").convert_alpha()

#IMAGE SCALING
cat_image = pygame.transform.scale(cat_image, (100, 100))
dog_image = pygame.transform.scale(dog_image, (80, 80))
fish_image1 = pygame.transform.scale(fish_image1, (50, 50))
fish_image2 = pygame.transform.scale(fish_image2, (50, 50))
fish_image3 = pygame.transform.scale(fish_image3, (50, 50))
fish_image4 = pygame.transform.scale(fish_image4, (50, 50))
wall_image = pygame.transform.scale(wall_image, (50, 50))
portal_image = pygame.transform.scale(portal_image, (80, 80))
bg_image = pygame.transform.scale(bg_image, (1200, 800))

# sounds
fish_collection_sound = pygame.mixer.Sound("assets/collection.ogg.ogg")
game_music = pygame.mixer.Sound("assets/music.ogg.ogg")
portal_mist_sound = pygame.mixer.Sound("assets/portal.ogg.ogg")

#CLASSESSSSSS
class Cat:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.image = cat_image
        self.acceleration_strength = 0.8
        self.drag = 0.9
        self.max_speed = 6
        self.speed_timer = 0
        self.invincibility_timer = 0
        self.portal_ready = True
        self.can_shoot = False

    def get_rect(self):
        return self.image.get_rect(topleft=(self.position.x, self.position.y))

    def update(self, keys, walls):
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

        # move x and y separately so the cat slides along walls
        self.position.x += self.velocity.x
        if any(wall.get_rect().colliderect(self.get_rect()) for wall in walls):
            self.position.x -= self.velocity.x
            self.velocity.x = 0

        self.position.y += self.velocity.y
        if any(wall.get_rect().colliderect(self.get_rect()) for wall in walls):
            self.position.y -= self.velocity.y
            self.velocity.y = 0

        self.position.x = max(0, min(self.position.x, 1200 - self.image.get_width()))
        self.position.y = max(0, min(self.position.y, 800 - self.image.get_height()))

        if self.speed_timer > 0:
            self.speed_timer -= 1
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1

        if self.speed_timer > 0:
            self.max_speed = 10
        else:
            self.max_speed = 6

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
        self.stun_timer = 0

    def get_rect(self):
        return self.image.get_rect(topleft=(self.position.x, self.position.y))

    def update(self, cat, walls):
        if self.stun_timer > 0:
            self.stun_timer -= 1
            self.velocity = pygame.Vector2(0, 0)
            return False

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

        # turn around if dog hits a wall
        self.position.x += self.velocity.x
        if any(wall.get_rect().colliderect(self.get_rect()) for wall in walls):
            self.position.x -= self.velocity.x
            self.direction.x *= -1

        self.position.y += self.velocity.y
        if any(wall.get_rect().colliderect(self.get_rect()) for wall in walls):
            self.position.y -= self.velocity.y
            self.direction.y *= -1

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

# fish class for buffs and projectiles
class Sushi:
    def __init__(self, x, y, sushi_type):
        self.x = x
        self.y = y
        self.sushi_type = sushi_type
        if sushi_type == "salmon":
            self.image = fish_image1
        elif sushi_type == "tuna":
            self.image = fish_image2
        elif sushi_type == "fish3":
            self.image = fish_image3
        else:
            self.image = fish_image4
        self.collected = False
        self.flying = False
        self.velocity = pygame.Vector2(0, 0)

    def get_type(self):
        return self.sushi_type

    def get_rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        if self.collected == False:
            screen.blit(self.image, (self.x, self.y))
   
    def check_if_collected(self, screen, player):
        global score
        if self.collected == False and self.flying == False and player.get_rect().colliderect(self.get_rect()):
            self.collected = True
            fish_collection_sound.play()
            self.apply_buff(player)
            score += 1

    def apply_buff(self, player):
        if self.sushi_type == "tuna":
            player.speed_timer = 600
        elif self.sushi_type == "fish3":
            player.invincibility_timer = 300
        elif self.sushi_type == "fish4":
            player.can_shoot = True

    def shoot(self, target_x, target_y):
        self.velocity = pygame.Vector2(target_x - self.x, target_y - self.y)
        if self.velocity.length() > 0:
            self.velocity.scale_to_length(12)
        self.flying = True

    def move(self, dogs):
        global score
        if self.collected == True:
            return
        self.x += self.velocity.x
        self.y += self.velocity.y
        if self.x < 0 or self.x > 1200 or self.y < 0 or self.y > 800:
            self.collected = True
        for dog in dogs:
            if self.collected == False and self.get_rect().colliderect(dog.get_rect()):
                self.collected = True
                dog.stun_timer = 180 # dog is frozen for 3 seconds
                score += 2

class Walls:
    def __init__ (self):
        self.position_X = 25 * random.randint(0, 23)
        self.position_Y = 25 * random.randint(0, 15)
        self.image = wall_image
        self.VectorWall = pygame.math.Vector2(self.position_X, self.position_Y)

    def get_rect(self):
            return self.image.get_rect(topleft=(self.VectorWall))

    def draw(self, screen):
        screen.blit(self.image, self.VectorWall)

# portal class for tp
class Portal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = portal_image
        self.move_timer = 1800

    def get_rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def teleport(p1, p2, player):
        touching1 = p1.get_rect().colliderect(player.get_rect())
        touching2 = p2.get_rect().colliderect(player.get_rect())

        if not touching1 and not touching2:
            player.portal_ready = True
            return
        if player.portal_ready == False:
            return

        if touching1:
            player.position = pygame.Vector2(p2.x, p2.y)
        else:
            player.position = pygame.Vector2(p1.x, p1.y)
        player.portal_ready = False
        portal_mist_sound.play()

    def update(portal, walls):
        portal.move_timer -= 1
        if portal.move_timer <= 0:
            portal.move_timer = 1800
            while True:
                portal.x = random.randint(0, 1120)
                portal.y = random.randint(0, 720)
                if not any(wall.get_rect().colliderect(portal.get_rect().inflate(60, 60)) for wall in walls):
                    break
            portal_mist_sound.play()

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
while len(walls) < numWalls:
    wall = Walls()
    on_something = wall.get_rect().colliderect(cat.get_rect().inflate(100, 100))
    on_something = on_something or wall.get_rect().colliderect(pygame.Rect(600, 400, 50, 50).inflate(60, 60))
    for dog in dogs:
        if wall.get_rect().colliderect(dog.get_rect().inflate(60, 60)):
            on_something = True
    if on_something == False:
        walls.append(wall)

# portals
portal1 = Portal(200, 600)
portal2 = Portal(1000, 100)

# make sushi method; more salmon than anything else
def new_sushi():
    sushi_type = random.choice(["salmon", "salmon", "salmon", "salmon", "salmon", "salmon", "tuna", "fish3"])
    while True:
        sushi = Sushi(random.randint(0, 1150), random.randint(0, 750), sushi_type)
        if not any(wall.get_rect().colliderect(sushi.get_rect()) for wall in walls):
            return sushi

# make 20 sushi
sushis = []
for s in range(19):
    sushis.append(new_sushi())
sushis.append(Sushi(600, 400, "fish4"))
shots = []

# start screen
x_button = pygame.Rect(930, 130, 50, 50)
overlay = pygame.Surface((1200, 800))
overlay.set_alpha(190)
overlay.fill((0, 0, 0))

game_music.set_volume(0.4)
game_music.play(loops = -1)

#Game Start
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == "start" and event.type == pygame.MOUSEBUTTONDOWN and x_button.collidepoint(event.pos):
            game_state = "playing"
        if game_state == "playing" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and cat.can_shoot:
            shot = Sushi(cat.position.x + 25, cat.position.y + 25, "salmon")
            mouse_x, mouse_y = pygame.mouse.get_pos()
            shot.shoot(mouse_x, mouse_y)
            shots.append(shot)
    keys = pygame.key.get_pressed()

    if game_state == "playing":
        cat.update(keys, walls)
        for dog in dogs:
            touched_cat = dog.update(cat, walls)

            if touched_cat and cat.invincibility_timer == 0:
                lives -= 1
                cat.invincibility_timer = 120

                cat.position = pygame.Vector2(100, 100)
                cat.velocity = pygame.Vector2(0, 0)

        for sushi in sushis:
            sushi.check_if_collected(screen, cat)

        for shot in shots:
            shot.move(dogs)

        portal1.update(walls)
        portal2.update(walls)
        portal1.teleport(portal2, cat)

        time_left -= 1

        if all(sushi.collected for sushi in sushis):
            game_state = "win"
            game_music.stop()
        elif lives <= 0 or time_left <= 0:
            game_state = "lose"
            game_music.stop()

    #RENDERING
    screen.blit(bg_image, (0, 0))
    # fish render
    for sushi in sushis:
        sushi.draw(screen)

    for shot in shots:
        shot.draw(screen)
    # portal render
    portal1.draw(screen)
    portal2.draw(screen)
    #cat render
    cat.draw(screen)  
    #dog render
    for dog in dogs:
        dog.draw(screen)
    #wall render
    for wall in walls:
        wall.draw(screen)
    #TEXTT
    fish_collected = sum(1 for sushi in sushis if sushi.collected)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
    fish_text = font.render(f"Fish: {fish_collected}/{len(sushis)}", True, (0, 0, 0))
    time_text = font.render(f"Time: {time_left // 60}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))
    screen.blit(fish_text, (10, 90))
    screen.blit(time_text, (10, 130))
    if cat.can_shoot:
        shoot_text = font.render("Left click to shoot!", True, (0, 0, 0))
        screen.blit(shoot_text, (10, 170))

    #START SCREEN
    if game_state == "start":
        screen.blit(overlay, (0, 0))
        pygame.draw.rect(screen, (40, 40, 40), (220, 120, 760, 560))
        pygame.draw.rect(screen, (255, 255, 255), (220, 120, 760, 560), 4)
        pygame.draw.rect(screen, (200, 40, 40), x_button)
        x_text = font.render("X", True, (255, 255, 255))
        screen.blit(x_text, (x_button.centerx - x_text.get_width() // 2, x_button.centery - x_text.get_height() // 2))

        title_text = big_font.render("PacMac", True, (255, 255, 255))
        screen.blit(title_text, (600 - title_text.get_width() // 2, 150))
        instructions = [
            "You woke up today and now you're a cat!",
            "Collect all the sushi before time runs out.",
            "Avoid the 4 dogs. You have 9 lives.",
            "Arrow keys: move the cat",
            "Tuna: speed boost    First roll: invincibility",
            "Special roll: unlocks left click to shoot sushi",
            "and freeze the dogs",
            "Step on a portal to teleport to the other one",
            "Click the X to start!"
        ]
        y = 280
        for line in instructions:
            line_text = font.render(line, True, (255, 255, 255))
            screen.blit(line_text, (600 - line_text.get_width() // 2, y))
            y += 45

    #END SCREENS
    if game_state == "win" or game_state == "lose":
        screen.blit(overlay, (0, 0))
        if game_state == "win":
            end_text = big_font.render("YOU WIN!", True, (120, 255, 120))
        else:
            end_text = big_font.render("GAME OVER", True, (255, 90, 90))
        score_end_text = font.render(f"Final score: {score}   Fish: {fish_collected}/{len(sushis)}", True, (255, 255, 255))
        screen.blit(end_text, (600 - end_text.get_width() // 2, 300))
        screen.blit(score_end_text, (600 - score_end_text.get_width() // 2, 420))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()