import pygame
import random


CELL_SIZE = 60
GRID_SIZE = 5
MARGIN = 30
NUM_SHIPS = 3
WINDOW_WIDTH = CELL_SIZE * GRID_SIZE * 2 + MARGIN * 3
WINDOW_HEIGHT = CELL_SIZE * GRID_SIZE + MARGIN * 2


WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Морской бой 2D")
font = pygame.font.SysFont(None, 32)


def create_field():
    return [["~"] * GRID_SIZE for _ in range(GRID_SIZE)]

def place_ships(field, num=NUM_SHIPS):
    placed = 0
    while placed < num:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        if field[y][x] == "~":
            field[y][x] = "S"
            placed += 1

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

def get_cell(pos, offset_x, offset_y):
    x, y = pos
    grid_x = (x - offset_x) // CELL_SIZE
    grid_y = (y - offset_y) // CELL_SIZE
    if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
        return grid_x, grid_y
    return None

def count_ships(field):
    return sum(row.count("S") for row in field)


player_field = create_field()
enemy_field = create_field()
place_ships(player_field)
place_ships(enemy_field)

running = True
player_turn = True
game_over = False
winner = ""


while running:
    screen.fill(GRAY)

    
    draw_grid(player_field, MARGIN, MARGIN)
    draw_grid(enemy_field, MARGIN * 2 + GRID_SIZE * CELL_SIZE, MARGIN, hide_ships=True)

    
    if game_over:
        msg = font.render(f"{winner} победил!", True, RED)
        screen.blit(msg, (WINDOW_WIDTH // 2 - 80, 10))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and player_turn and not game_over:
            cell = get_cell(event.pos, MARGIN * 2 + GRID_SIZE * CELL_SIZE, MARGIN)
            if cell:
                x, y = cell
                if enemy_field[y][x] not in ["X", "O"]:
                    if enemy_field[y][x] == "S":
                        enemy_field[y][x] = "X"
                        print("🔥 Попадание!")
                    else:
                        enemy_field[y][x] = "O"
                        print("💨 Промах!")
                        player_turn = False

        if not player_turn and not game_over:
            pygame.time.delay(500)
            while True:
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, GRID_SIZE - 1)
                if player_field[y][x] not in ["X", "O"]:
                    if player_field[y][x] == "S":
                        player_field[y][x] = "X"
                        print("💥 Компьютер попал!")
                    else:
                        player_field[y][x] = "O"
                        print("👾 Компьютер промахнулся.")
                        player_turn = True
                    break

        
        if count_ships(enemy_field) == 0 and not game_over:
            game_over = True
            winner = "Игрок"
        elif count_ships(player_field) == 0 and not game_over:
            game_over = True
            winner = "Компьютер"

pygame.quit()
