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
        # Camera setup
        self.capture = cv2.VideoCapture(0)
        self.has_capture = True
        if self.capture == None or not self.capture.isOpened():
            self.has_capture = False

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
        if self.has_capture != False:
            success, original_img = self.capture.read()
            img = cv2.flip(original_img, 1)
            return img
        else:
            return None

    def calculate_fps(self, img):
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

    def alien_spawn(self, type):
        if type == "Ax":
            alien_sprite = Ax(SCREEN_WIDTH, SCREEN_HEIGHT, self.player_sprite)
        elif type == "Eldredth":
            alien_sprite = Eldredth(SCREEN_WIDTH, SCREEN_HEIGHT, self.player_sprite)
        elif type == "Dash":
            alien_sprite = Dash(SCREEN_WIDTH, SCREEN_HEIGHT, self.player_sprite)
        self.aliens.add(alien_sprite)

    def game_over(self):
        print("Game over!")
        pygame.quit()
        sys.exit()

    def collision_check(self):
        # Player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser, self.aliens, True):
                    laser.kill()

        # Alien lasers
        if self.aliens:
            for alien in self.aliens:
                for laser in alien.lasers:
                    if pygame.sprite.spritecollide(laser, self.player, True):
                        laser.kill()
                        self.game_over()
                if pygame.sprite.spritecollide(alien, self.player, True):
                    self.game_over()

    def run(self):
        # Update all sprite groups
        # Draw all sprite groups

        img = self.cam_capture()

        self.player.update(img, self.has_capture)
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)

        self.aliens.update()
        self.aliens.draw(screen)
        for alien in self.aliens.sprites():
            alien.lasers.draw(screen)

        self.collision_check()

        # Calculate FPS

        if self.has_capture:
            self.calculate_fps(img)


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
