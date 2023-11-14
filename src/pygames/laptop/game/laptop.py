"""
The game itself.

@author "Dániel Lajos Mizsák" <info@pythonvilag.hu>
"""

import os

import config as cfg
import draw
import pygame
from unit import create_task, create_units


class Laptop:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(cfg.GAME_TITLE)

        self.screen = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.start_time = pygame.time.get_ticks()
        self.current_time = 0
        self.mouse_position = pygame.mouse.get_pos()
        self.mouse_active = False
        self.score = 0

        self.units = create_units()
        self.task_text, self.solution_text = create_task(self.units)
        self.input_text = ""

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
            elif cfg.START_TIME < self.current_time < (cfg.START_TIME + cfg.SOLVE_TIME):
                draw.draw_solve_phase(self)
            elif self.current_time > (cfg.START_TIME + cfg.SOLVE_TIME):
                self.game_over = True

            if self.game_over:
                draw.draw_solve_phase(self)
                draw.draw_solution_phase(self)

            pygame.display.update()

        pygame.quit()

    def setup_phase(self):
        self.start_time = pygame.time.get_ticks()
        self.mouse_active = False

        self.units = create_units()
        self.task_text, self.solution_text = create_task(self.units)
        self.input_text = ""

        if self.game_over:
            self.score = 0
            self.game_over = False
        else:
            self.score += 1

    def event_phase(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False

            if (
                event.type == pygame.KEYDOWN
                and self.current_time > cfg.START_TIME
                and not self.game_over
            ):
                if event.key == pygame.K_RETURN:
                    if self.input_text == self.solution_text:
                        self.setup_phase()
                    else:
                        self.game_over = True
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                elif event.key != pygame.K_RETURN:
                    self.input_text += str(event.unicode)

            if event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                if self.mouse_active:
                    self.setup_phase()


if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = f"{cfg.WINDOW_POS_LEFT}, {cfg.WINDOW_POS_TOP}"

    game = Laptop()
    game.run()
