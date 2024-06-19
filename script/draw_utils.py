import pygame
import random

# 色定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLACK = (32, 32, 32)
DARK_GRAY = (64, 64, 64)
VERY_LIGHT_GRAY = (224, 224, 224)
LIGHT_GRAY = (192, 192, 192)
GREEN = (34, 139, 34)
GRID_COLOR = WHITE
ORANGE = (255, 165, 0)

# フォント初期化を追加
pygame.font.init()  # この行を追加

font = pygame.font.Font(None, 24)
small_font = pygame.font.Font(None, 24)
large_font = pygame.font.Font(None, 72)

def draw_board(screen, window_size, cell_size, board_size, last_move=None):
    screen.fill(GREEN)
    for x in range(0, window_size, cell_size):
        for y in range(0, window_size, cell_size):
            rect = pygame.Rect(x, y, cell_size, cell_size)
            if last_move and x // cell_size == last_move[0] and y // cell_size == last_move[1]:
                pygame.draw.rect(screen, ORANGE, rect, 3)  # 直前の移動位置をオレンジ色で囲む
            else:
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)

    for i in range(board_size):
        num_surface = small_font.render(str(i + 1), True, BLACK)
        screen.blit(num_surface, (i * cell_size + cell_size // 2 - num_surface.get_width() // 2, 0))
        screen.blit(num_surface, (0, i * cell_size + cell_size // 2 - num_surface.get_height() // 2))

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

def draw_buttons(screen, window_size, screen_height, observed, winner, observe_counts, observe_mode):
    pygame.draw.rect(screen, WHITE, (window_size // 2 - 75, screen_height - 70, 150, 40))
    if winner is not None:
        button_text = "Reset"
    elif observed:
        button_text = "Continue"
    elif observe_mode:
        button_text = "Cancel Observing"
    else:
        button_text = "Observe"
    text_surface = font.render(button_text, True, BLACK)
    text_rect = text_surface.get_rect(center=(window_size // 2, screen_height - 50))
    screen.blit(text_surface, text_rect)

    observe_text = f"Sente:{observe_counts['black']}/5 Gote:{observe_counts['white']}/5"
    observe_surface = small_font.render(observe_text, True, BLACK)
    observe_rect = observe_surface.get_rect(center=(window_size // 2, screen_height - 20))
    screen.blit(observe_surface, observe_rect)

def display_winner(screen, winner, window_size):
    winner_text = f"{winner} wins!"
    text_surface = large_font.render(winner_text, True, BLACK)
    text_rect = text_surface.get_rect(center=(window_size // 2, window_size // 2))
    screen.blit(text_surface, text_rect)

def draw_log(screen, log, scroll_pos, window_size, log_width, board_size, cell_size):
    log_area = pygame.Rect(window_size, 0, log_width, window_size)
    pygame.draw.rect(screen, WHITE, log_area)
    max_lines = window_size // small_font.get_height()
    visible_log = log[scroll_pos:scroll_pos + max_lines]

    for i, entry in enumerate(visible_log):
        log_surface = small_font.render(entry, True, BLACK)
        screen.blit(log_surface, (window_size + 10, i * small_font.get_height()))

def draw_menu(screen, window_size, screen_height):
    screen.fill(GREEN)
    title_surface = large_font.render("Quantum Gomoku", True, BLACK)
    title_rect = title_surface.get_rect(center=(window_size // 2, window_size // 4))
    screen.blit(title_surface, title_rect)

    vs_cpu_button = pygame.Rect(window_size // 2 - 100, window_size // 2, 200, 50)
    vs_player_button = pygame.Rect(window_size // 2 - 100, window_size // 2 + 70, 200, 50)
    
    pygame.draw.rect(screen, WHITE, vs_cpu_button)
    pygame.draw.rect(screen, WHITE, vs_player_button)
    
    vs_cpu_text = font.render("VS CPU", True, BLACK)
    vs_player_text = font.render("VS Player", True, BLACK)
    
    vs_cpu_text_rect = vs_cpu_text.get_rect(center=vs_cpu_button.center)
    vs_player_text_rect = vs_player_text.get_rect(center=vs_player_button.center)
    
    screen.blit(vs_cpu_text, vs_cpu_text_rect)
    screen.blit(vs_player_text, vs_player_text_rect)
    
    return vs_cpu_button, vs_player_button

def draw_player_selection(screen, window_size, screen_height):
    screen.fill(GREEN)
    title_surface = large_font.render("Select Player", True, BLACK)
    title_rect = title_surface.get_rect(center=(window_size // 2, window_size // 4))
    screen.blit(title_surface, title_rect)

    sente_button = pygame.Rect(window_size // 2 - 100, window_size // 2, 200, 50)
    gote_button = pygame.Rect(window_size // 2 - 100, window_size // 2 + 70, 200, 50)
    
    pygame.draw.rect(screen, WHITE, sente_button)
    pygame.draw.rect(screen, WHITE, gote_button)
    
    sente_text = font.render("Sente", True, BLACK)
    gote_text = font.render("Gote", True, BLACK)
    
    sente_text_rect = sente_text.get_rect(center=sente_button.center)
    gote_text_rect = gote_text.get_rect(center=gote_button.center)
    
    screen.blit(sente_text, sente_text_rect)
    screen.blit(gote_text, gote_text_rect)
    
    return sente_button, gote_button

def draw_stone(screen, color, x, y, cell_size, text_color, probability):
    pygame.draw.circle(screen, color, (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), cell_size // 2 - 5)
    pygame.draw.circle(screen, BLACK if color in [WHITE, VERY_LIGHT_GRAY, LIGHT_GRAY] else WHITE, (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), cell_size // 2 - 5, 2)
    
    text_surface = pygame.font.Font(None, 24).render(f"{int(probability * 100)}", True, text_color)
    text_rect = text_surface.get_rect(center=(x * cell_size + cell_size // 2, y * cell_size + cell_size // 2))
    screen.blit(text_surface, text_rect)

def draw_thinking_message(screen, window_size, screen_height, message):
    text_surface = small_font.render(message, True, BLACK)
    text_rect = text_surface.get_rect(bottomright=(window_size - 10, screen_height - 10))
    screen.blit(text_surface, text_rect)

def observe_stone(probability):
    if random.random() < probability:
        return BLACK, WHITE
    else:
        return WHITE, BLACK
