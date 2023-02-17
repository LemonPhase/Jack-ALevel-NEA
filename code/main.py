import pygame
import sys
import os
import cv2
from player import Player
from alien import Ax, Eldredth, Dash

# https://www.youtube.com/watch?v=o-6pADy5Mdg&t=108s (Thank you for saving my life, ily)


os.chdir(os.path.dirname(__file__))


class Game:
    def __init__(self) -> None:
        # Hand detector setup

        self.capture = cv2.VideoCapture(0)
        if self.capture == None or not self.capture.isOpened():
            self.capture = False

        # FPS
        self.previous_time = 0
        self.current_time = 0

        # Player setup
        self.player_sprite = Player(
            (SCREEN_WIDTH / 2, SCREEN_HEIGHT), SCREEN_WIDTH, SCREEN_HEIGHT
        )
        self.player = pygame.sprite.GroupSingle(self.player_sprite)

        # Alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_spawn("Ax")
        self.alien_spawn("Eldredth")
        self.alien_spawn("Dash")

    def cam_capture(self):
        if self.capture != False:
            success, original_img = self.capture.read()
            # Flip image horizontally
            img = cv2.flip(original_img, 1)
        else:
            # No camera detected
            img = False

        return img

    def alien_spawn(self, type):
        if type == "Ax":
            alien_sprite = Ax(SCREEN_WIDTH, SCREEN_HEIGHT)
        elif type == "Eldredth":
            alien_sprite = Eldredth(SCREEN_WIDTH, SCREEN_HEIGHT)
        elif type == "Dash":
            alien_sprite = Dash(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.aliens.add(alien_sprite)

    def collision_check(self):
        # Player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser, self.aliens, True):
                    laser.kill()

        # Alien lasers
        if self.aliens:
            for alien in self.aliens:
                if pygame.sprite.spritecollide(alien, self.player, True):
                    print("Game over!")
                    pygame.quit()
                    sys.exit()

                for laser in alien.lasers:
                    if pygame.sprite.spritecollide(laser, self.player, True):
                        laser.kill()
                        print("Game over!")
                        pygame.quit()
                        sys.exit()

    def fps(self, img):
        self.current_time = pygame.time.get_ticks() / 1000
        fps = 1 / (self.current_time - self.previous_time)
        self.previous_time = self.current_time
        cv2.putText(
            img,
            str(int(fps)),
            (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            3,
            (255, 0, 255),
            3,
        )
        cv2.imshow("Image", img)

    def run(self):
        # Update all sprite groups
        # Draw all sprite groups

        img = self.cam_capture()

        # Player update
        self.player.update(img)
        self.player.sprite.lasers.draw(screen)
        self.player_pos = self.player.sprite.rect.center
        print(self.player_pos)

        self.player.draw(screen)

        # Alien update
        self.aliens.update(self.player_pos)
        for alien in self.aliens.sprites():
            alien.lasers.draw(screen)

        self.aliens.draw(screen)

        self.collision_check()

        # Calculate FPS
        if img != False:
            self.fps(img)


if __name__ == "__main__":
    pygame.init()
    SCREEN_HEIGHT = 720
    SCREEN_WIDTH = 1080

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((20, 20, 30))

        game.run()
        pygame.display.flip()
        clock.tick(60)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
