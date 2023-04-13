"""
Drawing functions.

@author Dániel Lajos Mizsák info@pythonvilag.hu
"""

import config as cfg
import pygame
import pygame.freetype


def draw_order_phase(self):
    self.mouse_active = "disabled"

    for y in range(cfg.BOARD_DIMENSION):
        for x in range(cfg.BOARD_DIMENSION):
            x_top_left = cfg.GAP_SIZE / 2 + x * (cfg.GAP_SIZE + cfg.TILE_SIZE)
            y_top_left = cfg.GAP_SIZE / 2 + y * (cfg.GAP_SIZE + cfg.TILE_SIZE)

            tile_color = "SQUARE_BACKGROUND"
            if self.board.is_tile_active(x, y):
                tile_color = "WHITE"

            tile = pygame.Rect(
                (int(x_top_left), int(y_top_left), int(cfg.TILE_SIZE), int(cfg.TILE_SIZE))
            )
            pygame.draw.rect(self.screen, cfg.GAME_COLORS[tile_color], tile)


def draw_solve_phase(self):
    self.mouse_active = "enabled"

    for y in range(cfg.BOARD_DIMENSION):
        for x in range(cfg.BOARD_DIMENSION):
            x_top_left = cfg.GAP_SIZE / 2 + x * (cfg.GAP_SIZE + cfg.TILE_SIZE)
            y_top_left = cfg.GAP_SIZE / 2 + y * (cfg.GAP_SIZE + cfg.TILE_SIZE)

            tile_color = "SQUARE_BACKGROUND"
            if (x, y) in self.board.correctly_guessed_tiles:
                tile_color = "WHITE"
            elif (x, y) in self.board.wrongly_guess_tiles:
                tile_color = "RED"

            tile = pygame.Rect(
                (int(x_top_left), int(y_top_left), int(cfg.TILE_SIZE), int(cfg.TILE_SIZE))
            )
            pygame.draw.rect(self.screen, cfg.GAME_COLORS[tile_color], tile)


def draw_solution_phase(self):
    for y in range(cfg.BOARD_DIMENSION):
        for x in range(cfg.BOARD_DIMENSION):
            x_top_left = cfg.GAP_SIZE / 2 + x * (cfg.GAP_SIZE + cfg.TILE_SIZE)
            y_top_left = cfg.GAP_SIZE / 2 + y * (cfg.GAP_SIZE + cfg.TILE_SIZE)

            tile_color = "SQUARE_BACKGROUND"
            if (x, y) in self.board.correctly_guessed_tiles:
                tile_color = "WHITE"
            elif (x, y) in self.board.wrongly_guess_tiles:
                tile_color = "RED"
            elif (x, y) not in self.board.correctly_guessed_tiles and (
                x,
                y,
            ) in self.board.correct_tiles:
                tile_color = "GREEN"

            tile = pygame.Rect(
                (int(x_top_left), int(y_top_left), int(cfg.TILE_SIZE), int(cfg.TILE_SIZE))
            )
            pygame.draw.rect(self.screen, cfg.GAME_COLORS[tile_color], tile)

    draw_play_again(self)


def draw_play_again(self):
    play_again_text_rect = pygame.freetype.SysFont(cfg.FONT_TYPE, int(cfg.TEXT_SIZE)).get_rect(
        "Play Again?"
    )
    play_again_text_rect.center = (int(cfg.SCREEN_WIDTH * 0.5), int(cfg.SCREEN_HEIGHT * 0.9))

    if is_mouse_hovering_button(pygame.mouse.get_pos(), play_again_text_rect):
        self.mouse_active = "play_again"
        play_again_text_color = "WHITE"
    else:
        self.mouse_active = "disabled"
        play_again_text_color = "SQUARE_BACKGROUND"

    pygame.freetype.SysFont(cfg.FONT_TYPE, cfg.TEXT_SIZE).render_to(
        self.screen,
        play_again_text_rect.topleft,
        "Play Again?",
        cfg.GAME_COLORS[play_again_text_color],
    )


def is_mouse_hovering_button(mouse_position, play_again_text_rect):
    x, y = mouse_position
    x_min = play_again_text_rect.topleft[0]
    x_max = play_again_text_rect.topleft[0] + play_again_text_rect.width
    y_min = play_again_text_rect.topleft[1]
    y_max = play_again_text_rect.topleft[1] + play_again_text_rect.height

    if x_min <= x <= x_max and y_min <= y <= y_max:
        return True
    return False
