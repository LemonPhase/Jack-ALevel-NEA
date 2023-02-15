import pygame
import math


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, y_max, laser_speed=15, angle=0, dimension=(4, 20)):
        super().__init__()
        self.image = pygame.Surface(dimension)
        self.image.fill("white")
        self.rect = self.image.get_rect(center=pos)
        self.laser_speed = laser_speed
        self.y_max = y_max
        self.angle = angle

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.y_max + 50:
            self.kill()

    def move(self):
        self.rect.y -= math.cos(self.angle) * self.laser_speed
        self.rect.x -= math.sin(self.angle) * self.laser_speed

    def update(self):
        self.move()
        self.destroy()


class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos, y_max, laser_speed=-5):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill("white")
        self.rect = self.image.get_rect(center=pos)
        self.laser_speed = laser_speed
        self.y_max = y_max

    def detonate(self):
        if self.rect.y >= 350:
            self.kill()

    def update(self):
        super().update()
        print(self.rect.y)
        self.detonate()
