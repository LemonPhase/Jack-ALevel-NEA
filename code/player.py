import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, max_x, max_y, max_speed):
        super().__init__()
        self.image = pygame.image.load(
            "../Graphics\player.png"
        ).convert_alpha()  # Spacecraft Icon
        self.rect = self.image.get_rect(midbotton=pos)

    def get_input(self):
        pass


player1 = Player(0, 0, 0, 0)
