"""
The game itself.

@author "Dániel Lajos Mizsák" <info@pythonvilag.hu>
"""

import csv
import os
import random

import config as cfg
import draw
import pygame


class WaveLength:
    game_states = ["SETUP", "GUESSING", "LOWER_HIGHER", "NEXT_ROUND"]
    sector_lengths = [12, 7, 2]
    sector_rewards = [2, 3, 4]

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(cfg.GAME_TITLE)

        self.screen = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.score = [0, 1]
        self.current_team = 1
        with open(file="wavelength/docs/opposites.csv", mode="r") as f:
            self.opposite_pairs = list(csv.reader(f, delimiter=","))

        self.setup_phase()
        self.running = True

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.screen.fill(cfg.GAME_COLORS["BACKGROUND"])

            self.events = pygame.event.get()
            self.event_phase()

            draw.draw_board(self)
            draw.draw_opposite_values(self)
            draw.draw_score(self)

            self.next_rectangle = draw.draw_next_button_rectangle(self)
            self.back_rectangle = draw.draw_back_button_rectangle(self)

            if self.game_state == "SETUP":
                draw.draw_setup(self)
            elif self.game_state == "GUESSING":
                draw.draw_guessing(self)
            elif self.game_state == "LOWER_HIGHER":
                draw.draw_guessing(self)
                draw.draw_lower_higher(self)
            elif self.game_state == "NEXT_ROUND":
                draw.draw_setup(self)
                draw.draw_guessing(self)

            pygame.display.update()

        pygame.quit()

    def setup_phase(self):
        self.game_state = "SETUP"
        self.current_team = (self.current_team + 1) % 2
        self.guess_value = 90
        self.value_to_guess = random.randint(12, 180 - 12)
        self.opposite_pair = random.choice(self.opposite_pairs)

    def event_phase(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and self.game_state == "GUESSING":
                if event.key == pygame.K_a:
                    self.guess_value -= 1
                if event.key == pygame.K_d:
                    self.guess_value += 1

            # Only register mouse clicks if it is pressed for more than 500ms
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.button_timer = pygame.time.get_ticks()

            if (
                event.type == pygame.MOUSEBUTTONUP
                and pygame.time.get_ticks() - self.button_timer > 500
            ):
                mouse_position = pygame.mouse.get_pos()

                if self.next_rectangle.collidepoint(mouse_position):
                    if self.game_state == "LOWER_HIGHER":
                        # Points
                        self.score[self.current_team] += self.calculate_points()

                        # Lower
                        if mouse_position[0] < self.next_rectangle.centerx:
                            if (self.calculate_points() != max(self.sector_rewards)) and (
                                self.value_to_guess < self.guess_value
                            ):
                                self.score[(self.current_team + 1) % 2] += 1

                        # Higher
                        if mouse_position[0] > self.next_rectangle.centerx:
                            if (self.calculate_points() != max(self.sector_rewards)) and (
                                self.value_to_guess > self.guess_value
                            ):
                                self.score[(self.current_team + 1) % 2] += 1
                    if self.game_state == "NEXT_ROUND":
                        pass
                    self.game_state = self.game_states[
                        (self.game_states.index(self.game_state) + 1) % len(self.game_states)
                    ]

                if self.back_rectangle.collidepoint(mouse_position) and self.game_state != "SETUP":
                    self.game_state = self.game_states[
                        (self.game_states.index(self.game_state) - 1) % len(self.game_states)
                    ]

                self.button_timer = 0

    def calculate_points(self):
        difference = abs(self.value_to_guess - self.guess_value)
        for sector_length, sector_reward in zip(
            reversed(self.sector_lengths), reversed(self.sector_rewards)
        ):
            if difference <= sector_length:
                return sector_reward
        return 0


if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = f"{cfg.WINDOW_POS_LEFT}, {cfg.WINDOW_POS_TOP}"

    game = WaveLength()
    game.run()
