import pygame
import math
from hand import HandDetector
from laser import Laser


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, x_max, y_max, max_speed=5, size=(60, 60)):
        super().__init__()
        self.image = pygame.image.load(
            "..\Graphics\player.png"
        ).convert_alpha()  # Spacecraft Icon
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = max_speed
        self.x_max = x_max
        self.y_max = y_max
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 300  # ms

        self.lasers = pygame.sprite.Group()

    def get_input(self):
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        elif keys[pygame.K_d]:
            self.rect.x += self.speed
        elif keys[pygame.K_w]:
            self.rect.y -= self.speed
        elif keys[pygame.K_s]:
            self.rect.y += self.speed

        # Laser
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
    
    def get_hand(self, dx, dy):
        # hand_speed = math.sqrt(dx**2 * dy**2)
        # if hand_speed != 0:
        #     if  hand_speed > self.speed:
        #         self.rect.x += dx / hand_speed * self.speed
        #         self.rect.y += dy / hand_speed * self.speed
        #     else:
        #         self.rect.x += dx / hand_speed
        #         self.rect.y += dy / hand_speed
        # else:
        #     pass
        self.rect.x += dx * self.speed/2
        self.rect.y += dy * self.speed/2

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.x_max:
            self.rect.right = self.x_max
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.y_max:
            self.rect.bottom = self.y_max

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, self.y_max))

    def update(self, dx, dy):
        self.get_input()
        self.get_hand(dx, dy)
        self.constraint()
        self.recharge()
        self.lasers.update()
