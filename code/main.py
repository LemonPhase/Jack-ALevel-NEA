import pygame, sys
from player import Player
from alien import Alien

# https://www.youtube.com/watch?v=o-6pADy5Mdg&t=108s (Thank you for saving my life, ily)


class Game:
    def __init__(self) -> None:
        # Player setup
        player_sprite = Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT), SCREEN_WIDTH, SCREEN_HEIGHT, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_setup()
        
    
    def alien_setup(self):
        alien_sprite = Alien("Ax", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.aliens.add(alien_sprite)

    def run(self):
        self.player.update()
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        # Update all sprite groups
        # Draw all sprite groups
        pass


if __name__ == "__main__":
    pygame.init()
    SCREEN_HEIGHT = 480
    SCREEN_WIDTH = 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((30, 30, 30))

        game.run()
        pygame.display.flip()
        clock.tick(60)
