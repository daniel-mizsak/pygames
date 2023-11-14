"""
Drawing functions.

@author "Dániel Lajos Mizsák" <info@pythonvilag.hu>
"""

import config as cfg
import pygame
import pygame.freetype

pygame.freetype.init()

HUGE_FONT = pygame.freetype.SysFont(cfg.FONT_TYPE, cfg.HUGE_TEXT_SIZE)
LARGE_FONT = pygame.freetype.SysFont(cfg.FONT_TYPE, cfg.LARGE_TEXT_SIZE)
MEDIUM_FONT = pygame.freetype.SysFont(cfg.FONT_TYPE, cfg.MEDIUM_TEXT_SIZE)
SMALL_FONT = pygame.freetype.SysFont(cfg.FONT_TYPE, cfg.SMALL_TEXT_SIZE)


def draw_text(screen, text_data):
    text_data["font"] = pygame.freetype.SysFont(cfg.FONT_TYPE, text_data["font"])
    order_rect = text_data["font"].get_rect(str(text_data["text"]))
    order_rect.center = text_data["center"]
    text_data["font"].render_to(
        screen, order_rect.topleft, str(text_data["text"]), cfg.GAME_COLORS[text_data["color"]]
    )


def generate_background_square(index):
    background_square = pygame.Rect(
        (
            index * cfg.BACKGROUND_SQUARE_SIDE + (index + 1) * cfg.GAP_SIZE,
            int(cfg.BACKGROUND_SQUARE_SIDE / 2),
            cfg.BACKGROUND_SQUARE_SIDE,
            cfg.BACKGROUND_SQUARE_SIDE,
        )
    )
    return background_square


# Order phase
def draw_order_phase(self):
    for index, unit in enumerate(self.units):
        background_square = generate_background_square(index)
        pygame.draw.rect(self.screen, cfg.GAME_COLORS["SQUARE_BACKGROUND"], background_square)

        order_text = {
            "font": calculate_font_size(self.current_time),
            "text": unit.order,
            "color": "WHITE",
            "center": background_square.center,
        }
        draw_text(self.screen, order_text)


def calculate_font_size(
    current_time,
    font_size=cfg.HUGE_TEXT_SIZE,
    start_time=cfg.START_TIME,
):
    decay_start = 1 / 3
    if current_time < start_time * decay_start:
        return font_size
    else:
        return max(
            int(
                font_size / (1 - decay_start)
                - current_time * font_size / start_time / (1 - decay_start)
            ),
            1,
        )


# Solve phase
def draw_solve_phase(self):
    for index, unit in enumerate(self.units):
        background_square = generate_background_square(index)
        pygame.draw.rect(self.screen, cfg.GAME_COLORS[unit.background_color], background_square)

        draw_unit(self.screen, background_square, unit.shape, unit.shape_color)
        draw_solve_texts(self, background_square, unit)
        draw_timer(self)
        draw_input(self)


def draw_unit(screen, background_square, shape, shape_color):
    shape_center = background_square.center
    if shape == "SQUARE":
        square = background_square.copy()
        square.width = cfg.SQUARE_SIDE
        square.height = cfg.SQUARE_SIDE
        square.center = shape_center
        pygame.draw.rect(screen, cfg.GAME_COLORS[shape_color], square)

    elif shape == "RECTANGLE":
        rectangle = background_square.copy()
        rectangle.width = cfg.SQUARE_SIDE * 1.2
        rectangle.height = cfg.SQUARE_SIDE / 1.2
        rectangle.center = shape_center
        pygame.draw.rect(screen, cfg.GAME_COLORS[shape_color], rectangle)

    elif shape == "TRIANGLE":
        pygame.draw.polygon(
            screen,
            cfg.GAME_COLORS[shape_color],
            [
                [shape_center[0], shape_center[1] - cfg.TRIANGLE_SIZE],
                [shape_center[0] - cfg.TRIANGLE_SIZE, shape_center[1] + cfg.TRIANGLE_SIZE],
                [shape_center[0] + cfg.TRIANGLE_SIZE, shape_center[1] + cfg.TRIANGLE_SIZE],
            ],
            0,
        )

    elif shape == "CIRCLE":
        pygame.draw.circle(screen, cfg.GAME_COLORS[shape_color], shape_center, cfg.CIRCLE_RADIUS)


def draw_solve_texts(self, background_square, unit):
    color_text = {
        "font": cfg.MEDIUM_TEXT_SIZE,
        "text": unit.color_text,
        "color": unit.text_color,
        "center": (
            background_square.center[0],
            background_square.center[1] - int(cfg.MEDIUM_TEXT_SIZE * 1.2),
        ),
    }
    draw_text(self.screen, color_text)

    shape_text = {
        "font": cfg.MEDIUM_TEXT_SIZE,
        "text": unit.shape_text,
        "color": unit.text_color,
        "center": (
            background_square.center[0],
            background_square.center[1] + int(cfg.MEDIUM_TEXT_SIZE * 1.2),
        ),
    }
    draw_text(self.screen, shape_text)

    number_text = {
        "font": cfg.LARGE_TEXT_SIZE,
        "text": unit.number,
        "color": unit.number_color,
        "center": background_square.center,
    }
    draw_text(self.screen, number_text)

    score_text = {
        "font": cfg.MEDIUM_TEXT_SIZE,
        "text": f"Score: {self.score}",
        "color": "WHITE",
        "center": (cfg.SCREEN_WIDTH * 0.9, cfg.SCREEN_HEIGHT * 0.1),
    }
    draw_text(self.screen, score_text)

    task_text = {
        "font": cfg.SMALL_TEXT_SIZE,
        "text": self.task_text,
        "color": "WHITE",
        "center": (cfg.SCREEN_WIDTH * 0.5, cfg.SCREEN_HEIGHT * 0.8),
    }
    draw_text(self.screen, task_text)


