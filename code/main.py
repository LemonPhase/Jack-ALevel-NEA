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


# Game class that contains all the elements in the gameplay
class Game:
    def __init__(self) -> None:
        # Leader board
        try:
            self.file = open("LeaderBoard.txt", "r+")
        except:
            # Create a leaderboard file
            self.file = open("LeaderBoard.txt", "w")
            self.file.close()

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
        self.play_time = 0

        # FPS
        self.clock = pygame.time.Clock()
        self.previous_time = pygame.time.get_ticks() / 1000
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

        # Parsing the txt file
        for leader in self.lb_list:
            lst = leader.split(", ")
            # 2d array
            self.leader_board.append([int(lst[i]) for i in range(2)])

        if len(self.leader_board) < 5:
            for i in range(5 - len(self.leader_board)):
                self.leader_board.append([0, 0])

    def update_leader_board(self):
        self.leader_board.append([self.score, int(round(self.play_time, 0))])
        # Sort by the first index, reverse order
        self.leader_board.sort(key=lambda x: x[0], reverse=True)
        # List comprehension
        new_leader_board = [[str(i) for i in lst] for lst in self.leader_board]
        for line in new_leader_board[:5]:
            self.file.write(", ".join(line) + "\n")
        self.file.close()

    def display_leader_board(self):
        self.get_leader_board()
        running = True
        display_lb = self.leader_board

        while running:
            screen.fill(BG_COLOR)

            title_text = self.get_font(150).render("LEADERBOARD", False, TITLE_COLOR)
            sub_title_text = self.get_font(75).render("SCORE        TIME", False, SUB_COLOR)

            title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, 150))
            sub_title_rect = sub_title_text.get_rect(center=(SCREEN_WIDTH / 2, 275))

            font_size = 50
            first_text = self.get_font(font_size).render(
                f"1st: {display_lb[0][0]}              {display_lb[0][1]}",
                False,
                TEXT_COLOR,
            )
            second_text = self.get_font(font_size).render(
                f"2nd: {display_lb[1][0]}             {display_lb[1][1]}",
                False,
                TEXT_COLOR,
            )
            third_text = self.get_font(font_size).render(
                f"3rd: {display_lb[2][0]}              {display_lb[2][1]}",
                False,
                TEXT_COLOR,
            )
            forth_text = self.get_font(font_size).render(
                f"4th: {display_lb[3][0]}              {display_lb[3][1]}",
                False,
                TEXT_COLOR,
            )
            fifth_text = self.get_font(font_size).render(
                f"5th: {display_lb[4][0]}              {display_lb[4][1]}",
                False,
                TEXT_COLOR,
            )

            xpos = SCREEN_WIDTH / 2 - 25
            start_ypos = 350
            gap = 75
            first_rect = first_text.get_rect(center=(xpos, start_ypos))
            second_rect = second_text.get_rect(center=(xpos, start_ypos + gap))
            third_rect = third_text.get_rect(center=(xpos, start_ypos + gap * 2))
            forth_rect = forth_text.get_rect(center=(xpos, start_ypos + gap * 3))
            fifth_rect = fifth_text.get_rect(center=(xpos, start_ypos + gap * 4))

            screen.blit(title_text, title_rect)
            screen.blit(sub_title_text, sub_title_rect)
            screen.blit(first_text, first_rect)
            screen.blit(second_text, second_rect)
            screen.blit(third_text, third_rect)
            screen.blit(forth_text, forth_rect)
            screen.blit(fifth_text, fifth_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.quit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            pygame.display.update()

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
            screen.blit(self.live_surf, (x, SCREEN_HEIGHT - self.live_surf.get_size()[1] - 5))

    def display_score(self):
        score_surf = self.get_font(50).render(f"Score: {self.score}", False, "white")
        score_rect = score_surf.get_rect(topleft=(15, 10))
        screen.blit(score_surf, score_rect)

    def display_time(self):
        self.play_time += self.current_time - self.previous_time
        time_surf = self.get_font(50).render(str(round(self.play_time, 1)), False, "white")
        time_rect = time_surf.get_rect(topright=(SCREEN_WIDTH - 15, 10))
        screen.blit(time_surf, time_rect)

    def quit_game(self):
        # Save the leader board
        save_leader_board = [[str(i) for i in lst] for lst in self.leader_board]
        if len(save_leader_board) < 5:
            for line in save_leader_board:
                self.file.write(", ".join(line) + "\n")
        else:
            for line in save_leader_board[:5]:
                self.file.write(", ".join(line) + "\n")
        self.file.close()

        print("Game quit")
        pygame.quit()
        sys.exit()

    def instructions(self):
        pygame.display.set_caption("Instructions")
        running = True

        while running:
            screen.fill((10, 10, 10))
            title_text = self.get_font(100).render("Instructions", ANTI_ALIASING, TITLE_COLOR)
            keyboard_text = self.get_font(75).render("Keyboard", ANTI_ALIASING, SUB_COLOR)
            camera_text = self.get_font(75).render("Camera", ANTI_ALIASING, SUB_COLOR)
            ecp_text = self.get_font(30).render("Escape to exit", ANTI_ALIASING, TEXT_COLOR)

            kb_line1 = self.get_font(50).render("WASD to move", ANTI_ALIASING, TEXT_COLOR)
            kb_line2 = self.get_font(50).render("SPACE to shoot", ANTI_ALIASING, TEXT_COLOR)

            cam_line1 = self.get_font(50).render("Make sure camera is on", ANTI_ALIASING, TEXT_COLOR)
            cam_line2 = self.get_font(50).render("and your hand is in the capture", ANTI_ALIASING, TEXT_COLOR)
            cam_line3 = self.get_font(50).render("Gun gesture to shoot", ANTI_ALIASING, TEXT_COLOR)
            cam_line4 = self.get_font(50).render("Fist to enter turrent mode", ANTI_ALIASING, TEXT_COLOR)

            gun_image = pygame.image.load("..\Graphics\GunGesture.png")
            gun_image = pygame.transform.scale(gun_image, (60, 60))
            fist_image = pygame.image.load("..\Graphics\FistGesture.png")
            fist_image = pygame.transform.scale(fist_image, (60, 60))

            kb_x_center = SCREEN_WIDTH / 2 - 250
            cam_x_center = SCREEN_WIDTH / 2 + 225

            title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, 100))
            keyboard_rect = keyboard_text.get_rect(center=(kb_x_center, 225))
            camera_rect = camera_text.get_rect(center=(cam_x_center, 225))
            ecp_rect = ecp_text.get_rect(center=(SCREEN_WIDTH / 2, 670))

            kb_y_start = 350
            kb_y_gap = 100
            kb_line1_rect = kb_line1.get_rect(center=(kb_x_center, kb_y_start))
            kb_line2_rect = kb_line2.get_rect(center=(kb_x_center, kb_y_start + kb_y_gap))

            cam_y_start = 300
            cam_y_gap = 75
            cam_line1_rect = cam_line1.get_rect(center=(cam_x_center, cam_y_start))
            cam_line2_rect = cam_line2.get_rect(center=(cam_x_center, cam_y_start + cam_y_gap))
            cam_line3_rect = cam_line3.get_rect(center=(cam_x_center, cam_y_start + 2 * cam_y_gap))
            cam_line4_rect = cam_line4.get_rect(center=(cam_x_center, cam_y_start + 3 * cam_y_gap))

            gun_rect = gun_image.get_rect(center=(cam_x_center - 200, cam_y_start + 2 * cam_y_gap))
            fist_rect = fist_image.get_rect(center=(cam_x_center - 250, cam_y_start + 3 * cam_y_gap))

            screen.blit(title_text, title_rect)
            screen.blit(keyboard_text, keyboard_rect)
            screen.blit(camera_text, camera_rect)
            screen.blit(ecp_text, ecp_rect)

            screen.blit(kb_line1, kb_line1_rect)
            screen.blit(kb_line2, kb_line2_rect)
            screen.blit(cam_line1, cam_line1_rect)
            screen.blit(cam_line2, cam_line2_rect)
            screen.blit(cam_line3, cam_line3_rect)
            screen.blit(cam_line4, cam_line4_rect)
            screen.blit(gun_image, gun_rect)
            screen.blit(fist_image, fist_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.quit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            pygame.display.update()

    def pause_menu(self):
        pygame.display.set_caption("Game paused")
        running = True

        # Pause menu loop
        while running:
            self.current_time = pygame.time.get_ticks() / 1000
            self.previous_time = self.current_time

            screen.fill((10, 10, 10))

            # Mouse position
            menu_mouse_pos = pygame.mouse.get_pos()

            # Menu title
            menu_text = self.get_font(100).render("Pause Menu", True, TITLE_COLOR)
            menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH / 2, 150))
            screen.blit(menu_text, menu_rect)

            # Button setup
            continue_button = Button(
                pos=(SCREEN_WIDTH / 2, 300),
                text_input="CONTINUE",
                font=self.get_font(75),
                base_color=SUB_COLOR,
                hovering_color=TEXT_COLOR,
            )
            main_menu_button = Button(
                pos=(SCREEN_WIDTH / 2, 400),
                text_input="MAIN MENU",
                font=self.get_font(75),
                base_color=SUB_COLOR,
                hovering_color=TEXT_COLOR,
            )
            instruction_button = Button(
                pos=(SCREEN_WIDTH / 2, 500),
                text_input="INSTRUCTIONS",
                font=self.get_font(75),
                base_color=SUB_COLOR,
                hovering_color=TEXT_COLOR,
            )
            quit_button = Button(
                pos=(SCREEN_WIDTH / 2, 600),
                text_input="QUIT",
                font=self.get_font(75),
                base_color=SUB_COLOR,
                hovering_color=TEXT_COLOR,
            )

            # Display button
            for button in [
                continue_button,
                main_menu_button,
                instruction_button,
                quit_button,
            ]:
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
                    if instruction_button.check_input(menu_mouse_pos):
                        self.instructions()
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
        self.current_time = pygame.time.get_ticks() / 1000
        fps = 1 / (self.current_time - self.previous_time)
        self.display_time()
        self.previous_time = self.current_time

        # Show FPS
        if self.has_capture:
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

        self.update_leader_board()
        # Display game over
        game_over = True
        start_time = pygame.time.get_ticks() / 1000
        while game_over:
            screen.fill((0, 0, 0))
            if pygame.time.get_ticks() / 1000 - start_time >= 5:
                game_over = False
            game_over_text = self.get_font(200).render("GAME OVER!", False, (192, 64, 64))
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            lb_update_text = self.get_font(35).render(
                f"Your score has been updated, check the leader board and see if you're on it!",
                False,
                (196, 252, 192),
            )
            lb_update_rect = lb_update_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        game_over = False

            screen.blit(game_over_text, game_over_rect)
            screen.blit(lb_update_text, lb_update_rect)
            pygame.display.set_caption("Game over")
            pygame.display.update()


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
        screen.fill(BG_COLOR)

        # Mouse position
        menu_mouse_pos = pygame.mouse.get_pos()

        # Title
        title_text = game.get_font(150).render("GALAXY KNIGHT", False, TITLE_COLOR)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, 150))
        screen.blit(title_text, title_rect)

        # Button setup
        play_button = Button(
            pos=(SCREEN_WIDTH / 2, 300),
            text_input="NEW GAME",
            font=game.get_font(100),
            base_color=SUB_COLOR,
            hovering_color=TEXT_COLOR,
        )
        leader_board_button = Button(
            pos=(SCREEN_WIDTH / 2, 400),
            text_input="LEADER BOARD",
            font=game.get_font(100),
            base_color=SUB_COLOR,
            hovering_color=TEXT_COLOR,
        )
        instruction_button = Button(
            pos=(SCREEN_WIDTH / 2, 500),
            text_input="INSTRUCTIONS",
            font=game.get_font(100),
            base_color=SUB_COLOR,
            hovering_color=TEXT_COLOR,
        )
        quit_button = Button(
            pos=(SCREEN_WIDTH / 2, 600),
            text_input="QUIT",
            font=game.get_font(100),
            base_color=SUB_COLOR,
            hovering_color=TEXT_COLOR,
        )

        # Display button
        for button in [play_button, leader_board_button, instruction_button, quit_button]:
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
                if leader_board_button.check_input(menu_mouse_pos):
                    game.display_leader_board()
                if instruction_button.check_input(menu_mouse_pos):
                    game.instructions()
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
    # Window setup
    SCREEN_HEIGHT = 720
    SCREEN_WIDTH = 1080

    # Game setup
    PLAYER_SPEED = 10
    PLAYER_SIZE = (60, 60)
    TARGET_FPS = 45

    ANTI_ALIASING = False

    # Colors
    TITLE_COLOR = (64, 192, 225)
    SUB_COLOR = (196, 252, 192)
    TEXT_COLOR = (255, 255, 255)
    BG_COLOR = (10, 10, 10)
    # Read leaderboard

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    main_menu()
