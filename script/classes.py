import pygame
import random
import time
from draw_utils import get_color_and_text, draw_stone, observe_stone

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
        self.color, self.text_color = observe_stone(self.probability)
        self.observed = True

    def reset(self):
        self.color = self.original_color
        self.observed = False
        self.color, self.text_color = get_color_and_text(self.player, self.probability)

    def draw(self, screen, cell_size):
        draw_stone(screen, self.color, self.x, self.y, cell_size, self.text_color, self.probability)

class CPU:
    def __init__(self, board, board_size):
        self.board = board
        self.board_size = board_size

    def cpu_turn(self, place_stone_callback):
        best_moves = self.find_best_moves()
        if best_moves:
            move = random.choice(best_moves)
            print(f"CPU placing stone at ({move[0]}, {move[1]})")  # デバッグ用
            place_stone_callback(move[0], move[1])

    def find_best_moves(self):
        best_moves = []
        center = self.board_size // 2
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] is None:
                    # 中央に近い位置を優先
                    if abs(x - center) <= 2 and abs(y - center) <= 2:
                        best_moves.append((x, y))
        return best_moves
