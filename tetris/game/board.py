import random
from itertools import permutations

import config as cfg
import numpy as np


class Board:
    def __init__(
        self,
        tetrominos: dict = cfg.TETROMINOS,
        board_height: int = cfg.BOARD_HEIGHT,
        board_width: int = cfg.BOARD_WIDTH,
    ) -> None:
        self.board = np.zeros((board_height, board_width), dtype=int)
        self.bag = generate_next_tile(tetrominos)
        self.tile = next(self.bag)

        self.shape = np.array(tetrominos[self.tile]["shape"])
        self.color = tetrominos[self.tile]["color"]
        self.height, self.width = self.shape.shape

        self.tile_position = np.array((0, 4))

    def tile_fall(self):
        self.tile_position[0] += 1
        if self.collides():
            self.tile_position[0] -= 1
            self.lock_tile()

    def move_tile_left(self):
        self.tile_position[1] -= 1
        if self.collides():
            self.tile_position[1] += 1

    def move_tile_right(self):
        self.tile_position[1] += 1
        if self.collides():
            self.tile_position[1] -= 1

    def rotate_tile_positive(self):
        self.shape = np.rot90(self.shape, k=1)
        self.height, self.width = self.shape.shape
        if self.collides():
            self.shape = np.rot90(self.shape, k=(-1) * 1)
            self.height, self.width = self.shape.shape

    def rotate_tile_negative(self):
        self.shape = np.rot90(self.shape, k=3)
        self.height, self.width = self.shape.shape
        if self.collides():
            self.shape = np.rot90(self.shape, k=(-1) * 3)
            self.height, self.width = self.shape.shape

    def collides(self) -> bool:
        x0 = self.tile_position[1]
        x1 = x0 + self.width
        y0 = self.tile_position[0]
        y1 = y0 + self.height

        under = self.board[y0:y1, x0:x1]
        if under.shape != self.shape.shape or np.logical_and(under, self.shape).any():
            return True
        return False

    def lock_tile(self):
        for x in range(self.width):
            for y in range(self.height):
                self.board[self.tile_position[0] + y, self.tile_position[1] + x] += self.shape[y, x]
        self.clear_line()
        self.reset()

    def clear_line(self):
        for num, line in enumerate(self.board):
            if line.all():
                self.board[1 : num + 1, :] = self.board[0:num, :]
                self.board[0, :] = np.zeros((1, self.board.shape[1]))

    def reset(self, n=None):
        if n is None:
            n = next(self.bag)
        if self.collides():
            print("GAME OVER")

    def tile_drop(self):
        while True:
            self.tile_position[0] += 1
            if self.collides():
                self.tile_position[0] -= 1
                self.lock_tile()
                break


def generate_next_tile(tetrominos):
    while True:
        yield from random.choice(list(permutations(tetrominos)))
