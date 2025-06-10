# -*- coding: utf-8 -*-

import curses

from .calc import CalculateFunc
from .chart import DrawChart, DrawDoubleChart

# Размеры окна выбора метода построения графика
MAIN_WINDOW_WIDTH = 45
MAIN_WINDOW_HEIGHT = 8

# Размеры окна выбора функции
FUNCT_WINDOW_WIDTH = 29
FUNCT_WINDOW_HEIGHT = 10

# Размеры окна ввод параметров (A, B) для функции
CHOICE_VALUES_WINDOW_WIDTH = 30
CHOICE_VALUES_WINDOW_HEIGHT = 8

# Размеры окна ввода параметров (x1, x2, step) для функции
CHOICE_x1x2_WINDOW_WINDT = 40
CHOICE_x1x2_WINDOW_HEIGHT = 9

# Размеры окна ввода параметров 
X1X2Y1Y2_WINDOW_WIDTH = 35
X1X2Y1Y2_WINDOW_HEIGHT = 10

# Размеры окна отображения ошибки
ERR_WINDOW_WIDTH = 29
ERR_WINDOW_HEIGHT = 4

HEIGHT_MARGIN = 10

LEFT_MARGIN = 35

def err_window(window, e, h=0):
    # Создание окна для отображения ошибки выбора

    while True:
        err_window = curses.newwin(ERR_WINDOW_HEIGHT, ERR_WINDOW_WIDTH, HEIGHT_MARGIN + h, LEFT_MARGIN)
        curses.curs_set(0)
        err_window.keypad(1)

        err_window.clear()
        err_window.border()

        err_window.addstr(1, 2, f'Ошибка: {e}')
        err_window.addstr(2, 2, f'Enter - Попробовать снова')

        err_key = err_window.getch()
        if err_key in (curses.KEY_ENTER, 10, 13):
            err_window.clear()
            err_window.refresh()
            del err_window
            del window
            break

        elif err_key == curses.KEY_RESIZE:
            window.border()
            window.refresh()
            continue

def method_choice():
    # Выбор метода построения графика/графиков

    while True:
        try:
            window = curses.newwin(MAIN_WINDOW_HEIGHT, MAIN_WINDOW_WIDTH, HEIGHT_MARGIN, LEFT_MARGIN)
            curses.curs_set(0)
            window.keypad(1)

            window.clear()
            window.border()

            window.addstr(1, 2, 'Выберите метод')
            window.addstr(3, 2, '1. Построить график функции')
            window.addstr(5, 2, '2. Найти точку пересечения двух графиков')

            key = window.getch()

            if key == curses.KEY_RESIZE:
                continue

            elif key == ord('1'):
                choice = 1
            elif key == ord('2'):
                choice = 2
            else:
                raise ValueError('Некорректный ввод')

            return choice
        
        # Вызов окна ошибки
        except ValueError as e:
            err_window(window, e, 8)
            continue

        finally:
            window.clear()
            window.refresh()
            del window


def draw_func_window():
    # Выбор функции для отрисовки графика

    while True:
        try:
            window = curses.newwin(FUNCT_WINDOW_HEIGHT, FUNCT_WINDOW_WIDTH, HEIGHT_MARGIN, LEFT_MARGIN)
            curses.curs_set(0)
            window.keypad(1)

            window.clear()
            window.border()

            window.addstr(1, 2, f'Выберите функцию')
            window.addstr(3, 2, f'1. sin(x)')
            window.addstr(4, 2, f'2. cos(x)')
            window.addstr(5, 2, f'3. exp(x)')
            window.addstr(6, 2, f'4. x^2')
            window.addstr(7, 2, f'5. ln(x)')

            choice = window.getch()

            if choice == curses.KEY_RESIZE:
                continue

            elif choice == ord('1'):
                choice = 'sin(x)'
            elif choice == ord('2'):
                choice = 'cos(x)'
            elif choice == ord('3'):
                choice = 'exp(x)'
            elif choice == ord('4'):
                choice = 'x^2'
            elif choice == ord('5'):
                choice = 'ln(x)'
            else:
                raise ValueError('Некорректный ввод')
            
            return choice

        # Вызов окна ошибки
        except ValueError as e:
            err_window(window, e, 10)
            continue

        finally:
            window.clear()
            window.refresh()
            del window
        

