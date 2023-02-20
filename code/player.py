import pygame
import math
import cv2
from hand import HandDetector
from laser import Laser


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, x_max, y_max, speed, size):
        super().__init__()
        self.image = pygame.image.load(
            "..\Graphics\Player.png"
        ).convert_alpha()  # Spacecraft Icon
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.x_max = x_max
        self.y_max = y_max
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 300  # ms
        self.lasers = pygame.sprite.Group()

        # Hand detector
        self.detector = HandDetector()
        self.current_hand = (0, 0)
        self.previous_hand = (0, 0)

    def get_input(self):
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        elif keys[pygame.K_d]:
            self.rect.x += self.speed
        elif keys[pygame.K_w]:
            self.rect.y -= self.speed
        elif keys[pygame.K_s]:
            self.rect.y += self.speed

        # Laser
        if keys[pygame.K_SPACE]:
            self.shoot_laser()

    def get_hand(self, img, has_capture):
        if has_capture:
            img = self.detector.FindHands(img)

            # List of all hand landmarks in a 2d array
            # Reference https://google.github.io/mediapipe/solutions/hands.html
            lmList = self.detector.FindPosition(img)

            if len(lmList) != 0:
                # print(lmList)
                self.current_hand = lmList[9][1:]
                # Gun gesture (shoot laser)
                if lmList[16][2] > lmList[9][2] and lmList[20][2] > lmList[9][2]:
                    self.shoot_laser()
                # Fist gesture (no movment)
                if (
                    lmList[8][2] > lmList[5][2]
                    and lmList[12][2] > lmList[9][2]
                    and lmList[16][2] > lmList[13][2]
                    and lmList[20][2] > lmList[9][2]
                ):
                    self.previous_hand = self.current_hand

            # Movement
            dx = self.current_hand[0] - self.previous_hand[0]
            dy = self.current_hand[1] - self.previous_hand[1]
            self.previous_hand = self.current_hand
            hand_speed = math.sqrt(dx**2 * dy**2)

            if hand_speed != 0:
                # Speed limit
                if hand_speed > self.speed * 20:
                    self.rect.x += dx / hand_speed * self.speed * 20
                    self.rect.y += dy / hand_speed * self.speed * 20
                else:
                    self.previous_hand = self.current_hand
                    self.rect.x += dx * self.speed / 4
                    self.rect.y += dy * self.speed / 4

        else:
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

    def shoot_laser(self):
        if self.ready:
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            self.lasers.add(Laser(self.rect.center, self.y_max, "blue"))

    def update(self, original_img, has_capture):
        self.get_input()
        self.get_hand(original_img, has_capture)
        self.constraint()
        self.recharge()
        self.lasers.update()
