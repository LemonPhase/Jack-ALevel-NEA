import pygame
import sys
import os
import cv2
import math
import random
from player import Player
from alien import Ax, Eldredth, Dash
from button import Button

# https://www.youtube.com/watch?v=o-6pADy5Mdg&t=108s (Thank you for saving my life, ily)


os.chdir(os.path.dirname(__file__))


class Game:
    def __init__(self) -> None:
        # Leader board
        self.file = open("LeaderBoard.txt", "r+")
        self.lb_list = self.file.read().splitlines()
        self.get_leader_board()
        self.file.close()

        self.file = open("LeaderBoard.txt", "w")

        # Camera setup
        try:
            self.capture = cv2.VideoCapture(0)
            self.has_capture = True
            if self.capture == None or not self.capture.isOpened():
                self.has_capture = False
        except:
            print("Error: no capture")

        # Play time record
        self.start_time = pygame.time.get_ticks() / 1000
        self.play_time = 0

        # FPS
        self.clock = pygame.time.Clock()
        self.previous_time = 0
        self.current_time = 0

        # Player setup
        self.player_sprite = Player(
            (SCREEN_WIDTH / 2, SCREEN_HEIGHT),
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            PLAYER_SPEED,
            PLAYER_SIZE,
        )
        self.player = pygame.sprite.GroupSingle(self.player_sprite)

        # Health and score
        self.lives = 3
        self.live_surf = pygame.image.load("..\graphics\health.png")
        self.live_surf = pygame.transform.scale(self.live_surf, (50, 50))
        self.live_x_start_pos = 10
        self.score = 0

        # Alien setup
        self.aliens_types = ["Ax", "Eldredth", "Dash"]
        self.aliens = pygame.sprite.Group()
        self.last_spawn = 0
        self.spawn_cooldown = 0

        # Audio setup

        self.explosion_sound = pygame.mixer.Sound("..\Audio\Explosion.wav")
        self.explosion_sound.set_volume(0.15)

    def cam_capture(self):
        if self.has_capture != False:
            success, original_img = self.capture.read()
            img = cv2.flip(original_img, 1)
            return img
        else:
            return None

    def get_font(self, size):
        # Returns font in the desired size
        return pygame.font.Font("..\Font\Brandford.otf", size)

    def get_leader_board(self):
        self.leader_board = []

        for leader in self.lb_list:
            lst = leader.split(",")
            self.leader_board.append([int(lst[i]) for i in range(2)])

    def update_leader_board(self):
        self.leader_board.append([self.score, int(round(self.play_time, 0))])
        self.leader_board.sort(key=lambda x: x[0], reverse=True)
        new_leader_board = [[str(i) for i in lst] for lst in self.leader_board]
        print(new_leader_board)
        if len(new_leader_board) < 5:
            for line in new_leader_board:
                self.file.write(",".join(line) + "\n")
        else:
            for line in new_leader_board[:4]:
                self.file.write(",".join(line) + "\n")
        self.file.close()

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

    def calculate_cd(self, time):
        # the respawn cd decreases as time passes, minimum cd 0.5s
        return math.exp(-1 * (1 / 50 * time - 1)) + 1 / 2

    def alien_spawn(self, type):
        if type == "Ax":
            alien_sprite = Ax(SCREEN_WIDTH, SCREEN_HEIGHT, self.player_sprite)
        elif type == "Eldredth":
            alien_sprite = Eldredth(SCREEN_WIDTH, SCREEN_HEIGHT, self.player_sprite)
        elif type == "Dash":
            alien_sprite = Dash(SCREEN_WIDTH, SCREEN_HEIGHT, self.player_sprite)
        self.aliens.add(alien_sprite)

    def game_progress(self):
        time = pygame.time.get_ticks() / 1000  # in seconds
        if (time - self.last_spawn) >= self.spawn_cooldown:
            self.alien_spawn(random.choice(self.aliens_types))
            self.last_spawn = time
            self.spawn_cooldown = self.calculate_cd(time)
        else:
            pass

    def collision_check(self):
        # Player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:

                alien_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if alien_hit:
                    self.explosion_sound.play()
                    for alien in alien_hit:
                        self.score += alien.score
                    laser.kill()

        # Alien lasers
        if self.aliens:
            for alien in self.aliens:
                for laser in alien.lasers:
                    if pygame.sprite.spritecollide(laser, self.player, False):
                        laser.kill()
                        self.lives -= 1
                if pygame.sprite.spritecollide(alien, self.player, False):
                    self.explosion_sound.play()
                    alien.kill()
                    self.lives -= 1

    def display_lives(self):
        for live in range(self.lives):
            x = self.live_x_start_pos + (live * self.live_surf.get_size()[0])
            screen.blit(
                self.live_surf, (x, SCREEN_HEIGHT - self.live_surf.get_size()[1] - 5)
            )

    def display_score(self):
        score_surf = self.get_font(50).render(f"Score: {self.score}", False, "white")
        score_rect = score_surf.get_rect(topleft=(15, 10))
        screen.blit(score_surf, score_rect)

    def display_time(self):
        self.play_time = (pygame.time.get_ticks() / 1000) - self.start_time
        # print(self.play_time)
        time_surf = self.get_font(50).render(
            str(
                round(
                    self.play_time,
                    1,
                )
            ),
            False,
            "white",
        )
        time_rect = time_surf.get_rect(topright=(SCREEN_WIDTH - 15, 10))
        screen.blit(time_surf, time_rect)

    def quit_game(self):
        # Save the leader board
        new_leader_board = [[str(i) for i in lst] for lst in self.leader_board]
        if len(new_leader_board) < 5:
            for line in new_leader_board:
                self.file.write(", ".join(line) + "\n")
        else:
            for line in new_leader_board[:4]:
                self.file.write(", ".join(line) + "\n")
        self.file.close()

        print("Game quit")
        pygame.quit()
        sys.exit()

    def pause_menu(self):
        # Pause play time

        self.play_time += pygame.time.get_ticks() / 1000 - self.start_time

        pygame.display.set_caption("Game paused")
        running = True

        # Pause menu loop
        while running:
            # Pause the timer
            self.start_time = pygame.time.get_ticks() / 1000
            screen.fill((10, 10, 10))

            # Mouse position
            menu_mouse_pos = pygame.mouse.get_pos()

            # Menu title
            menu_text = self.get_font(100).render("Pause Menu", True, (64, 192, 225))
            menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH / 2, 150))
            screen.blit(menu_text, menu_rect)

            # Button setup
            continue_button = Button(
                pos=(SCREEN_WIDTH / 2, 325),
                text_input="CONTINUE",
                font=self.get_font(75),
                base_color=(196, 252, 192),
                hovering_color="white",
            )
            main_menu_button = Button(
                pos=(SCREEN_WIDTH / 2, 450),
                text_input="MAIN MENU",
                font=self.get_font(75),
                base_color=(196, 252, 192),
                hovering_color="white",
            )
            quit_button = Button(
                pos=(SCREEN_WIDTH / 2, 575),
                text_input="QUIT",
                font=self.get_font(75),
                base_color=(196, 252, 192),
                hovering_color="white",
            )

            # Display button
            for button in [continue_button, main_menu_button, quit_button]:
                button.change_color(menu_mouse_pos)
                button.update(screen)

            # Button clicks
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.quit_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.check_input(menu_mouse_pos):
                        return True
                    if main_menu_button.check_input(menu_mouse_pos):
                        return False
                    if quit_button.check_input(menu_mouse_pos):
                        self.quit_game()

            pygame.display.update()

    def run(self):
        # Update all sprite groups
        # Draw all sprite groups

        img = self.cam_capture()

        self.player.update(img, self.has_capture)
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)

        self.game_progress()

        self.aliens.update()
        self.aliens.draw(screen)
        for alien in self.aliens.sprites():
            alien.lasers.draw(screen)

        self.collision_check()

        self.display_lives()
        self.display_score()
        self.display_time()

        # Calculate FPS
        if self.has_capture:
            self.calculate_fps(img)

        # Game over
        if self.lives <= 0:
            return False
        else:
            return True

    def play(self):
        bg_img = pygame.image.load("..\Graphics\Background.jpg")
        bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        i = 0
        running = True

        # Gameplay loop
        while running:
            pygame.display.set_caption("PIU PIU PIU!!!")
            self.play_time += pygame.time.get_ticks() / 1000 - self.start_time
            # Background scrolling
            screen.fill((0, 0, 0))
            screen.blit(bg_img, (0, i))
            screen.blit(bg_img, (0, -SCREEN_HEIGHT + i))
            if i == 1 * SCREEN_HEIGHT:
                screen.blit(bg_img, (0, SCREEN_HEIGHT + i))
                i = 0
            i += 3  # Pixel each scroll

            running = self.run()
            pygame.display.flip()
            self.clock.tick(TARGET_FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = self.pause_menu()

        # Display game over
        game_over = True
        start_time = pygame.time.get_ticks() / 1000
        while game_over:
            screen.fill((0, 0, 0))
            if pygame.time.get_ticks() / 1000 - start_time >= 1.5:
                game_over = False
            game_over_text = self.get_font(200).render(
                "GAME OVER!", False, (192, 64, 64)
            )
            game_over_rect = game_over_text.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            )
            screen.blit(game_over_text, game_over_rect)
            pygame.display.set_caption("Game over")
            pygame.display.update()

        self.update_leader_board()


