from __future__ import annotations

import random
import sys
import re

import pygame

from game_config import *


current_level = None
current_sequence = None


def find_color(color):
    if(color == 'red'):
        return 9
    if(color == 'blue'):
        return 3
    if(color == 'green'):
        return 2
    if(color == 'orange'):
        return 1
    if(color == 'dark-blue'):
        return 10
    if(color == 'yellow'):
        return 11
    if(color == 'dark-green'):
        return 5
    if(color == 'purple'):
        return 7

    # else:
    #     rgb = []
    #     for i in (0, 2, 4):
    #         decimal = int(hex[i:i+2], 16)
    #         rgb.append(decimal)
    #     return tuple(rgb)


cur_level = 0
cur_rep = 0
cur_sequence = 0
piece = None

GAME_LIST = []
game_index_to_key = {}


def select_piece():
    global cur_rep, cur_sequence, piece, cur_level
    while(cur_level < len(GAME_LIST)):
        print(f"New Iteration, level is: {cur_level}")
        while(cur_sequence < len(GAME_LIST[cur_level])):
            sequence_rep_pair = GAME_LIST[cur_level][cur_sequence]
            sequence_name, rep = sequence_rep_pair[0], sequence_rep_pair[1]
            sequence = SEQUENCES[game_index_to_key[cur_level]][sequence_name]

            while(cur_rep < rep):
                try:
                    if piece is not None:
                        yield piece

                finally:
                    piece_name = random.choice(sequence)
                    piece = SHAPES[game_index_to_key[cur_level]][piece_name]
                    color = GLOBAL_COLORS[game_index_to_key[cur_level]][piece_name]
                    color = color[1:]
                    color = color[0:-1]
                    color = find_color(color)

                    for i in range(len(piece)):
                        for j in range(len(piece[i])):
                            if(piece[i][j] == 1):
                                piece[i][j] = color

                    cur_rep += 1
                    if(cur_rep >= rep):
                        cur_rep = 0
                        break
                    print(cur_rep, rep)

            cur_sequence += 1
            if(cur_sequence >= len(GAME_LIST[cur_level])):
                cur_sequence = 0
                break

        print("Change Level")
        cur_level += 1
        if(cur_level >= len(GAME_LIST)):
            cur_level = len(GAME_LIST) - 1
            cur_sequence = 0
            cur_rep = 0
        print(f"DONE {cur_level}")


class Tetrimino():
    def __init__(self, board: Board, shape: list[list[int]]) -> None:
        self.board = board
        self.shape = shape
        self.x = int(board.cols / 2 - len(self.shape[0])/2)
        self.y = 0

    def check_collision(self):
        for cy, row in enumerate(self.shape):
            for cx, cell in enumerate(row):
                try:
                    if cell and self.board[self.y + cy][self.x + cx]:
                        return True
                except IndexError:
                    return True
        return False

    def rotate_clockwise(self):
        self.shape = [[self.shape[y][x] for y in range(len(self.shape))]
                      for x in range(len(self.shape[0]) - 1, -1, -1)]

    def rotate(self):
        old_shape = self.shape  # To check
        self.rotate_clockwise()
        if self.check_collision():
            self.shape = old_shape

    def __getitem__(self, index: int):
        return self.shape[index]


class Board():
    def __init__(self, rows: int, cols: int) -> None:
        self.cols = cols
        self.rows = rows

        self.next_shape = next(select_piece())
        self.gameboard = [[0 for _ in range(self.cols)]
                          for _ in range(self.rows)]

    def new_tetrimino(self) -> None:
        result = Tetrimino(self, self.next_shape)
        self.next_shape = next(select_piece())
        if result.check_collision():
            Tetris.gameover = True
        self.curr_tetrimino = result

    def fuse_tetrimino(self, tetrimino: Tetrimino) -> None:
        off_x, off_y = tetrimino.x, tetrimino.y
        for cy, row in enumerate(tetrimino):
            for cx, val in enumerate(row):
                self.gameboard[cy + off_y - 1][cx + off_x] += val

    def remove_row(self, row: int):
        del self.gameboard[row]
        self.gameboard = [[0 for _ in range(self.cols)]] + self.gameboard

    def __getitem__(self, index: int):
        return self.gameboard[index]


