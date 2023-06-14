import math

import config as cfg
import pygame
from pygame import transform

from wavelength import WaveLength


# Board
def draw_board(self: WaveLength) -> None:
    pygame.draw.polygon(self.screen, cfg.GAME_COLORS["WHITE"], circle_sector_vertices(0, 180))


def circle_sector_vertices(
    start_angle: int,
    end_angle: int,
    center: tuple[int, int] = cfg.CIRCLE_CENTER,
    radius: int = cfg.CIRCLE_RADIUS,
) -> list[tuple[int, int]]:
    vertices = [center]
    for angle in range(start_angle, end_angle + 1):
        x = center[0] - int(radius * math.cos(math.radians(angle)))
        y = center[1] - int(radius * math.sin(math.radians(angle)))
        vertices.append((x, y))
    return vertices


# Opposite values
def draw_opposite_values(self: WaveLength) -> None:
    opposite_value_font = pygame.font.Font(None, 24)

    opposite_value_text = opposite_value_font.render(
        str(self.opposite_pair[0]),
        True,
        cfg.GAME_COLORS["WHITE"],
    )
    opposite_value_text_rect = opposite_value_text.get_rect()
    opposite_value_text_rect.center = (
        cfg.CIRCLE_CENTER[0] - cfg.CIRCLE_RADIUS,
        cfg.CIRCLE_CENTER[1] + 20,
    )
    self.screen.blit(opposite_value_text, opposite_value_text_rect.topleft)

    opposite_value_text = opposite_value_font.render(
        str(self.opposite_pair[1]),
        True,
        cfg.GAME_COLORS["WHITE"],
    )
    opposite_value_text_rect = opposite_value_text.get_rect()
    opposite_value_text_rect.center = (
        cfg.CIRCLE_CENTER[0] + cfg.CIRCLE_RADIUS,
        cfg.CIRCLE_CENTER[1] + 20,
    )
    self.screen.blit(opposite_value_text, opposite_value_text_rect.topleft)


# Score
def draw_score(self: WaveLength) -> None:
    for i in range(cfg.SCORE_TO_WIN):
        if i >= cfg.SCORE_TO_WIN - self.score[0]:
            rectangle_color = cfg.GAME_COLORS["BLUE"]
        else:
            rectangle_color = cfg.GAME_COLORS["WHITE"]
        pygame.draw.rect(
            self.screen,
            rectangle_color,
            (
                45,
                15 + (i * 30),
                15,
                15,
            ),
        )
        if i >= cfg.SCORE_TO_WIN - self.score[1]:
            rectangle_color = cfg.GAME_COLORS["RED"]
        else:
            rectangle_color = cfg.GAME_COLORS["WHITE"]
        pygame.draw.rect(
            self.screen,
            rectangle_color,
            (
                cfg.SCREEN_WIDTH - 45 - 15,
                15 + (i * 30),
                15,
                15,
            ),
        )


# Setup
def draw_setup(self: WaveLength) -> None:
    reward_font = pygame.font.Font(None, 18)
    sector_lengths = [12, 7, 2]
    sector_rewards = [2, 3, 4]
    sector_colors = ["YELLOW", "ORANGE", "BLUE"]
    for sector_length, sector_reward, sector_color in zip(
        sector_lengths, sector_rewards, sector_colors
    ):
        polygon_vertices = circle_sector_vertices(
            self.value_to_guess - sector_length,
            self.value_to_guess + sector_length,
        )
        pygame.draw.polygon(
            self.screen,
            cfg.GAME_COLORS[sector_color],
            polygon_vertices,
        )

        for sign in [-1, 1]:
            reward_text = transform.rotate(
                reward_font.render(str(sector_reward), True, cfg.GAME_COLORS["BLACK"]),
                90 - (self.value_to_guess + sign * sector_length),
            )
            reward_text_rect = reward_text.get_rect()
            reward_text_rect.center = polygon_vertices[3 * -1 * sign]
            self.screen.blit(reward_text, move_point_closer_to_center(reward_text_rect.topleft))


def move_point_closer_to_center(
    point: tuple[int, int],
    center: tuple[int, int] = cfg.CIRCLE_CENTER,
    ratio: float = 0.95,
) -> tuple[int, int]:
    return (
        int((point[0] - center[0]) * ratio + center[0]),
        int((point[1] - center[1]) * ratio + center[1]),
    )


