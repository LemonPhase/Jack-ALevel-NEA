import pygame

from player import Player
import os

print(os.getcwd())


class Game:
    def __init__(self):
        # Player setup
        player_sprite = Player(
            ((screen_width / 2), screen_height), screen_width, screen_height, max_speed
        )


if __name__ == "__main__":
    pygame.init()
    screen_width = 600
    screen_height = 600
    max_speed = 10
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    game = Game()
