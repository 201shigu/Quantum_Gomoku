import pygame
import random
from classes import Stone, CPU
from draw_utils import draw_board, draw_buttons, display_winner, draw_log, draw_thinking_message
from settings import BLACK, WHITE, LIGHT_GRAY, OBSERVE_LIMIT

class Game:
    def __init__(self, screen, window_size, screen_height, log_width, board_size, cell_size):
        self.screen = screen
        self.window_size = window_size
        self.screen_height = screen_height
        self.log_width = log_width
        self.cell_size = cell_size
        self.board_size = board_size
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = "black"
        self.turn_count = 0
        self.observed = False
        self.winner = None
        self.log = []
        self.scroll_pos = 0
        self.player_side = "sente"
        self.cpu_side = "gote"
        self.cpu = CPU(self.board, self.board_size)
        self.last_move = None
        self.cpu_thinking = False
        self.vs_cpu_mode = False  # モードのフラグを追加
        self.observe_counts = {"black": OBSERVE_LIMIT, "white": OBSERVE_LIMIT}
        self.observe_mode = False
        self.observer = None

    def set_player(self, player_side, vs_cpu):
        self.player_side = player_side
        self.cpu_side = "gote" if player_side == "sente" else "sente"
        self.vs_cpu_mode = vs_cpu  # モードを設定
        pygame.display.set_mode((self.window_size + self.log_width, self.screen_height))  # ゲーム画面に遷移する際にログ用スペースを確保

    def handle_mouse_click(self, x, y):
        if self.window_size // 2 - 75 <= x <= self.window_size // 2 + 75 and self.screen_height - 70 <= y <= self.screen_height - 30:
            if self.winner is not None:
                self.reset_game()
            elif self.observe_mode:
                self.observe_mode = False
            elif self.observed:
                self.reset_observations()
                self.observed = False
            elif self.observe_counts[self.current_player] > 0:
                self.observe_mode = True
                self.observer = self.current_player
            else:
                draw_thinking_message(self.screen, self.window_size, self.screen_height, "Can't Observe")
                pygame.display.flip()
                pygame.time.wait(1000)
        elif not self.observed and self.winner is None and (not self.vs_cpu_mode or self.current_player == ("black" if self.player_side == "sente" else "white")):
            grid_x, grid_y = x // self.cell_size, y // self.cell_size
            print(f"Placing stone at grid ({grid_x}, {grid_y})")  # デバッグ用
            if 0 <= grid_x < self.board_size and 0 <= grid_y < self.board_size and self.board[grid_x][grid_y] is None:
                self.place_stone(grid_x, grid_y)
                if self.observe_mode:
                    self.log.append(f"{self.observer.capitalize()}: Observe")
                    self.observe_counts[self.observer] -= 1
                    self.observe_mode = False
                    self.show_observing_message()
                    self.observed = True
                else:
                    if self.vs_cpu_mode:
                        self.cpu_thinking = True
        self.check_draw()

    def check_draw(self):
        if self.observe_counts["black"] == 0 and self.observe_counts["white"] == 0 and self.winner is None:
            self.winner = "Draw"

    def handle_scroll(self, scroll_amount):
        self.scroll_pos = max(0, min(self.scroll_pos - scroll_amount, len(self.log) - 1))

    def place_stone(self, grid_x, grid_y):
        self.turn_count += 1
        remainder = self.turn_count % 4
        if remainder == 1:
            probability = 0.9
        elif remainder == 2:
            probability = 0.1
        elif remainder == 3:
            probability = 0.7
        elif remainder == 0:
            probability = 0.3
        print(f"Stone placed with probability {probability}")  # デバッグ用
        self.board[grid_x][grid_y] = Stone(grid_x, grid_y, probability, self.current_player)
        self.last_move = (grid_x, grid_y)
        self.log.append(f"{self.current_player.capitalize()} {self.turn_count}: ({grid_x + 1},{grid_y + 1})")
        self.current_player = "white" if self.current_player == "black" else "black"

    def observe_board(self):
        for row in self.board:
            for stone in row:
                if stone is not None and not stone.observed:
                    stone.observe()

    def reset_observations(self):
        for row in self.board:
            for stone in row:
                if stone is not None and stone.observed:
                    stone.reset()

    def check_winner(self):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        black_win = False
        white_win = False

        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] is not None and self.board[x][y].observed:
                    stone = self.board[x][y]
                    for direction in directions:
                        count = 1
                        for i in range(1, 5):
                            nx, ny = x + direction[0] * i, y + direction[1] * i
                            if 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[nx][ny] is not None and self.board[nx][ny].observed:
                                next_stone = self.board[nx][ny]
                                if next_stone.color == stone.color:
                                    count += 1
                                else:
                                    break
                            else:
                                break
                        if count >= 5:
                            if stone.color == BLACK:
                                black_win = True
                            else:
                                white_win = True

        if black_win and white_win:
            return self.observer
        elif black_win:
            return "black"
        elif white_win:
            return "white"
        return None

    def reset_game(self):
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = "black"
        self.turn_count = 0
        self.observed = False
        self.winner = None
        self.log = []
        self.last_move = None
        self.cpu_thinking = False
        self.observe_counts = {"black": OBSERVE_LIMIT, "white": OBSERVE_LIMIT}
        self.observe_mode = False
        self.observer = None

    def show_observing_message(self):
        draw_thinking_message(self.screen, self.window_size, self.screen_height, "Observing...")
        pygame.display.flip()
        pygame.time.wait(1000)
        self.observe_board()
        self.winner = self.check_winner()
        self.observed = True

    def update(self, cpu_mode=False):
        draw_board(self.screen, self.window_size, self.cell_size, self.board_size, self.last_move)
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] is not None:
                    self.board[x][y].draw(self.screen, self.cell_size)
        draw_buttons(self.screen, self.window_size, self.screen_height, self.observed, self.winner, self.observe_counts, self.observe_mode)
        if self.winner:
            display_winner(self.screen, self.winner, self.window_size)
        draw_log(self.screen, self.log, self.scroll_pos, self.window_size, self.log_width, self.board_size, self.cell_size)

        if cpu_mode and self.current_player == ("black" if self.cpu_side == "sente" else "white") and not self.observed and self.winner is None:
            if self.cpu_thinking:
                draw_thinking_message(self.screen, self.window_size, self.screen_height, "CPU is thinking...")
                pygame.display.flip()
                pygame.time.wait(1000)
                self.cpu_thinking = False
            self.cpu.cpu_turn(self.place_stone)