def main_menu():
    # First game
    game = Game()
    pygame.display.set_caption("Main Menu")
    running = True

    # Music
    music = pygame.mixer.Sound("..\Audio\GalaxyNauts.wav")
    music.set_volume(0.2)
    music.play(loops=-1)

    new_game = False

    # Loop logic:
    # Main menu loop > game loop > pause menu loop

    # Main menu loop
    while running:
        # Background
        screen.fill((10, 10, 10))

        # Mouse position
        menu_mouse_pos = pygame.mouse.get_pos()

        # Title
        menu_text = game.get_font(150).render("GALAXY KNIGHT", True, (64, 192, 225))
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH / 2, 150))
        screen.blit(menu_text, menu_rect)

        # Button setup
        play_button = Button(
            pos=(SCREEN_WIDTH / 2, 325),
            text_input="NEW GAME",
            font=game.get_font(100),
            base_color=(196, 252, 192),
            hovering_color="white",
        )
        leader_board_button = Button(
            pos=(SCREEN_WIDTH / 2, 450),
            text_input="LEADER BOARD",
            font=game.get_font(100),
            base_color=(196, 252, 192),
            hovering_color="white",
        )
        quit_button = Button(
            pos=(SCREEN_WIDTH / 2, 575),
            text_input="QUIT",
            font=game.get_font(100),
            base_color=(196, 252, 192),
            hovering_color="white",
        )

        # Display button
        for button in [play_button, leader_board_button, quit_button]:
            button.change_color(menu_mouse_pos)
            button.update(screen)

        # Button clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game.quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_input(menu_mouse_pos):
                    game.play()
                    # Previous game finished
                    new_game = True
                if quit_button.check_input(menu_mouse_pos):
                    game.quit_game()

        # Create a new game
        if new_game:
            # Instantiating new game object, creating a new game
            game = Game()
            new_game = False

        pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    SCREEN_HEIGHT = 720
    SCREEN_WIDTH = 1080
    PLAYER_SPEED = 10
    PLAYER_SIZE = (60, 60)
    TARGET_FPS = 45
    # Read leaderboard

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    main_menu()
