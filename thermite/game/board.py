"""
Creates a board with randomized attributes.

@author Dániel Lajos Mizsák info@pythonvilag.hu
"""
import random

import config as cfg
import numpy as np


class Board:
    def __init__(self, board_dimension: int, tile_num: int):
        self.board = self.select_tiles(board_dimension, tile_num)
        self.tile_boundaries = self.create_tile_boundaries(board_dimension)

        self.correct_tiles = list(zip(np.where(self.board == 1)[0], np.where(self.board == 1)[1]))
        self.correctly_guessed_tiles = set()
        self.wrongly_guess_tiles = set()

    def __repr__(self):
        return f"Board(\n{self.board})"

    def guess_tile(self, mouse_position: tuple):
        x_mouse, y_mouse = mouse_position
        for (x, y), (x_min, x_max, y_min, y_max) in self.tile_boundaries.items():
            if x_min <= x_mouse <= x_max and y_min <= y_mouse <= y_max:
                if self.is_tile_active(x, y):
                    self.correctly_guessed_tiles.add((x, y))
                else:
                    self.wrongly_guess_tiles.add((x, y))

    def is_tile_active(self, x, y):
        if self.board[x, y] == 1:
            return True
        return False

    @staticmethod
    def select_tiles(board_dimension: int, tile_num: int) -> np.ndarray:
        active_tile_indices = random.sample(range(board_dimension**2), tile_num)
        board = np.zeros(board_dimension**2)
        board[active_tile_indices] = 1
        board = board.reshape(board_dimension, board_dimension)
        return board

    @staticmethod
    def create_tile_boundaries(board_dimension: int) -> dict:
        tile_boundaries = {}
        for y in range(board_dimension):
            for x in range(board_dimension):
                x_top_left = cfg.GAP_SIZE / 2 + x * (cfg.GAP_SIZE + cfg.TILE_SIZE)
                y_top_left = cfg.GAP_SIZE / 2 + y * (cfg.GAP_SIZE + cfg.TILE_SIZE)

                tile_boundaries[(x, y)] = (
                    x_top_left,
                    x_top_left + cfg.TILE_SIZE,
                    y_top_left,
                    y_top_left + cfg.TILE_SIZE,
                )
        return tile_boundaries


def create_board(board_dimension: int = cfg.BOARD_DIMENSION, tile_num: int = cfg.TILE_NUM) -> Board:
    board = Board(board_dimension, tile_num)
    return board


if __name__ == "__main__":
    b = create_board()
    print(b)

    print(b.tile_boundaries)

    # print(b.is_tile_active(1, 1))
    # print(b.board.shape)
    # print(b.correct_tiles)
