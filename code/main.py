import pygame, sys

# https://www.youtube.com/watch?v=o-6pADy5Mdg&t=108s


class Game:
    def __init__(self) -> None:
        player_sprite = Player((screen_width / 2, screen_height))
        self.player = pygame.sprite.GroupSingle(player_sprite)
        pass

    def run(self):
        # Update all sprite groups
        # Draw all sprite groups
        pass


if __name__ == "__main__":
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((30, 30, 30))

        pygame.display.flip()
        clock.tick(60)
