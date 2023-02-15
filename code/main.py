import pygame, sys
import os
import cv2
from player import Player
from alien import Ax, Eldredth
from hand import HandDetector

# https://www.youtube.com/watch?v=o-6pADy5Mdg&t=108s (Thank you for saving my life, ily)


os.chdir(os.path.dirname(__file__))


class Game:
    def __init__(self) -> None:
        # Player setup
        player_sprite = Player(
            (SCREEN_WIDTH / 2, SCREEN_HEIGHT), SCREEN_WIDTH, SCREEN_HEIGHT
        )
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_spawn("Ax")
        self.alien_spawn("Eldredth")

    def alien_spawn(self, type):
        if type == "Ax":
            alien_sprite = Ax(SCREEN_WIDTH, SCREEN_HEIGHT)
        elif type == "Eldredth":
            alien_sprite = Eldredth(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.aliens.add(alien_sprite)

    def collision_check(self):
        # Player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser, self.aliens, True):
                    laser.kill()

        # Alien lasers
        if self.aliens.sprites():
            for alien in self.aliens:
                for laser in alien.lasers:
                    if pygame.sprite.spritecollide(laser, self.player, True):
                        laser.kill()
                        print("Game over!")
                        pygame.quit()
                        sys.exit()

    def run(self):
        # Update all sprite groups
        # Draw all sprite groups
        self.player.update()
        self.player.sprite.lasers.draw(screen)
        self.aliens.update()
        for alien in self.aliens.sprites():
            alien.lasers.draw(screen)

        self.collision_check()

        self.player.draw(screen)
        self.aliens.draw(screen)
        pass


if __name__ == "__main__":
    pygame.init()
    SCREEN_HEIGHT = 480
    SCREEN_WIDTH = 720

    capture = cv2.VideoCapture(0)
    previous_time = 0
    current_time = 0

    current_hand = (0, 0)
    previous_hand = (0, 0)

    Detector = HandDetector()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((20, 20, 30))
        success, orignal_img = capture.read()
        # Flip image
        img = cv2.flip(orignal_img, 1)
        img = Detector.FindHands(img)

        lmlist, x_mean, y_mean = Detector.FindMeanPosition(img)
        current_hand = (x_mean,y_mean)
        dx = current_hand[0]-previous_hand[0]
        dy = current_hand[1]-previous_hand[1]


        current_time = pygame.time.get_ticks()/1000
        fps = 1 / (current_time - previous_time) 
        previous_time = current_time

        cv2.putText(
            img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3
        )
        game.run()
        pygame.display.flip()
        clock.tick(60)

        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
