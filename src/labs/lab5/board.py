# -*- coding: utf-8 -*-

import math
import random
import json
import os
import time
from datetime import datetime

# Получаем путь к директории текущего файла
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

#Файл для хранения лучших результатов
BEST_SCORE_FILE_NAME = os.path.join(CURRENT_DIR, "best_score.txt")

#Файл для хранения статистики блоков
BLOCK_STATS_FILE = os.path.join(CURRENT_DIR, "block_stats.json")

#Файл для хранения статистики всех сломанных линий
GLOBAL_STATS_FILE = os.path.join(CURRENT_DIR, "global_stats.json")

block_shapes = [
    # T Block
    [[0, 1, 0],
     [1, 1, 1]],

    # L Block
    [[1, 0],
     [1, 0],
     [1, 1]],

    # J Block
    [[0, 1],
     [0, 1],
     [1, 1]],

    # S Block
    [[0, 1, 1],
     [1, 1, 0]],

    # Z Block
    [[1, 1, 0],
     [0, 1, 1]],

    # O Block
    [[1, 1],
     [1, 1]],

    # I Block
    [[1], [1], [1], [1]]
]


class Board:
    def __init__(self, height, width, player_name='Player'):
        self.height = height
        self.width = width
        self.board = self._get_new_board()

        self.current_block_pos = None
        self.current_block = None
        self.next_block = None
        self.player_name = player_name

        self.game_over = False
        self.score = None
        self.lines = None
        self.best_score = None
        self.level = None

        #self для работы с таймером
        self.start_time = None
        self.paused_time = 0
        self.pause_start = None

    def start(self):
        #Начало игры

        self.board = self._get_new_board()

        self.current_block_pos = None
        self.current_block = None
        self.next_block = None

        self.game_over = False
        self.score = 0
        self.lines = 0
        self.level = 1
        self.best_score = self._read_best_score()

        #self для работы с таймером
        self.start_time = time.time()
        self.paused_time = 0
        self.pause_start = None

        self._place_new_block()

    def is_game_over(self):
        #Конец игры

        return self.game_over

    def get_session_time(self):
        #Получение времени сеанса

        if self.start_time is None:
            return 0
        paused = self.paused_time
        if self.pause_start is not None:
            paused += time.time() - self.pause_start
        return int(time.time() - self.start_time - paused)

    def rotate_block(self):
        #Поворот блока

        rotated_shape = list(map(list, zip(*self.current_block.shape[::-1])))

        if self._can_move(self.current_block_pos, rotated_shape):
            self.current_block.shape = rotated_shape

    def move_block(self, direction):
        #Попытка переместить блок

        pos = self.current_block_pos
        if direction == "left":
            new_pos = [pos[0], pos[1] - 1]
        elif direction == "right":
            new_pos = [pos[0], pos[1] + 1]
        elif direction == "down":
            new_pos = [pos[0] + 1, pos[1]]
        else:
            raise ValueError("wrong directions")

        if self._can_move(new_pos, self.current_block.shape):
            self.current_block_pos = new_pos
        elif direction == "down":
            self._land_block()
            self._burn()
            self._place_new_block()

    def drop(self):
        #Опустить блок на самый низ

        i = 1
        while self._can_move((self.current_block_pos[0] + 1, self.current_block_pos[1]), self.current_block.shape):
            i += 1
            self.move_block("down")

        self._land_block()
        self._burn()
        self._place_new_block()

    def _get_new_board(self):
        #Создание пустой доски

        return [[0 for _ in range(self.width)] for _ in range(self.height)]

    def _place_new_block(self):
        #Размещение блока и генерация следующего

        if self.next_block is None:
            self.current_block = self._get_new_block()
            self.next_block = self._get_new_block()
        else:
            self.current_block = self.next_block
            self.next_block = self._get_new_block()

        #Типы блоков и их номера
        block_type_m = {0: "T", 1: "L", 2: "J", 3: "S", 4: "Z", 5: "O", 6: "I"}
        if self.current_block is not None:
            stats = Board.read_block_stats()
            block_letter = block_type_m.get(self.current_block.block_type, None)
            if block_letter is not None:
                stats[block_letter] += 1
                Board.save_block_stats(stats)

        size = Block.get_size(self.current_block.shape)
        col_pos = math.floor((self.width - size[1]) / 2)
        self.current_block_pos = [0, col_pos]

        if self._check_overlapping(self.current_block_pos, self.current_block.shape):
            self.game_over = True
            self._save_best_score(self.player_name)
        else:
            self.score += 5

    def _land_block(self):
        #Размещение блока на доску и создание нового блока

        size = Block.get_size(self.current_block.shape)
        for row in range(size[0]):
            for col in range(size[1]):
                if self.current_block.shape[row][col] == 1:
                    self.board[self.current_block_pos[0] + row][self.current_block_pos[1] + col] = 1

    def _burn(self):
        #Удаление заполненных линий

        for row in range(self.height):
            if all(col != 0 for col in self.board[row]):
                for r in range(row, 0, -1):
                    self.board[r] = self.board[r - 1]
                self.board[0] = [0 for _ in range(self.width)]
                self.score += 100
                self.lines += 1
                stats = Board.read_global_stats()
                stats["lines_cleared"] += 1
                Board.save_global_stats(stats)
                if self.lines % 10 == 0:
                    self.level += 1

    def _check_overlapping(self, pos, shape):
        #Проверка перекрывания блоков

        size = Block.get_size(shape)
        for row in range(size[0]):
            for col in range(size[1]):
                if shape[row][col] == 1:
                    if self.board[pos[0] + row][pos[1] + col] == 1:
                        return True
        return False

    def _can_move(self, pos, shape):
        #Проверка возможности перемещения блока

        size = Block.get_size(shape)
        if pos[1] < 0 or pos[1] + size[1] > self.width \
                or pos[0] + size[0] > self.height:
            return False

        return not self._check_overlapping(pos, shape)

    def _save_best_score(self, player_name):
        #Сохранение 10 лучших результатов в файле "best_score.txt"

        scores = []
        if os.path.exists(BEST_SCORE_FILE_NAME):
            with open(BEST_SCORE_FILE_NAME, 'r') as file:
                for line in file:
                    parts = line.strip().split(' | ')
                    if len(parts) == 3:
                        try:
                            score = int(parts[0])
                            name = parts[1]
                            date = parts[2]
                            scores.append((score, name, date))
                        except ValueError:
                            continue

        now = datetime.now().strftime('(%d-%m-%Y %H:%M:%S)')
        scores.append((self.score, player_name, now))
        scores = sorted(scores, key=lambda x: x[0], reverse=True)[:10]

        with open(BEST_SCORE_FILE_NAME, 'w') as file:
            for score, name, date in scores:
                file.write(f'{score} | {name} | {date}\n')

    @staticmethod
    def _read_best_score():
        #Чтение лучших результатов из файла "best_score.txt"

        if os.path.exists(BEST_SCORE_FILE_NAME):
            best = 0
            with open(BEST_SCORE_FILE_NAME) as file:
                for line in file:
                    parts = line.strip().split(' | ')
                    if len(parts) == 3:
                        try:
                            score = int(parts[0])
                            if score > best:
                                best = score
                        except ValueError:
                            continue
            return best
        return 0

    @staticmethod
    def save_block_stats(stats):
        #Сохранение статистики блоков в файл "block_stats.json"
        with open(BLOCK_STATS_FILE, 'w') as f:
            json.dump(stats, f)

    @staticmethod
    def read_block_stats():
        #Чтение статистики блоков из файла "block_stats.json"

        if os.path.exists(BLOCK_STATS_FILE):
            try:
                with open(BLOCK_STATS_FILE, 'r') as f:
                    data = json.load(f)
                    if not data:
                        return {"T": 0, "L": 0, "J": 0, "S": 0, "Z": 0, "O": 0, "I": 0}
                    return data
            except Exception:
                return {"T": 0, "L": 0, "J": 0, "S": 0, "Z": 0, "O": 0, "I": 0}
        return {"T": 0, "L": 0, "J": 0, "S": 0, "Z": 0, "O": 0, "I": 0}

    @staticmethod
    def save_global_stats(stats):
        #Сохранение статистики всех сломанных линий в файл "global_stats.json"
        with open(GLOBAL_STATS_FILE, 'w') as f:
            json.dump(stats, f)

    @staticmethod
    def read_global_stats():
        #Чтение статистики всех сломанных линий из файла "global_stats.json"
        if os.path.exists(GLOBAL_STATS_FILE):
            try:
                with open(GLOBAL_STATS_FILE, 'r') as f:
                    data = json.load(f)
                    if not data or "lines_cleared" not in data:
                        return {"lines_cleared": 0}
                    return data
            except Exception:
                return {"lines_cleared": 0}
        return {"lines_cleared": 0}

    

    @staticmethod
    def _get_top_scores():
        #Получение топа из 10 лучших результатов из файла "best_score.txt"

        scores = []
        if os.path.exists(BEST_SCORE_FILE_NAME):
            with open(BEST_SCORE_FILE_NAME) as file:
                for line in file:
                    parts = line.strip().split(' | ')
                    if len(parts) == 3:
                        try:
                            score = int(parts[0])
                            name = parts[1]
                            date = parts[2]
                            scores.append((score, name, date))
                        except ValueError:
                            continue
        return scores[:10]

    @staticmethod
    def _get_new_block():
        #Получение рандомного блока

        block = Block(random.randint(0, len(block_shapes) - 1))

        if random.getrandbits(1):
            block.flip()

        return block


class Block:
    def __init__(self, block_type):
        self.shape = block_shapes[block_type]
        self.color = block_type + 1
        self.block_type = block_type

    def flip(self):
        self.shape = list(map(list, self.shape[::-1]))

    def _get_rotated(self):
        return list(map(list, zip(*self.shape[::-1])))

    def size(self):
        return self.get_size(self.shape)

    @staticmethod
    def get_size(shape):
        return [len(shape), len(shape[0])]