# Guessing
def draw_guessing(self: WaveLength) -> None:
    pygame.draw.line(
        self.screen,
        cfg.GAME_COLORS["RED"],
        cfg.CIRCLE_CENTER,
        guess_line_end(self.guess_value, cfg.CIRCLE_RADIUS, *cfg.CIRCLE_CENTER),
        5,
    )


def guess_line_end(angle: int, line_length: int, start_x: int, start_y: int) -> tuple[int, int]:
    angle_radians = math.radians(angle)
    end_x = start_x - int(math.cos(angle_radians) * line_length)
    end_y = start_y - int(math.sin(angle_radians) * line_length)
    return end_x, end_y


# Lower higher
def draw_lower_higher(self: WaveLength) -> None:
    original_recrangle = self.next_rectangle.copy()
    lower_higher_colors = ["BLUE", "RED"]
    lower_higher_texts = ["LOWER", "HIGHER"]

    for i in range(2):
        lower_higher_rectangle = pygame.rect.Rect(
            original_recrangle.left + i * original_recrangle.width // 2,
            original_recrangle.top,
            original_recrangle.width // 2,
            original_recrangle.height,
        )
        pygame.draw.rect(
            self.screen, cfg.GAME_COLORS[lower_higher_colors[i]], lower_higher_rectangle
        )

        lower_higher_font = pygame.font.Font(None, 20)
        lower_higher_text = lower_higher_font.render(
            lower_higher_texts[i],
            True,
            cfg.GAME_COLORS["WHITE"],
        )
        lower_higher_text_rect = lower_higher_text.get_rect()
        lower_higher_text_rect.center = (
            lower_higher_rectangle.left + lower_higher_rectangle.width // 2,
            lower_higher_rectangle.top + lower_higher_rectangle.height // 2,
        )
        self.screen.blit(lower_higher_text, lower_higher_text_rect.topleft)


# Buttons
def draw_next_button_rectangle(self: WaveLength) -> pygame.rect.Rect:
    # Rectangle
    next_rectangle_left = cfg.SCREEN_WIDTH - 2 * cfg.CIRCLE_RADIUS - 100
    next_rectangle_top = cfg.SCREEN_HEIGHT - 250
    next_rectangle_width = 2 * cfg.CIRCLE_RADIUS
    next_rectangle_height = 100

    next_rectangle = pygame.rect.Rect(
        next_rectangle_left,
        next_rectangle_top,
        next_rectangle_width,
        next_rectangle_height,
    )
    pygame.draw.rect(self.screen, cfg.GAME_COLORS["WHITE"], next_rectangle)

    # Text
    hide_board_font = pygame.font.Font(None, 24)
    button_text = "HIDE BOARD"
    if self.game_state == "GUESSING":
        button_text = "MARK GUESS"
    elif self.game_state == "NEXT_ROUND":
        button_text = "NEXT ROUND"

    hide_board_text = hide_board_font.render(
        button_text,
        True,
        cfg.GAME_COLORS["BLACK"],
    )
    hide_board_text_rect = hide_board_text.get_rect()
    hide_board_text_rect.center = (
        next_rectangle_left + next_rectangle_width // 2,
        next_rectangle_top + next_rectangle_height // 2,
    )
    self.screen.blit(hide_board_text, hide_board_text_rect.topleft)

    return next_rectangle


def draw_back_button_rectangle(self: WaveLength) -> pygame.rect.Rect:
    # Rectangle
    back_rectangle_left = cfg.SCREEN_WIDTH - 2 * cfg.CIRCLE_RADIUS - 100
    back_rectangle_top = cfg.SCREEN_HEIGHT - 120
    back_rectangle_width = 2 * cfg.CIRCLE_RADIUS
    back_rectangle_height = 70

    back_rectangle = pygame.rect.Rect(
        back_rectangle_left,
        back_rectangle_top,
        back_rectangle_width,
        back_rectangle_height,
    )
    pygame.draw.rect(self.screen, cfg.GAME_COLORS["WHITE"], back_rectangle)

    # Text
    hide_board_font = pygame.font.Font(None, 24)
    hide_board_text = hide_board_font.render("BACK", True, cfg.GAME_COLORS["BLACK"])
    hide_board_text_rect = hide_board_text.get_rect()
    hide_board_text_rect.center = (
        back_rectangle_left + back_rectangle_width // 2,
        back_rectangle_top + back_rectangle_height // 2,
    )
    self.screen.blit(hide_board_text, hide_board_text_rect.topleft)

    return back_rectangle
