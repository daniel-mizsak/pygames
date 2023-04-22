"""
The game itself.

@author "Dániel Lajos Mizsák" <info@pythonvilag.hu>
"""

import os
import random

import config as cfg
import draw
import pygame


class WaveLength:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(cfg.GAME_TITLE)

        self.screen = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.guessing = False
        self.guess_value = 90
        self.value_to_guess = random.randint(12, 180 - 12)

        self.running = True

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.screen.fill(cfg.GAME_COLORS["BACKGROUND"])

            self.events = pygame.event.get()
            self.event_phase()

            draw.draw_board(self)
            if not self.guessing:
                draw.draw_reward_sectors(self)
            else:
                draw.draw_guess_line(self)

            pygame.display.update()

        pygame.quit()

    def setup_phase(self):
        self.guessing = False
        self.guess_value = 90
        self.value_to_guess = random.randint(12, 180 - 12)

    def event_phase(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and self.guessing:
                if event.key == pygame.K_a:
                    self.guess_value += 1
                if event.key == pygame.K_d:
                    self.guess_value -= 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.guessing = not self.guessing


if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = f"{cfg.WINDOW_POS_LEFT}, {cfg.WINDOW_POS_TOP}"

    game = WaveLength()
    game.run()
