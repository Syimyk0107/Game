import pygame
import random

CELL_SIZE = 40
GRID_SIZE = 10
WIDTH = HEIGHT = CELL_SIZE * GRID_SIZE * 2 + 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

background_img = pygame.image.load("Sea.jpg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
bg_y = 0  
def draw_moving_background():
    global bg_y
    rel_y = bg_y % HEIGHT
    screen.blit(background_img, (0, rel_y - HEIGHT))
    screen.blit(background_img, (0, rel_y))
    bg_y += 1 
    

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Морской Бой")
FONT = pygame.font.SysFont("arial", 24)

hit_sound = pygame.mixer.Sound("C:/Users/Notnik_kg/Music/effect.mp3")
miss_sound = pygame.mixer.Sound("C:/Users/Notnik_kg/Music/ship_miss.mp3")

def create_board():
    return [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

player1_board = create_board()
player2_board = create_board()
hits_on_p2 = create_board()
hits_on_p1 = create_board()

def draw_grid(board, hits, offset_x, offset_y, show_ships=False):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            rect = pygame.Rect(i * CELL_SIZE + offset_x, j * CELL_SIZE + offset_y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLUE, rect, 1)
            if show_ships and board[j][i] == 1:
                pygame.draw.rect(screen, GRAY, rect)
            if hits[j][i] == 1:
                pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 4)
            elif hits[j][i] == -1:
                pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE // 4)

def place_ships(board):
    sizes = [4, 3, 3, 2, 2, 1, 1]
    for size in sizes:
        placed = False
        while not placed:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            orientation = random.choice(['H', 'V'])
            if orientation == 'H' and x + size <= GRID_SIZE and all(board[y][x + i] == 0 for i in range(size)):
                for i in range(size):
                    board[y][x + i] = 1
                placed = True
            elif orientation == 'V' and y + size <= GRID_SIZE and all(board[y + i][x] == 0 for i in range(size)):
                for i in range(size):
                    board[y + i][x] = 1
                placed = True

def get_cell(pos, offset_x):
    x, y = pos
    x -= offset_x
    y -= 30
    if 0 <= x < CELL_SIZE * GRID_SIZE and 0 <= y < CELL_SIZE * GRID_SIZE:
        return x // CELL_SIZE, y // CELL_SIZE
    return None

def show_menu():
    screen.fill(WHITE)
    title = FONT.render("Выберите режим игры", True, BLACK)
    pvp_text = FONT.render("1. Игрок против Игрока", True, BLACK)
    pvc_text = FONT.render("2. Игрок против Компьютера", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(pvp_text, (WIDTH // 2 - pvp_text.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(pvc_text, (WIDTH // 2 - pvc_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "PVP"
                elif event.key == pygame.K_2:
                    return "PVC"

def check_victory(board, hits):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if board[y][x] == 1 and hits[y][x] != 1:
                return False
    return True

def show_winner(winner_text):
    screen.fill(WHITE)
    text = FONT.render(winner_text, True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

def show_turn_text(player_number):
    screen.fill(WHITE)
    text = FONT.render(f"Ход Игрока {player_number}", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2000) 

mode = show_menu()  
place_ships(player1_board)
place_ships(player2_board)
turn = True  # True — игрок 1, False — игрок 2 или компьютер
running = True
game_over = False

draw_moving_background()
while running:
    
    if mode == "PVP":  
        if turn:
            draw_grid(player1_board, hits_on_p1, 30, 30, True)
            draw_grid(player2_board, hits_on_p2, WIDTH // 2 + 30, 30, False)
        else:
            
            draw_grid(player1_board, hits_on_p1, 30, 30, False)
            draw_grid(player2_board, hits_on_p2, WIDTH // 2 + 30, 30, True)
    elif mode == "PVC":  
        if turn:
            draw_grid(player1_board, hits_on_p1, 30, 30, True)
            draw_grid(player2_board, hits_on_p2, WIDTH // 2 + 30, 30, False)
        else:
            draw_grid(player1_board, hits_on_p1, 30, 30, False)
            draw_grid(player2_board, hits_on_p2, WIDTH // 2 + 30, 30, True)

    pygame.display.flip() 

    if game_over:
        break  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if turn:  
                cell = get_cell(pygame.mouse.get_pos(), WIDTH // 2 + 30)
                if cell:
                    x, y = cell
                    if hits_on_p2[y][x] == 0:  
                        if player2_board[y][x] == 1:
                            hits_on_p2[y][x] = 1
                            hit_sound.play()
                            if check_victory(player2_board, hits_on_p2):
                                show_winner("Игрок 1 победил!")
                                game_over = True
                        else:
                            hits_on_p2[y][x] = -1
                            miss_sound.play()
                            turn = False  
                            show_turn_text(2)
            else:  
                cell = get_cell(pygame.mouse.get_pos(), 30)
                if cell:
                    x, y = cell
                    if hits_on_p1[y][x] == 0: 
                        if player1_board[y][x] == 1:
                            hits_on_p1[y][x] = 1
                            hit_sound.play()
                            if check_victory(player1_board, hits_on_p1):
                                show_winner("Игрок 2 победил!")
                                game_over = True
                        else:
                            hits_on_p1[y][x] = -1
                            miss_sound.play()
                            turn = True  
                            show_turn_text(1)

        if mode == "PVC" and not turn and not game_over:
            pygame.time.wait(500)  
            
            while True:
                draw_moving_background()
                x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
                if hits_on_p1[y][x] == 0:  
                    if player1_board[y][x] == 1:
                        hits_on_p1[y][x] = 1
                        hit_sound.play()
                        if check_victory(player1_board, hits_on_p1):
                            show_winner("Компьютер победил!")
                            game_over = True
                    else:
                        hits_on_p1[y][x] = -1
                        miss_sound.play()
                        turn = True 
                        show_turn_text("")
                    break

