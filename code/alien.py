import pygame
import random

class Alien(pygame.sprite.Sprite):
    def __init__(self, type, x_max, y_max):
        super().__init__()
        file_path = f"Graphics\{type}.png"
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(midtop=(0, random.randint(0, x_max)))
        self.x_max = x_max
        self.y_max = y_max
    
    
    def move(self):
        pass
    
    def attack(self):
        pass
    
    def recharge(self):
        pass
    
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
        self.constraint


    