import pygame
import random

# 初期化
pygame.init()

# 色定義
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
DARK_GRAY = (64, 64, 64)
LIGHT_BLACK = (32, 32, 32)
WHITE = (255, 255, 255)
LIGHT_GRAY = (192, 192, 192)
VERY_LIGHT_GRAY = (224, 224, 224)
GRID_COLOR = WHITE

# ボード設定
CELL_SIZE = 50
BOARD_SIZE = 16
WINDOW_SIZE = CELL_SIZE * BOARD_SIZE
SCREEN_HEIGHT = WINDOW_SIZE + 100
LOG_WIDTH = 300

screen = pygame.display.set_mode((WINDOW_SIZE, SCREEN_HEIGHT))  # 初期の画面サイズ
pygame.display.set_caption("Quantum_Gomoku")

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
large_font = pygame.font.Font(None, 72)

class Stone:
    def __init__(self, x, y, probability, player):
        self.x = x
        self.y = y
        self.probability = probability
        self.player = player
        self.color, self.text_color = get_color_and_text(player, probability)
        self.observed = False
        self.original_color = self.color

    def observe(self):
        if random.random() < self.probability:
            self.color, self.text_color = (BLACK, WHITE)
        else:
            self.color, self.text_color = (WHITE, BLACK)
        self.observed = True

    def reset(self):
        self.color = self.original_color
        self.observed = False
        self.color, self.text_color = get_color_and_text(self.player, self.probability)

