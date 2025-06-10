# -*- coding: utf-8 -*-

import curses
import time
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from src.labs.lab5.local import Localiz
from src.labs.lab5.board import Board

#Размеры доски
BOARD_WIDTH = 11 
BOARD_HEIGHT = 20 

#Размеры окна игры
GAME_WINDOW_WIDTH = 2 * BOARD_WIDTH + 2
GAME_WINDOW_HEIGHT = BOARD_HEIGHT + 2

#Размеры окна помощи
HELP_WINDOW_WIDTH = 23
HELP_WINDOW_HEIGHT = 7

#Размеры статус окна
STATUS_WINDOW_HEIGHT = 12
STATUS_WINDOW_WIDTH = HELP_WINDOW_WIDTH

#Размеры окна выбора локализации игры
LANG_WINDOW_WIDTH = 18
LANG_WINDOW_HEIGHT = 6

#Размеры окна ошибки при выборе локализации игры
ERR_WINDOW_WIDTH = 29
ERR_WINDOW_HEIGHT = 4

#Размеры окна статистики
STATS_WINDOW_WIDTH = 40
STATS_WINDOW_HEIGHT = 22

#Размеры окна с таймером
TIMER_WIDTH = 16
TIMER_HEIGHT = 3

TITLE_HEIGHT = 6

LEFT_MARGIN = 3

TITLE_WIDTH = FOOTER_WIDTH = 50


