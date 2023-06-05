import pygame
import sys
import random

from bullet import Bullet
from level import Level
from settings import *

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_map, screen)

font = pygame.font.Font("graphics/fonts/BASKVILL.TTF", 32)
lives = 1000

pygame.mixer.music.load("sounds/music/space_invaders_music.mp3")
pygame.mixer.music.play(-1)


# Enemy shooting logic
def enemy_shoot(enemies, projectiles):
    for enemy in enemies:
        # Determine the conditions for enemy shooting
        if random.randint(1, 100) == 1:  # Random chance to shoot
            # Create a new enemy projectile using the Bullet class
            projectile = Bullet(enemy.rect.center, -1)  # Set the direction to 1 for upward movement
            projectiles.add(projectile)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("black")

    level.run()

    # Update enemy positions
    level.enemies.update()

    # Handle enemy shooting logic
    enemy_shoot(level.enemies, level.enemy_projectiles)

    # Update projectile positions
    level.enemy_projectiles.update()

    # Draw everything on the screen
    level.tiles.draw(screen)
    level.player.draw(screen)
    level.enemies.draw(screen)
    level.player.sprite.draw_bullets(screen)
    level.enemy_projectiles.draw(screen)

    level.check_bullet_collisions()

    lives -= 1
    text = font.render(str(lives), True, (0, 255, 0))
    screen.blit(text, (0, 0))

    #if lives == 0:
        #sys.exit()

    pygame.display.update()
    clock.tick(fps)