def draw_coice_value_window():
    # Ввод параметров A и B выбранной функции

    flag = 0
    A = ''
    B = ''
    try:
        while True:
            window = curses.newwin(CHOICE_VALUES_WINDOW_HEIGHT, CHOICE_VALUES_WINDOW_WIDTH, HEIGHT_MARGIN, LEFT_MARGIN)
            curses.curs_set(0)
            window.keypad(1)
            curses.noecho()

            window.clear()
            window.border()

            window.addstr(1, 2, 'Введите параметры')
            window.addstr(6, 2, 'Enter - подтвердить')

            window.addstr(3, 2, 'A: ' + A.ljust(9))
            window.addstr(4, 2, 'B: ' + B.ljust(9))

            window.refresh()

            key = window.getch()

            if key == curses.KEY_RESIZE:
                continue

            if key in (curses.KEY_ENTER, 10, 13):
                flag += 1
                if flag > 1:
                    break

            elif key in (curses.KEY_BACKSPACE, 127, 8):
                if flag == 0 and len(A) > 0:
                    A = A[:-1]
                elif flag == 1 and len(B) > 0:
                    B = B[:-1]

            elif key >= ord('0') and key <= ord('9'):
                if flag == 0 and len(A) < 10:
                    A += chr(key)
                elif flag == 1 and len(B) <10:
                    B += chr(key)

            elif key == ord('-'):
                if flag == 0 and len(A) == 0:
                    A += chr(key)
                elif flag == 1 and len(B) == 0:
                    B += chr(key)

            elif key == ord('.'):
                if flag == 0 and len(A) > 0:
                    A += chr(key)
                elif flag == 1 and len(B) > 0:
                    B += chr(key)
            
    finally:
        window.clear()
        window.refresh()
        del window
    try:
        # Если не ввели параметры (A, B), то исходные равны 1
        _A = float(A) if A else 1
        _B = float(B) if B else 1

        return _A, _B 

    except ValueError:
        return None, None


def draw_choice_x1x2_window():
    # Ввод параметров x1, x2, step (от x1 до x2 с шагом {step}) для выбранной функции

    flag = 0
    x1 = ''
    x2 = ''
    step = ''
    try:
        while True:
            window = curses.newwin(CHOICE_x1x2_WINDOW_HEIGHT, CHOICE_x1x2_WINDOW_WINDT, HEIGHT_MARGIN, LEFT_MARGIN)
            curses.curs_set(0)
            window.keypad(1)
            curses.noecho()

            window.clear()
            window.border()

            window.addstr(1, 2, 'Введите диапазон икса (от x1 до x2)')
            window.addstr(7, 2, 'Enter - подтвердить')

            window.addstr(3, 2, 'x1: ' + x1.ljust(9))
            window.addstr(4, 2, 'x2: ' + x2.ljust(9))
            window.addstr(5, 2, 'шаг: ' + step.ljust(8))

            window.refresh()

            key = window.getch()

            if key == curses.KEY_RESIZE:
                continue

            elif key in (curses.KEY_ENTER, 10, 13):
                flag += 1
                if flag > 2:
                    break

            elif key in (curses.KEY_BACKSPACE, 127, 8):
                if flag == 0 and len(x1) > 0:
                    x1 = x1[:-1]
                elif flag == 1 and len(x2) > 0:
                    x2 = x2[:-1]
                elif flag == 2 and len(step) > 0:
                    step = step[:-1]

            elif key >= ord('0') and key <= ord('9'):
                if flag == 0 and len(x1) < 10:
                    x1 += chr(key)
                elif flag == 1 and len(x2) < 10:
                    x2 += chr(key)
                elif flag == 2 and len(step) < 9:
                    step += chr(key)

            elif key == ord('-'):
                if flag == 0 and len(x1) == 0:
                    x1 += chr(key)
                elif flag == 1 and len(x2) == 0:
                    x2 += chr(key)

            elif key == ord('.'):
                if flag == 0 and len(x1) > 0:
                    x1 += chr(key)
                elif flag == 1 and len(x2) > 0:
                    x2 += chr(key)
                elif flag == 2 and len(step) > 0:
                    step += chr(key)
    finally:
        window.clear()
        window.refresh()
        del window
    try:
        # Если не ввели параметры (x1, x2, step), то исходные равны (-10, 10, 1)
        _x1 = float(x1) if x1 else -10
        _x2 = float(x2) if x2 else 10
        _step = float(step) if step else 1

        return _x1, _x2, _step

    except ValueError:
        return None, None, None


