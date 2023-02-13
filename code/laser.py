import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, y_max, laser_speed=15):
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.image.fill("white")
        self.rect = self.image.get_rect(center=pos)
        self.laser_speed = laser_speed
        self.y_max = y_max

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.y_max + 50:
            self.kill()

    def update(self):
        self.rect.y -= self.laser_speed
        self.destroy()