class Tetris:
    gameover = False
    paused = False

    def __init__(self, rows: int, cols: int, cell_size: int = 30) -> None:
        pygame.init()
        pygame.key.set_repeat(250, 25)

        self.cell_size: int = cell_size
        self.width = cell_size * (cols+8)
        self.height = cell_size * rows
        self.rlim = cell_size * cols
        self.rows = rows
        self.cols = cols

        self.background_grid = [
            [-1 if (x % 2) == (y % 2) else 0 for x in range(cols)] for y in range(rows)]

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.default_font = pygame.font.Font(
            pygame.font.get_default_font(), 18)
        # block mouse movement events
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.init_game()

    def init_game(self) -> None:
        self.board: Board = Board(self.rows, self.cols)
        self.board.new_tetrimino()
        self.level: int = 1
        self.score: int = 0
        self.lines: int = 0
        speed = 1000 - LVL_SPEED_MOD[self.level-1]
        # 1000 ms is the time for each step the shape takes
        pygame.time.set_timer(pygame.USEREVENT+1, speed if speed > 25 else 25)

    def draw_matrix(self, matrix, offset):
        off_x, off_y = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    rect = ((off_x+x) * self.cell_size, (off_y+y) * self.cell_size,
                            self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, COLORS[val], rect, 0)
                    # if val != -1:
                    #     pygame.draw.rect(self.screen, WHITE, rect, 1)

    def draw(self) -> None:
        pygame.draw.line(self.screen, WHITE, (self.rlim + 1, 0),
                         (self.rlim + 1, self.height - 1))
        self.disp_msg("Next Shape:", (self.rlim + self.cell_size, 10))
        self.disp_msg(f"Score: {self.score}\n\nLevel: {self.level}\nLines: {self.lines}",
                      (self.rlim + self.cell_size, self.cell_size*10 if self.rows > 12 else self.cell_size*5))
        self.draw_matrix(self.background_grid, (0, 0))
        self.draw_matrix(self.board, (0, 0))
        tetrimino = self.board.curr_tetrimino
        self.draw_matrix(tetrimino.shape, (tetrimino.x, tetrimino.y))
        self.draw_matrix(self.board.next_shape, (self.board.cols + 1, 2))

    def disp_msg(self, msg, topleft):
        x, y = topleft
        for line in msg.splitlines():
            msg_img = self.default_font.render(line, True, WHITE, BLACK)
            self.screen.blit(msg_img, (x, y))
            y += 20

    def centre_msg(self, msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image = self.default_font.render(line, True, WHITE, BLACK)

            msg_im_centre_x, msg_im_centre_y = msg_image.get_size()
            msg_x = (self.width - msg_im_centre_x) // 2
            msg_y = (self.height - msg_im_centre_y) // 2 + i*20

            self.screen.blit(msg_image, (msg_x, msg_y))

    def update_stats(self, n: int):
        self.lines += n
        self.score += LINE_SCORES[n] * self.level

        if self.lines >= self.level*6:
            self.level += 1

            newdelay = 1000 - LVL_SPEED_MOD[self.level-1]
            newdelay = 25 if newdelay < 25 else newdelay

            pygame.time.set_timer(pygame.USEREVENT+1, newdelay)

    def move(self, delta_x):

        if not Tetris.gameover and not Tetris.paused:
            tetrimino = self.board.curr_tetrimino
            old_x = tetrimino.x
            new_x = tetrimino.x + delta_x
            new_x = 0 if new_x < 0 else new_x

            if new_x > self.board.cols - len(tetrimino[0]):
                new_x = self.board.cols - len(tetrimino[0])

            tetrimino.x = new_x

            if tetrimino.check_collision():
                tetrimino.x = old_x

    def drop(self, manual: bool) -> bool:

        if not Tetris.gameover and not Tetris.paused:
            tetrimino = self.board.curr_tetrimino

            self.score += 1 if manual else 0
            tetrimino.y += 1

            if tetrimino.check_collision():
                self.board.fuse_tetrimino(tetrimino)
                self.board.new_tetrimino()

                cleared_rows = 0

                while True:
                    for i, row in enumerate(self.board):
                        if 0 not in row:
                            self.board.remove_row(i)
                            cleared_rows += 1
                            break
                    else:
                        break

                self.update_stats(cleared_rows)

                return True

        return False

    def instant_drop(self) -> None:
        if not Tetris.gameover and not Tetris.paused:
            while True:
                if self.drop(manual=True):
                    return

    def rotate_tetrimino(self) -> None:
        if not Tetris.gameover and not Tetris.paused:
            self.board.curr_tetrimino.rotate()

    def start_game(self):
        if Tetris.gameover:
            self.init_game()
            Tetris.gameover = False

    def toggle_pause(self):
        Tetris.paused = not Tetris.paused

    def run(self):

        Tetris.gameover = False
        Tetris.paused = False

        Clock = pygame.time.Clock()
        pygame.mixer.music.load("tetris_theme.mp3")
        pygame.mixer.music.play(-1)
        while True:
            Clock.tick(FPS)

            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.USEREVENT+1:
                    self.drop(manual=False)
                elif event.type == pygame.KEYDOWN:
                    if(event.key == pygame.K_ESCAPE):
                        self.quit()
                    if(event.key == pygame.K_LEFT):
                        self.move(-1)
                    if(event.key == pygame.K_RIGHT):
                        self.move(+1)
                    if(event.key == pygame.K_DOWN):
                        self.drop(manual=True)
                    if(event.key == pygame.K_UP):
                        self.rotate_tetrimino()
                    if(event.key == pygame.K_p):
                        self.toggle_pause()
                    if(event.key == pygame.K_SPACE):
                        self.start_game()
                    if(event.key == pygame.K_RETURN):
                        self.instant_drop()

            if Tetris.gameover:
                self.centre_msg(
                    f"Game Over!\nYour score: {self.score}.\nPress space to continue")
            else:
                if Tetris.paused:
                    self.centre_msg("Paused")
                else:
                    self.draw()

            pygame.display.update()

    def quit(self) -> None:
        self.centre_msg("Exiting...")
        pygame.display.update()
        sys.exit()


def playgamenow():
    global current_level, current_sequence

    global GAME_LIST
    global game_index_to_key

    j = 0
    for key in GAME:
        game_index_to_key[j] = key
        GAME_LIST.append(GAME[key])
        print(GAME_LIST)
        j += 1

    res = 18
    if(BOARD_HEIGHT < 30 and BOARD_WIDTH < 30):
        res = 30
    if(BOARD_HEIGHT >= 50):
        res = 15

    App = Tetris(BOARD_HEIGHT, BOARD_WIDTH, res)
    App.run()
