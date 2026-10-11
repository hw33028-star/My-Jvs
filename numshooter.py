import pygame
import sys
import random
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW= (255, 255, 0)
BLUE  = (50, 150, 255)
RED   = (255, 80, 80)

# Store bullets, fragments, and targets
bullets = []
fragments = []
targets = []

# Player character
player_x, player_y = 400, 550
player_speed = 5

# Score
score = 0

# Spawn target function
def spawn_target():
    x = random.randint(50, 750)
    y = 50
    dx = random.choice([-2, 2])
    text = str(random.randint(10, 99))
    targets.append({"x": x, "y": y, "dx": dx, "text": text})

# Game loop
spawn_timer = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Shoot bullet
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            num = str(random.randint(10, 999))  # bullet number
            bullet = {"x": player_x, "y": player_y-30, "text": num, "speed": -6}
            bullets.append(bullet)

    # Movement keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 20:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < 780:
        player_x += player_speed

    # Spawn targets periodically
    spawn_timer += 1
    if spawn_timer > 120:  # every ~2 seconds
        spawn_target()
        spawn_timer = 0

    # Move targets
    for target in targets:
        target["x"] += target["dx"]
        if target["x"] < 20 or target["x"] > 760:
            target["dx"] *= -1  # bounce back

    # Move bullets
    for bullet in bullets[:]:
        bullet["y"] += bullet["speed"]

        # Check collision with targets
        for target in targets[:]:
            text_img = font.render(target["text"], True, RED)
            target_rect = text_img.get_rect(center=(target["x"], target["y"]))
            bullet_rect = font.render(bullet["text"], True, YELLOW).get_rect(center=(bullet["x"], bullet["y"]))

            if bullet_rect.colliderect(target_rect):
                # Explode into digits
                digits = list(bullet["text"])
                for d in digits:
                    angle = random.uniform(0, 2*math.pi)
                    speed = random.uniform(2, 5)
                    fragments.append({
                        "x": bullet["x"], 
                        "y": bullet["y"], 
                        "dx": math.cos(angle)*speed,
                        "dy": math.sin(angle)*speed,
                        "text": d,
                        "life": 60
                    })
                bullets.remove(bullet)
                targets.remove(target)
                score += 10
                break

        # Remove if off screen
        if bullet in bullets and bullet["y"] < 0:
            bullets.remove(bullet)

    # Move fragments
    for frag in fragments[:]:
        frag["x"] += frag["dx"]
        frag["y"] += frag["dy"]
        frag["dy"] += 0.05  # gravity
        frag["life"] -= 1
        if frag["life"] <= 0:
            fragments.remove(frag)

    # Draw everything
    screen.fill(BLACK)

    # Player
    pygame.draw.rect(screen, BLUE, (player_x-15, player_y-30, 30, 30))  # body
    pygame.draw.rect(screen, WHITE, (player_x-5, player_y-50, 10, 20))   # gun

    # Bullets
    for bullet in bullets:
        text_img = font.render(bullet["text"], True, YELLOW)
        screen.blit(text_img, (bullet["x"], bullet["y"]))

    # Fragments
    for frag in fragments:
        text_img = font.render(frag["text"], True, YELLOW)
        screen.blit(text_img, (frag["x"], frag["y"]))

    # Targets
    for target in targets:
        text_img = font.render(target["text"], True, RED)
        screen.blit(text_img, (target["x"], target["y"]))

    # Score
    score_img = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_img, (10, 10))

    pygame.display.flip()
    clock.tick(60)
