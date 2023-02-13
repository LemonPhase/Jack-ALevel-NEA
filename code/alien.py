import pygame
import random


class Alien(pygame.sprite.Sprite):
    def __init__(self, x_max, y_max, size=(75, 75)):
        super().__init__()
        self.rect = self.image.get_rect(midtop=(random.randint(0, x_max), 10))
        self.x_max = x_max
        self.y_max = y_max
        self.ready = True
        self.attack_time = 0
        self.attack_cooldown = 2000  # ms
        self.moving = False
        self.speed = 3

    def move(self):
        current_time = pygame.time.get_ticks()
        if self.moving and current_time - self.move_time < self.move_cooldown:
            self.rect.x += self.speed
            if self.rect.left <= 0 or self.rect.right >= self.x_max:
                self.moving = False

        else:
            self.moving = True
            self.move_time = current_time
            self.move_cooldown = random.randint(0, 4000)
            self.speed = self.speed * -1

    def attack(self):
        pass

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

    def update(self):
        self.move()
        self.attack()
        self.recharge
        self.constraint()


class Ax(Alien):
    def __init__(self, x_max, y_max, size=(75, 75), speed=3):
        file_path = f"..\Graphics\Ax.png"
        self.image = pygame.image.load(file_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        super().__init__(x_max, y_max, size)
        self.move_time = 0
        self.move_cooldown = random.randint(0, 4000)
        self.speed = speed

    def attack(self):
        print("Ax attacks!")



class Eldredth(Alien):
    def __init__(self, x_max, y_max, size=(60, 60), speed=3):
        file_path = f"..\Graphics\Eldredth.png"
        self.image = pygame.image.load(file_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        super().__init__(x_max, y_max, size)
        self.move_time = 0
        self.move_cooldown = random.randint(0, 4000)
        self.speed = speed

    def attack(self):
        print("Edredth attacks!")