def draw_timer(self):
    timer_bg = pygame.Rect((0, 0, int(cfg.SCREEN_WIDTH * 0.95), 5))
    timer_bg.center = (int(cfg.SCREEN_WIDTH * 0.5), int(cfg.SCREEN_HEIGHT * 0.75))
    pygame.draw.rect(self.screen, cfg.GAME_COLORS["DARK_ORANGE"], timer_bg)

    if not self.game_over:
        timer_fg = timer_bg.copy()
        timer_fg.width = timer_bg.width * (
            1 - (self.current_time - cfg.START_TIME) / cfg.SOLVE_TIME
        )
        timer_fg.center = (int(cfg.SCREEN_WIDTH * 0.5), int(cfg.SCREEN_HEIGHT * 0.75))
        pygame.draw.rect(self.screen, cfg.GAME_COLORS["LIGHT_ORANGE"], timer_fg)


def draw_input(self):
    input_font = pygame.font.Font(None, cfg.SMALL_TEXT_SIZE)

    input_box = pygame.Rect(0, 0, 300, 32)
    input_box.center = (int(cfg.SCREEN_WIDTH * 0.5), int(cfg.SCREEN_HEIGHT * 0.9))

    txt_surface = input_font.render(self.input_text, True, cfg.GAME_COLORS["WHITE"])
    self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(self.screen, cfg.GAME_COLORS["WHITE"], input_box, 2)


# Solution phase
def draw_solution_phase(self):
    draw_solution(self)
    draw_play_again(self)


def draw_solution(self):
    solution_bg = pygame.Rect((0, 0, 800, 100))
    solution_bg.center = (int(cfg.SCREEN_WIDTH * 0.5), int(cfg.SCREEN_HEIGHT * 0.65))
    pygame.draw.rect(self.screen, cfg.GAME_COLORS["GREEN"], solution_bg, border_radius=20)

    solution_order = f'ORDER: {" ".join([str(u.order) for u in self.units])}'
    solution_order_rect = pygame.freetype.SysFont(cfg.FONT_TYPE, cfg.SMALL_TEXT_SIZE).get_rect(
        solution_order
    )
    solution_order_rect.center = (int(cfg.SCREEN_WIDTH * 0.5), int(cfg.SCREEN_HEIGHT * 0.65 - 20))
    pygame.freetype.SysFont(cfg.FONT_TYPE, cfg.SMALL_TEXT_SIZE).render_to(
        self.screen, solution_order_rect.topleft, solution_order, cfg.GAME_COLORS["WHITE"]
    )

    solution_text = "SOLUTION: " + self.solution_text.upper()
    solution_text_rect = SMALL_FONT.get_rect(solution_text)
    solution_text_rect.center = (int(cfg.SCREEN_WIDTH * 0.5), int(cfg.SCREEN_HEIGHT * 0.65 + 20))
    SMALL_FONT.render_to(
        self.screen, solution_text_rect.topleft, solution_text, cfg.GAME_COLORS["WHITE"]
    )


def draw_play_again(self):
    play_again_text_rect = pygame.freetype.SysFont(
        cfg.FONT_TYPE, int(cfg.SMALL_TEXT_SIZE)
    ).get_rect("Play Again?")
    play_again_text_rect.center = (int(cfg.SCREEN_WIDTH * 0.5 + 300), int(cfg.SCREEN_HEIGHT * 0.9))

    self.mouse_position = pygame.mouse.get_pos()

    if is_mouse_hovering_button(self.mouse_position, play_again_text_rect):
        self.mouse_active = True
        play_again_text_color = "WHITE"
    else:
        self.mouse_active = False
        play_again_text_color = "SQUARE_BACKGROUND"

    SMALL_FONT.render_to(
        self.screen,
        play_again_text_rect.topleft,
        "Play Again?",
        cfg.GAME_COLORS[play_again_text_color],
    )


def is_mouse_hovering_button(mouse, play_again_text_rect):
    x = mouse[0]
    y = mouse[1]

    x_min = play_again_text_rect.topleft[0]
    x_max = play_again_text_rect.topleft[0] + play_again_text_rect.width
    y_min = play_again_text_rect.topleft[1]
    y_max = play_again_text_rect.topleft[1] + play_again_text_rect.height

    if x_min <= x <= x_max and y_min <= y <= y_max:
        return True
    return False
