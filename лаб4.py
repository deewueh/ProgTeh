import pygame
import sys

CELL_SIZE = 50
GRID_SIZE = 10
WINDOW_SIZE = CELL_SIZE * GRID_SIZE
EXTRA_HEIGHT = 50
WHITE = (255, 255, 255)
PINK = (255, 192, 203)
PURPLE = (204, 204, 255)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + EXTRA_HEIGHT))
pygame.display.set_caption("Игра 4 в ряд")
font = pygame.font.SysFont(None, 21)

grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_player = PINK
game_over = False
winner = None


def draw_grid():
    screen.fill(WHITE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = grid[row][col] if grid[row][col] else WHITE
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)


def display_message(text):
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (WINDOW_SIZE // 2 - text_surface.get_width() // 2, WINDOW_SIZE + 10))


def check_winner(row, col):
    def check_direction(dx, dy):
        count = 0
        x, y = col, row
        while 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and grid[y][x] == current_player:
            count += 1
            x += dx
            y += dy
        x, y = col - dx, row - dy
        while 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and grid[y][x] == current_player:
            count += 1
            x -= dx
            y -= dy
        return count >= 4

    return (check_direction(1, 0) or
            check_direction(0, 1) or
            check_direction(1, 1) or
            check_direction(-1, 1))


def reset_game():
    global grid, current_player, game_over, winner
    grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current_player = PINK
    game_over = False
    winner = None


def main():
    global current_player, game_over, winner

    while True:
        draw_grid()

        if game_over:
            display_message(
                f"Победил {'Розовый' if winner == PINK else 'Фиолетовый'}. Нажмите R для новой игры или Q для выхода.")
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = pygame.mouse.get_pos()
                if y < WINDOW_SIZE:
                    col, row = x // CELL_SIZE, y // CELL_SIZE

                    if grid[row][col] is None:
                        grid[row][col] = current_player

                        if check_winner(row, col):
                            winner = current_player
                            game_over = True
                        else:
                            current_player = PURPLE if current_player == PINK else PINK


main()
