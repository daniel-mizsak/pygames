import math
from typing import Type

import config as cfg
import pygame

from wavelength import WaveLength


def circle_sector_vertices(
    center: tuple[int, int], radius: int, start_angle: int, end_angle: int
) -> list[tuple[int, int]]:
    vertices = [center]
    for angle in range(start_angle, end_angle + 1):
        x = center[0] - int(radius * math.cos(math.radians(angle)))
        y = center[1] - int(radius * math.sin(math.radians(angle)))
        vertices.append((x, y))
    return vertices


def guess_line_end(angle: int, line_length: int, start_x: int, start_y: int) -> tuple[int, int]:
    angle_radians = math.radians(angle)
    end_x = start_x + int(math.cos(angle_radians) * line_length)
    end_y = start_y - int(math.sin(angle_radians) * line_length)
    return end_x, end_y


def draw_board(self: WaveLength) -> None:
    pygame.draw.polygon(
        self.screen,
        cfg.GAME_COLORS["WHITE"],
        circle_sector_vertices(cfg.CIRCLE_CENTER, cfg.CIRCLE_RADIUS, 0, 180),
    )


def draw_reward_sectors(self: WaveLength) -> None:
    pygame.draw.polygon(
        self.screen,
        cfg.GAME_COLORS["YELLOW"],
        circle_sector_vertices(
            cfg.CIRCLE_CENTER, cfg.CIRCLE_RADIUS, self.value_to_guess - 12, self.value_to_guess + 12
        ),
    )
    pygame.draw.polygon(
        self.screen,
        cfg.GAME_COLORS["ORANGE"],
        circle_sector_vertices(
            cfg.CIRCLE_CENTER, cfg.CIRCLE_RADIUS, self.value_to_guess - 7, self.value_to_guess + 7
        ),
    )
    pygame.draw.polygon(
        self.screen,
        cfg.GAME_COLORS["BLUE"],
        circle_sector_vertices(
            cfg.CIRCLE_CENTER, cfg.CIRCLE_RADIUS, self.value_to_guess - 2, self.value_to_guess + 2
        ),
    )


def draw_guess_line(self: WaveLength) -> None:
    pygame.draw.line(
        self.screen,
        cfg.GAME_COLORS["RED"],
        cfg.CIRCLE_CENTER,
        guess_line_end(self.guess_value, cfg.CIRCLE_RADIUS, *cfg.CIRCLE_CENTER),
        5,
    )
