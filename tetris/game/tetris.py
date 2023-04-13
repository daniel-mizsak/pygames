import os

import config as cfg
import draw
import pygame
from board import Board


class Tetris:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(cfg.GAME_TITLE)

        self.screen = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.score = 0
        self.board = Board()

        self.game_over = False
        self.running = True

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.screen.fill(cfg.GAME_COLORS["BACKGROUND"])

            self.events = pygame.event.get()
            self.event_phase()

            pygame.display.update()

        pygame.quit()

    def setup_phase(self):
        self.score = 0

    def event_phase(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.board.move_tile_left()
                if event.key == pygame.K_d:
                    self.board.move_tile_right()
                if event.key == pygame.K_q:
                    self.board.rotate_tile_positive()
                if event.key == pygame.K_e:
                    self.board.rotate_tile_negative()
                if event.key == pygame.K_s:
                    self.board.tile_fall()
                if event.key == pygame.K_SPACE:
                    self.board.tile_drop()

    def play_phase(self):
        dt = 0.001 * self.clock.tick(60)
        speed = self.score // 10 + 1

        # if t // (1 / speed) != (t + dt) // (1 / speed):
        #     self.board.tile.fall()
        # t += dt

        draw.draw_board(self)

        # board_surface = pygame.transform.scale(board_surface, (300, 600))
        # self.screen.blit(board_surface, (0, 0))
        pygame.display.update()


if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = f"{cfg.WINDOW_POS_LEFT}, {cfg.WINDOW_POS_TOP}"

    game = Tetris()
    game.run()