def draw_X1X2Y1Y2_window():
    # Ввод параметров X1 X2 Y1 Y2 - размер окна графика при его создании (от X1 до X2, от Y1 до Y2)

    flag = 0
    X1 = ''
    X2 = ''
    Y1 = ''
    Y2 = ''
    try:
        while True:
            window = curses.newwin(X1X2Y1Y2_WINDOW_HEIGHT, X1X2Y1Y2_WINDOW_WIDTH, HEIGHT_MARGIN, LEFT_MARGIN)
            curses.curs_set(0)
            window.keypad(1)
            curses.noecho()

            window.clear()
            window.border()

            window.addstr(1, 2, 'Введите размеры окна графика')
            window.addstr(8, 2, 'Enter - подтвердить')

            window.addstr(3, 2, 'X1: ' + X1.ljust(9))
            window.addstr(4, 2, 'X2: ' + X2.ljust(9))
            window.addstr(5, 2, 'Y1: ' + Y1.ljust(9))
            window.addstr(6, 2, 'Y2: ' + Y2.ljust(9))

            window.refresh()

            key = window.getch()

            if key == curses.KEY_RESIZE:
                continue

            elif key in (curses.KEY_ENTER, 10, 13):
                flag += 1
                if flag > 3:
                    break

            elif key in (curses.KEY_BACKSPACE, 127, 8):
                if flag == 0 and len(X1) > 0:
                    X1 = X1[:-1]
                elif flag == 1 and len(X2) > 0:
                    X2 = X2[:-1]
                elif flag == 2 and len(Y1) > 0:
                    Y1 = Y1[:-1]
                elif flag == 3 and len(Y2) > 0:
                    Y2 = Y2[:-1]

            elif key >= ord('0') and key <= ord('9'):
                if flag == 0 and len(X1) < 10:
                    X1 += chr(key)
                elif flag == 1 and len(X2) < 10:
                    X2 += chr(key)
                elif flag == 2 and len(Y1) < 10:
                    Y1 += chr(key)
                elif flag == 3 and len(Y2) < 10:
                    Y2 += chr(key)

            elif key == ord('-'):
                if flag == 0 and len(X1) == 0:
                    X1 += chr(key)
                elif flag == 1 and len(X2) == 0:
                    X2 += chr(key)
                elif flag == 2 and len(Y1) == 0:
                    Y1 += chr(key)
                elif flag == 3 and len(Y2) == 0:
                    Y2 += chr(key)

            elif key == ord('.'):
                if flag == 0 and len(X1) > 0:
                    X1 += chr(key)
                elif flag == 1 and len(X2) > 0:
                    X2 += chr(key)
                elif flag == 2 and len(Y1) > 0:
                    Y1 += chr(key)
                elif flag == 3 and len(Y2) > 0:
                    Y2 += chr(key)

    finally:
        window.clear()
        window.refresh()
        del window

    try:
        # Если не ввели параметры (X1, X2, Y1, Y2), то исходные равны (0, 3, 0, 3)
        _X1 = float(X1) if X1 else -5
        _X2 = float(X2) if X2 else 5
        _Y1 = float(Y1) if Y1 else -5
        _Y2 = float(Y2) if Y2 else 5

        return _X1, _X2, _Y1, _Y2

    except ValueError:
        return None, None, None, None,


def main():
    try:
        # Инициализация curses
        scr = curses.initscr()
        curses.beep()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(0)

        # Выбор метода построения графика
        method = method_choice()

        if method == 1:
            # Получение параметров для одиночного графика
            choice = draw_func_window()
            A, B = draw_coice_value_window()
            x1, x2, step = draw_choice_x1x2_window()
            X1, X2, Y1, Y2 = draw_X1X2Y1Y2_window()

            # Вычисление значений графика
            chrt = CalculateFunc(A, B, x1, x2, step, choice)
            x, y = chrt.calculate_y()

            # Отрисовка графика
            draw = DrawChart(x, y, X1, X2, Y1, Y2, choice)
            draw_chart = draw.draw_chart()

        elif method == 2:
            # Получение общих параметров для двух графиков
            x1, x2, step = draw_choice_x1x2_window()
            X1, X2, Y1, Y2 = draw_X1X2Y1Y2_window()

            # Получение параметров для первого графика
            choice1 = draw_func_window()
            A1, B1, = draw_coice_value_window()
            
            # Вычисление значений для первого графика
            chrt1 = CalculateFunc(A1, B1, x1, x2, step, choice1)
            x_values, y1 = chrt1.calculate_y()

            # Получение параметров для второго графика
            choice2 = draw_func_window()
            A2, B2 = draw_coice_value_window()

            # Вычисление значений для второго графика
            chrt2 = CalculateFunc(A2, B2, x1, x2, step, choice2)
            x_values, y2 = chrt2.calculate_y()

            # Отрисовка двух графиков
            draw = DrawDoubleChart(x_values, y1, y2, X1, X2, Y1, Y2, choice1, choice2)
            draw_chart = draw._draw_chart()

    finally:
        curses.endwin()

if __name__ == '__main__':
    main()