def init_colors():
    #Инициализация цветов

    curses.init_pair(99, 8, curses.COLOR_BLACK)
    curses.init_pair(98, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(97, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(96, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(95, curses.COLOR_BLACK, curses.COLOR_WHITE)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, 13)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_MAGENTA)


def init_game_window():
    #Создание игрового окна

    window = curses.newwin(GAME_WINDOW_HEIGHT, GAME_WINDOW_WIDTH, TITLE_HEIGHT, LEFT_MARGIN)
    window.nodelay(True)
    window.keypad(1)

    return window

def init_status_window():
    #Создание окна статуса   

    window = curses.newwin(STATUS_WINDOW_HEIGHT, STATUS_WINDOW_WIDTH, TITLE_HEIGHT, GAME_WINDOW_WIDTH + 5)
    return window


def draw_game_window(window, GAME_OVER, PLAY_AGAIN, _PAUSE, game_board):
    #Отрисовка окна игры

    window.border()

    for a in range(BOARD_HEIGHT):
        for b in range(BOARD_WIDTH):
            if game_board.board[a][b] == 1:
                window.addstr(a + 1, 2 * b + 1, "  ", curses.color_pair(96))
            else:
                window.addstr(a + 1, 2 * b + 1, " .", curses.color_pair(99))

    for a in range(game_board.current_block.size()[0]):
        for b in range(game_board.current_block.size()[1]):
            if game_board.current_block.shape[a][b] == 1:
                x = 2 * game_board.current_block_pos[1] + 2 * b + 1
                y = game_board.current_block_pos[0] + a + 1
                window.addstr(y, x, "  ", curses.color_pair(game_board.current_block.color))

    if game_board.is_game_over():
        go_title = GAME_OVER
        ag_title = PLAY_AGAIN

        window.addstr(int(GAME_WINDOW_HEIGHT*.4), (GAME_WINDOW_WIDTH-len(go_title))//2, go_title, curses.color_pair(95))
        window.addstr(int(GAME_WINDOW_HEIGHT*.5), (GAME_WINDOW_WIDTH-len(ag_title))//2, ag_title, curses.color_pair(95))

    if pause:
        p_title = _PAUSE
        window.addstr(int(GAME_WINDOW_HEIGHT * .4), (GAME_WINDOW_WIDTH - len(p_title)) // 2, p_title,
                      curses.color_pair(95))

    window.refresh()


def draw_status_window(window, SCORE, LINES, LEVEL, BEST_SCORE, STATS, game_board):
    #Отисовка окна статуса

    if game_board.is_game_over():
        return

    for row in range(1, STATUS_WINDOW_HEIGHT - 1):
        window.addstr(row, 2, "".rjust(STATUS_WINDOW_WIDTH - 3, " "))

    window.border()

    window.addstr(1, 2, f"{SCORE}{game_board.score}")
    window.addstr(2, 2, f"{LINES}{game_board.lines}")
    window.addstr(3, 2, f"{LEVEL}{game_board.level}")
    window.addstr(4, 2, f"{BEST_SCORE}{game_board.best_score}")
    window.addstr(5, 2, f"{STATS}")

    start_col = int(STATUS_WINDOW_WIDTH / 2 - game_board.next_block.size()[1])

    for row in range(game_board.next_block.size()[0]):
        for col in range(game_board.next_block.size()[1]):
            if game_board.next_block.shape[row][col] == 1:
                window.addstr(7 + row, start_col + 2 * col, "  ", curses.color_pair(game_board.next_block.color))

    window.refresh()

def draw_lang_window():
    #Отрисовка окна с выбором локализации игры

    while True:
        window = curses.newwin(LANG_WINDOW_HEIGHT, LANG_WINDOW_WIDTH, TITLE_HEIGHT + 7, GAME_WINDOW_WIDTH - 7)
        
        try:
            window.border()
            
            window.addstr(1, 2, 'Select language')
            window.addstr(2, 2, '1. en')
            window.addstr(3, 2, '2. ru')
            window.addstr(4, 2, '3. do')
            window.addstr(2, 10, '4. fr')
            window.addstr(3, 10, '5. it')
            window.refresh()

            window.keypad(1)
            LANG = window.getch()
            if LANG == curses.KEY_RESIZE:
                curses.curs_set(0)
                draw_title()
                draw_footer()
                continue

            if LANG == ord('1'):
                LANG = 'en'
            elif LANG == ord('2'):
                LANG = 'ru'
            elif LANG == ord('3'):
                LANG = 'do'
            elif LANG == ord('4'):
                LANG = 'fr'
            elif LANG == ord('5'):
                LANG = 'it'
            else:
                raise ValueError('Incorrect input')

            _lang = Localiz(LANG)
            MOVE = _lang.MOVE
            DROP = _lang.DROP
            ROTATE = _lang.ROTATE
            PAUSE = _lang.PAUSE
            QUIT = _lang.QUIT
        
            SCORE = _lang.SCORE
            LINES = _lang.LINES
            LEVEL = _lang.LEVEL
            BEST_SCORE = _lang.BEST_SCORE
            STATS = _lang.STATS
            BLOCK_STATS = _lang.BLOCK_STATS
            CLEARED_LINES = _lang.CLEARED_LINES
            QUIT_STATS = _lang.QUIT_STATS
            NAME = _lang.NAME
            CONFIRM = _lang.CONFIRM
            GAME_OVER = _lang.GAME_OVER
            PLAY_AGAIN = _lang.PLAY_AGAIN
            _PAUSE = _lang._PAUSE

            window.clear()
            window.refresh()
            del window

            return MOVE, DROP, ROTATE, PAUSE, QUIT, SCORE, LINES, LEVEL, BEST_SCORE, STATS, BLOCK_STATS, CLEARED_LINES, QUIT_STATS, NAME, CONFIRM, GAME_OVER, PLAY_AGAIN, _PAUSE
    
        except ValueError as e:
            err_window = curses.newwin(ERR_WINDOW_HEIGHT, ERR_WINDOW_WIDTH, TITLE_HEIGHT + 13, GAME_WINDOW_WIDTH - 12)
            err_window.clear()
            err_window.border()

            err_window.addstr(1, 3, f'Error: {e}')
            err_window.addstr(2, 3, f'Press Enter to restart')
            err_window.refresh()

            bind = err_window.getch()
            if bind == curses.KEY_ENTER or bind == 10 or bind == 13:
                err_window.clear()
                err_window.refresh()
                del err_window
                continue
            else:
                err_window.clear()
                err_window.refresh()
                curses.endwin()
                exit()

def draw_stats_window(status_window, game_board, game_window, timer_window, SCORE, LINES, LEVEL, BEST_SCORE, STATS, BLOCK_STATS, CLEARED_LINES, QUIT_STATS, MOVE, DROP, ROTATE, PAUSE, QUIT, GAME_OVER, PLAY_AGAIN, _PAUSE):
    #Отрисовка окна статистики

    while True:
        window = curses.newwin(STATS_WINDOW_HEIGHT, STATS_WINDOW_WIDTH + 3, TITLE_HEIGHT + 1, LEFT_MARGIN + 3)
        window.border()
        window.keypad(1)

        window.addstr(1, 2, BEST_SCORE)
        top_scores = Board._get_top_scores()
        for idx, (score, name, date) in enumerate(top_scores):
            window.addstr(2 + idx, 2, f"{idx+1}. {name}: {score} {date}")

        blocks_stats = Board.read_block_stats()
        window.addstr(13, 2, BLOCK_STATS)
        for i, (block, count) in enumerate(blocks_stats.items()):
            window.addstr(14 + i, 4, f"{block}: {count}")

        global_stats = Board.read_global_stats()
        window.addstr(13, 22, f"{CLEARED_LINES}{global_stats['lines_cleared']}")

        window.addstr(STATS_WINDOW_HEIGHT-2, 2, QUIT_STATS)
        window.refresh()

        ch = window.getch()
        if ch == curses.KEY_RESIZE:
            curses.curs_set(0)
            draw_title()
            draw_footer()
            draw_status_window(status_window, SCORE, LINES, LEVEL, BEST_SCORE, STATS, game_board)
            draw_help_window(MOVE, DROP, ROTATE, PAUSE, QUIT)
            draw_game_window(game_window, GAME_OVER, PLAY_AGAIN, _PAUSE, game_board)
            draw_timer_window(timer_window, game_board.get_session_time())
            continue
        if ch == ord('q'):
            break

    window.clear()
    window.refresh()
    del window

def draw_help_window(MOVE, DROP, ROTATE, PAUSE, QUIT):
    #Отрисовка окна помощи

    window = curses.newwin(HELP_WINDOW_HEIGHT, HELP_WINDOW_WIDTH, TITLE_HEIGHT + STATUS_WINDOW_HEIGHT, GAME_WINDOW_WIDTH + 5)

    window.border()

    window.addstr(1, 2, MOVE)
    window.addstr(2, 2, DROP)
    window.addstr(3, 2, ROTATE)
    window.addstr(4, 2, PAUSE)
    window.addstr(5, 2, QUIT)

    window.refresh()

def draw_name_window(NAME, CONFIRM):
    #Отрисовка окна с вводом имени

    height, width = 5, 35
    y, x = TITLE_HEIGHT + 7, LEFT_MARGIN + 10
    name = ''
    while True:
        window = curses.newwin(height, width, y, x)
        window.border()
        window.addstr(1, 2, NAME)
        window.addstr(3, 2, CONFIRM)

        window.addstr(2, 2, "[" + name.ljust(20) + "]")
        window.move(2, 3 + len(name))
        window.refresh()
        window.keypad(1)
        curses.noecho()
        
        key = window.getch()
        if key == curses.KEY_RESIZE:
            curses.curs_set(0)
            draw_title()
            draw_footer()
            window.clear()
            window.refresh()
            del window
            continue

        elif key in (curses.KEY_ENTER, 10, 13):
            window.clear()
            window.refresh()
            del window
            break
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            name = name[:-1]
        elif 32 <= key <= 126 and len(name) < 20:
            name += chr(key)

        window.clear()
        window.refresh()
        del window

    return name[:6] if name else 'Player'

def draw_title():
    #Отрисовка надписи: TETRIS

    window = curses.newwin(TITLE_HEIGHT, TITLE_WIDTH, 1, LEFT_MARGIN)
    window.addstr(0, 4, "#####  ####  #####  ###    #   ####", curses.color_pair(98))
    window.addstr(1, 4, "  #    #       #    #  #      #", curses.color_pair(98))
    window.addstr(2, 4, "  #    ###     #    # #    #   ###", curses.color_pair(98))
    window.addstr(3, 4, "  #    #       #    #  #   #      #", curses.color_pair(98))
    window.addstr(4, 4, "  #    ####    #    #   #  #  ####", curses.color_pair(98))

    window.addstr(2, 0, " *", curses.color_pair(97))
    window.addstr(2, 41, " *", curses.color_pair(97))

    window.refresh()


def draw_footer():
    #Отрисовка надписи: Made with ❤

    title = "Made with"
    window = curses.newwin(1, FOOTER_WIDTH, TITLE_HEIGHT + GAME_WINDOW_HEIGHT + 1, LEFT_MARGIN)
    col_pos = int((GAME_WINDOW_WIDTH + STATUS_WINDOW_WIDTH - len(title) + 1) / 2)
    window.addstr(0, col_pos, title, curses.color_pair(98))
    window.addstr(0, col_pos + len(title) + 1, "❤", curses.color_pair(97))

    window.refresh()

def init_timer_window():
    #Создание окна для таймера

    window = curses.newwin(TIMER_HEIGHT, TIMER_WIDTH, TITLE_HEIGHT + 19, LEFT_MARGIN + GAME_WINDOW_WIDTH + 2)
    return window

def draw_timer_window(window, seconds):
    #Отрисовка окна таймера

    window.clear()
    window.border()
    mins = seconds // 60
    secs = seconds % 60
    window.addstr(1, 2, f'{mins:02}:{secs:02}')
    window.refresh()


def main():
    try:
        global pause
        pause = False  # Инициализируем переменную pause
        
        scr = curses.initscr()
        curses.beep()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(0)

        init_colors()

        draw_title()
        draw_footer()

        game_window = init_game_window()
        status_window = init_status_window()
        timer_window = init_timer_window()
        
        MOVE, DROP, ROTATE, PAUSE, QUIT, SCORE, LINES, LEVEL, BEST_SCORE, STATS, BLOCK_STATS, CLEARED_LINES, QUIT_STATS, NAME, CONFIRM, GAME_OVER, PLAY_AGAIN, _PAUSE = draw_lang_window()

        player_name = draw_name_window(NAME, CONFIRM)

        game_board = Board(BOARD_HEIGHT, BOARD_WIDTH, player_name)
        game_board.start()

        old_score = game_board.score

        draw_game_window(game_window, GAME_OVER, PLAY_AGAIN, _PAUSE, game_board)
        draw_status_window(status_window, SCORE, LINES, LEVEL, BEST_SCORE, STATS, game_board)

        draw_help_window(MOVE, DROP, ROTATE, PAUSE, QUIT)
        draw_timer_window(timer_window, game_board.get_session_time())

        start = time.time()

        quit_game = False
        while not quit_game:
            key_event = game_window.getch()

            #Перерисовка окон при изменении размера консоли
            if key_event == curses.KEY_RESIZE:
                curses.curs_set(0)
                draw_title()
                draw_footer()
                draw_status_window(status_window, SCORE, LINES, LEVEL, BEST_SCORE, STATS, game_board)
                draw_help_window(MOVE, DROP, ROTATE, PAUSE, QUIT)
                draw_game_window(game_window, GAME_OVER, PLAY_AGAIN, _PAUSE, game_board)
                draw_timer_window(timer_window, game_board.get_session_time())

            if key_event == ord("q"):
                quit_game = True

            if not game_board.is_game_over():
                if not pause:
                    if time.time() - start >= 1 / game_board.level:
                        game_board.move_block("down")
                        start = time.time()

                    if key_event == curses.KEY_UP:
                        game_board.rotate_block()
                    elif key_event == curses.KEY_DOWN:
                        game_board.move_block("down")
                    elif key_event == curses.KEY_LEFT:
                        game_board.move_block("left")
                    elif key_event == curses.KEY_RIGHT:
                        game_board.move_block("right")
                    elif key_event == ord(' '):
                        game_board.drop()
                    elif key_event == ord('s'):
                        #Строки для работы окна со статистикой
                        game_board.pause_start = time.time()
                        draw_stats_window(status_window, game_board, game_window, timer_window, SCORE, LINES, LEVEL, BEST_SCORE, STATS, BLOCK_STATS, CLEARED_LINES, QUIT_STATS, MOVE, DROP, ROTATE, PAUSE, QUIT, GAME_OVER, PLAY_AGAIN, _PAUSE)
                        
                        #Строки чтобы таймер "останавливался" в окне статистики
                        if game_board.pause_start is not None:
                            game_board.paused_time += time.time() - game_board.pause_start
                            game_board.pause_start = None

                        draw_status_window(status_window, SCORE, LINES, LEVEL, BEST_SCORE, STATS, game_board)
                        draw_help_window(MOVE, DROP, ROTATE, PAUSE, QUIT)
                        draw_game_window(game_window, GAME_OVER, PLAY_AGAIN, _PAUSE, game_board)
                        draw_timer_window(timer_window, game_board.get_session_time())

                if key_event == ord("p"):
                    pause = not pause
                    game_window.nodelay(not pause)
                    if pause:
                        game_board.pause_start = time.time()
                    else:
                        if game_board.pause_start is not None:
                            game_board.paused_time += time.time() - game_board.pause_start
                            game_board.pause_start = None
            else:
                curses.beep()
                game_window.nodelay(False)
                if key_event == ord("\n"):
                    game_board.start()
                    game_window.nodelay(True)

            draw_game_window(game_window, GAME_OVER, PLAY_AGAIN, _PAUSE, game_board)
            draw_timer_window(timer_window, game_board.get_session_time())

            if old_score != game_board.score:
                draw_status_window(status_window, SCORE, LINES, LEVEL, BEST_SCORE, STATS, game_board)
                old_score = game_board.score
    finally:
        curses.endwin()

if __name__ == '__main__':
    main()