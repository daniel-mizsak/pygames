import pygame


def draw_board(board):
    board_surface = pygame.Surface((board.shape[1], board.shape[0]))
    board_surface.fill([0, 0, 0])
    for x in range(board.shape[1]):
        for y in range(board.shape[0]):
            if board[y, x]:
                color = Tile.colors[board[y, x] - 1]
                board_surface.set_at((x, y), color)
    return board_surface


def draw_tile(tile, board_surface):
    tile_surface = pygame.Surface((tile.shape.shape[1], tile.shape.shape[0]))
    tile_surface.fill([0, 0, 0])
    tile_surface.set_colorkey([0, 0, 0])
    for x in range(tile.shape.shape[1]):
        for y in range(tile.shape.shape[0]):
            if tile.shape[y, x]:
                color = Tile.colors[tile.shape[y, x] - 1]
                tile_surface.set_at((x, y), color)
    board_surface.blit(tile_surface, (tile.pos[1], tile.pos[0]))
