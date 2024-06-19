import pygame
from game import Game
from draw_utils import draw_menu, draw_player_selection

# 初期化
pygame.init()

# ボード設定
CELL_SIZE = 50
BOARD_SIZE = 16
WINDOW_SIZE = CELL_SIZE * BOARD_SIZE
SCREEN_HEIGHT = WINDOW_SIZE + 100
LOG_WIDTH = 300

screen = pygame.display.set_mode((WINDOW_SIZE, SCREEN_HEIGHT))  # 初期の画面サイズ
pygame.display.set_caption("Quantum_Gomoku")

# ゲームのインスタンスを作成
game = Game(screen, WINDOW_SIZE, SCREEN_HEIGHT, LOG_WIDTH, BOARD_SIZE, CELL_SIZE)

running = True
game_started = False
cpu_mode = False
player_selection = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if game_started:
                print(f"Mouse click at ({x}, {y})")  # デバッグ用
                game.handle_mouse_click(x, y)
            elif player_selection:
                sente_button, gote_button = draw_player_selection(screen, WINDOW_SIZE, SCREEN_HEIGHT)
                if sente_button.collidepoint(x, y):
                    game.set_player("sente")
                    game_started = True
                elif gote_button.collidepoint(x, y):
                    game.set_player("gote")
                    game_started = True
            else:
                vs_cpu_button, vs_player_button = draw_menu(screen, WINDOW_SIZE, SCREEN_HEIGHT)
                if vs_cpu_button.collidepoint(x, y):
                    cpu_mode = True
                    player_selection = True
                elif vs_player_button.collidepoint(x, y):
                    game_started = True
                    screen = pygame.display.set_mode((WINDOW_SIZE + LOG_WIDTH, SCREEN_HEIGHT))  # ゲーム画面に遷移する際にログ用スペースを確保

        elif event.type == pygame.MOUSEWHEEL:
            if game_started:
                game.handle_scroll(event.y)

    if game_started:
        game.update(cpu_mode)
    elif player_selection:
        draw_player_selection(screen, WINDOW_SIZE, SCREEN_HEIGHT)
    else:
        draw_menu(screen, WINDOW_SIZE, SCREEN_HEIGHT)

    pygame.display.flip()

pygame.quit()