def draw_board():
    screen.fill(GREEN)
    for x in range(0, WINDOW_SIZE, CELL_SIZE):
        for y in range(0, WINDOW_SIZE, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)

    for i in range(BOARD_SIZE):
        num_surface = small_font.render(str(i + 1), True, BLACK)
        screen.blit(num_surface, (i * CELL_SIZE + CELL_SIZE // 2 - num_surface.get_width() // 2, 0))
        screen.blit(num_surface, (0, i * CELL_SIZE + CELL_SIZE // 2 - num_surface.get_height() // 2))

def get_color_and_text(player, probability):
    if player == "black":
        if probability == 0.9:
            return LIGHT_BLACK, WHITE
        elif probability == 0.7:
            return DARK_GRAY, WHITE
    elif player == "white":
        if probability == 0.1:
            return VERY_LIGHT_GRAY, BLACK
        elif probability == 0.3:
            return LIGHT_GRAY, BLACK

def place_stone(stone):
    pygame.draw.circle(screen, stone.color, (stone.x * CELL_SIZE + CELL_SIZE // 2, stone.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
    pygame.draw.circle(screen, BLACK if stone.color in [WHITE, VERY_LIGHT_GRAY, LIGHT_GRAY] else WHITE, (stone.x * CELL_SIZE + CELL_SIZE // 2, stone.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5, 2)
    
    text_surface = font.render(f"{int(stone.probability * 100)}", True, stone.text_color)
    text_rect = text_surface.get_rect(center=(stone.x * CELL_SIZE + CELL_SIZE // 2, stone.y * CELL_SIZE + CELL_SIZE // 2))
    screen.blit(text_surface, text_rect)

def draw_buttons():
    pygame.draw.rect(screen, WHITE, (WINDOW_SIZE // 2 - 50, SCREEN_HEIGHT - 70, 100, 40))
    button_text = "Observe" if not observed else ("Continue" if winner is None else "Reset")
    text_surface = font.render(button_text, True, BLACK)
    text_rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, SCREEN_HEIGHT - 50))
    screen.blit(text_surface, text_rect)

def display_winner(winner):
    winner_text = f"{winner} wins!"
    text_surface = large_font.render(winner_text, True, BLACK)
    text_rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
    screen.blit(text_surface, text_rect)

def observe_board():
    for row in board:
        for stone in row:
            if stone is not None and not stone.observed:
                stone.observe()

def reset_observations():
    for row in board:
        for stone in row:
            if stone is not None and stone.observed:
                stone.reset()

def check_winner():
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] is not None and board[x][y].observed:
                stone = board[x][y]
                for direction in directions:
                    count = 1
                    for i in range(1, 5):
                        nx, ny = x + direction[0] * i, y + direction[1] * i
                        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[nx][ny] is not None and board[nx][ny].observed:
                            next_stone = board[nx][ny]
                            if next_stone.color == stone.color:
                                count += 1
                            else:
                                break
                        else:
                            break
                    if count >= 5:
                        return stone.player
    return None

def reset_game():
    global board, current_player, turn_count, observed, winner, log
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    current_player = "black"
    turn_count = 0
    observed = False
    winner = None
    log = []

def draw_menu():
    screen.fill(GREEN)
    title_surface = large_font.render("Quantum Gomoku", True, BLACK)
    title_rect = title_surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 4))
    screen.blit(title_surface, title_rect)

    vs_cpu_button = pygame.Rect(WINDOW_SIZE // 2 - 100, WINDOW_SIZE // 2, 200, 50)
    vs_player_button = pygame.Rect(WINDOW_SIZE // 2 - 100, WINDOW_SIZE // 2 + 70, 200, 50)
    
    pygame.draw.rect(screen, WHITE, vs_cpu_button)
    pygame.draw.rect(screen, WHITE, vs_player_button)
    
    vs_cpu_text = font.render("VS CPU", True, BLACK)
    vs_player_text = font.render("VS Player", True, BLACK)
    
    vs_cpu_text_rect = vs_cpu_text.get_rect(center=vs_cpu_button.center)
    vs_player_text_rect = vs_player_text.get_rect(center=vs_player_button.center)
    
    screen.blit(vs_cpu_text, vs_cpu_text_rect)
    screen.blit(vs_player_text, vs_player_text_rect)
    
    return vs_cpu_button, vs_player_button

def draw_log(log, scroll_pos):
    log_area = pygame.Rect(WINDOW_SIZE, 0, LOG_WIDTH, WINDOW_SIZE)
    pygame.draw.rect(screen, WHITE, log_area)
    max_lines = WINDOW_SIZE // small_font.get_height()
    visible_log = log[scroll_pos:scroll_pos + max_lines]

    for i, entry in enumerate(visible_log):
        log_surface = small_font.render(entry, True, BLACK)
        screen.blit(log_surface, (WINDOW_SIZE + 10, i * small_font.get_height()))

running = True
current_player = "black"
board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
turn_count = 0
observed = False
winner = None
game_started = False
log = []
scroll_pos = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if game_started:
                if WINDOW_SIZE // 2 - 50 <= x <= WINDOW_SIZE // 2 + 50 and SCREEN_HEIGHT - 70 <= y <= SCREEN_HEIGHT - 30:
                    if winner is not None:
                        reset_game()
                    elif observed:
                        reset_observations()
                        observed = False
                    else:
                        observe_board()
                        winner = check_winner()
                        observed = True
                elif not observed and winner is None:
                    grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                    if 0 <= grid_x < BOARD_SIZE and 0 <= grid_y < BOARD_SIZE and board[grid_x][grid_y] is None:
                        turn_count += 1
                        remainder = turn_count % 4
                        if remainder == 1:
                            probability = 0.9
                        elif remainder == 2:
                            probability = 0.1
                        elif remainder == 3:
                            probability = 0.7
                        elif remainder == 0:
                            probability = 0.3
                        board[grid_x][grid_y] = Stone(grid_x, grid_y, probability, current_player)
                        log.append(f"{current_player.capitalize()} {turn_count}: ({grid_y + 1},{grid_x + 1})")
                        current_player = "white" if current_player == "black" else "black"
            else:
                vs_cpu_button, vs_player_button = draw_menu()
                if vs_cpu_button.collidepoint(x, y) or vs_player_button.collidepoint(x, y):
                    game_started = True
                    screen = pygame.display.set_mode((WINDOW_SIZE + LOG_WIDTH, SCREEN_HEIGHT))  # ゲーム画面に遷移する際にログ用スペースを確保

        elif event.type == pygame.MOUSEWHEEL:
            if game_started:
                scroll_pos = max(0, min(scroll_pos - event.y, len(log) - 1))

    if game_started:
        draw_board()
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if board[x][y] is not None:
                    place_stone(board[x][y])

        draw_buttons()
        if winner:
            display_winner(winner)
        draw_log(log, scroll_pos)
    else:
        vs_cpu_button, vs_player_button = draw_menu()

    pygame.display.flip()

pygame.quit()
