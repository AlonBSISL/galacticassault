import pygame
from settings import screen_width


class Bullet(pygame.sprite.Sprite):

    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.Surface((10, 30))  # Swap the width and height to make the bullet taller
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft=pos)
        if direction == 0:
            direction = 1
        self.speed = 10
        self.direction = pygame.math.Vector2(0, -direction * self.speed)  # Make the bullet move upwards

    def update(self):
        self.rect.y += self.direction.y
        if self.rect.y > screen_width or self.rect.y < 30:
            self.kill()
