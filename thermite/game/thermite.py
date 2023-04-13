"""
The game itself.

@author "Dániel Lajos Mizsák" <info@pythonvilag.hu>
"""

import os

import config as cfg
import draw
import pygame
from board import create_board


class Thermite:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(cfg.GAME_TITLE)

        self.screen = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.start_time = pygame.time.get_ticks()
        self.current_time = 0
        self.mouse_position = pygame.mouse.get_pos()
        self.mouse_active = "disabled"
        self.score = 0

        self.board = create_board()

        self.game_over = False
        self.running = True

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.screen.fill(cfg.GAME_COLORS["BACKGROUND"])

            self.events = pygame.event.get()
            self.event_phase()

            self.current_time = pygame.time.get_ticks() - self.start_time
            if self.current_time < cfg.START_TIME:
                draw.draw_order_phase(self)
            elif (self.current_time > cfg.START_TIME) and not self.game_over:
                draw.draw_solve_phase(self)

            if self.game_over:
                draw.draw_solution_phase(self)

            pygame.display.update()

        pygame.quit()

    def setup_phase(self):
        self.start_time = pygame.time.get_ticks()
        self.mouse_active = "disabled"

        self.board = create_board()

    def event_phase(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False

            if (
                (event.type == pygame.MOUSEBUTTONDOWN)
                and (self.mouse_active == "enabled")
                and (not self.game_over)
            ):
                self.board.guess_tile(pygame.mouse.get_pos())
                self.game_over = len(self.board.wrongly_guess_tiles) >= 3
                if len(self.board.correctly_guessed_tiles) == len(self.board.correct_tiles):
                    self.setup_phase()

            if (
                (event.type == pygame.MOUSEBUTTONDOWN)
                and (self.mouse_active == "play_again")
                and (self.game_over)
            ):
                self.game_over = False
                self.setup_phase()


if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = f"{cfg.WINDOW_POS_LEFT}, {cfg.WINDOW_POS_TOP}"

    game = Thermite()
    game.run()
