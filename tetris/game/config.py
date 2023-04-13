### WINDOW ###
GAME_TITLE = "Tetris"

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
WINDOW_POS_LEFT = 500
WINDOW_POS_TOP = 200

### BOARD ###
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

### GAME ###
GAME_COLORS = {
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "ORANGE": (255, 127, 0),
    "PURPLE": (128, 0, 128),
    "CYAN": (0, 255, 255),
    "BLACK": (0, 0, 0),
}

TETROMINOS = {
    "I": {"shape": ((1, 1, 1, 1),), "color": GAME_COLORS["CYAN"]},
    "J": {"shape": ((1, 0, 0), (1, 1, 1)), "color": GAME_COLORS["BLUE"]},
    "L": {"shape": ((0, 0, 1), (1, 1, 1)), "color": GAME_COLORS["ORANGE"]},
    "O": {"shape": ((1, 1), (1, 1)), "color": GAME_COLORS["YELLOW"]},
    "S": {"shape": ((0, 1, 1), (1, 1, 0)), "color": GAME_COLORS["GREEN"]},
    "T": {"shape": ((0, 1, 0), (1, 1, 1)), "color": GAME_COLORS["PURPLE"]},
    "Z": {"shape": ((1, 1, 0), (0, 1, 1)), "color": GAME_COLORS["RED"]},
}
