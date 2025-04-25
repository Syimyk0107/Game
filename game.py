import pygame
import random

# Настройки
CELL_SIZE = 60
GRID_SIZE = 5
MARGIN = 30
WINDOW_WIDTH = CELL_SIZE * GRID_SIZE * 2 + MARGIN * 3
WINDOW_HEIGHT = CELL_SIZE * GRID_SIZE + MARGIN * 2

# Цвета
BLUE = (0, 150, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Морской бой 2D")
font = pygame.font.SysFont(None, 32)

# Создание пустого поля
def create_field():
    return [["~"] * GRID_SIZE for _ in range(GRID_SIZE)]

# Расставим корабли случайно
def place_ships(field, num=3):
    placed = 0
    while placed < num:
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        if field[y][x] == "~":
            field[y][x] = "S"
            placed += 1

# Отображение сетки
def draw_grid(field, offset_x, offset_y, hide_ships=False):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLUE, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            value = field[y][x]
            if value == "X":
                pygame.draw.line(screen, RED, rect.topleft, rect.bottomright, 3)
                pygame.draw.line(screen, RED, rect.topright, rect.bottomleft, 3)
            elif value == "O":
                pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE // 4, 2)
            elif value == "S" and not hide_ships:
                pygame.draw.rect(screen, GREEN, rect.inflate(-10, -10))

# Получение координат клетки по клику
def get_cell(pos, offset_x, offset_y):
    x, y = pos
    grid_x = (x - offset_x) // CELL_SIZE
    grid_y = (y - offset_y) // CELL_SIZE
    if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
        return grid_x, grid_y
    return None

# Инициализация полей
player_field = create_field()
enemy_field = create_field()
place_ships(player_field)
place_ships(enemy_field)

# Основной игровой цикл
running = True
while running:
    screen.fill(GRAY)

    # Отрисовка полей
    draw_grid(player_field, MARGIN, MARGIN)
    draw_grid(enemy_field, MARGIN * 2 + GRID_SIZE * CELL_SIZE, MARGIN, hide_ships=True)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Получаем координаты клетки
            cell = get_cell(event.pos, MARGIN * 2 + GRID_SIZE * CELL_SIZE, MARGIN)
            if cell:
                x, y = cell
                # Здесь можно добавлять логику для попадания/промаха

pygame.quit()
