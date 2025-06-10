# -*- coding: utf-8 -*-

import os, random, time, datetime, json, sys
from threading import Thread

if os.getenv('OS') in ['Windows_NT', 'Linux']:
    import msvcrt as m

x = 3
y = 5
game_thread = True
fruit_cord_x = 5
fruit_cord_y = 6
button_default = 'd'
score = 0
icon_player = '>'
tail = 'o'
last2X, last2Y, lastX, lastY = 0, 0, 0, 0
elemX = [0] * 100
elemY = elemX.copy()
name = ''

def clear():
    if os.getenv('OS') == 'Windows_NT':
        os.system('cls')
    elif os.getenv('OS') in [None, 'Linux']:
        os.system('clear')

def write_results():
    try:
        results_path = 'player_results.txt'
        with open(results_path, 'a', encoding='utf-8') as file:
            results = {
                'name': name,
                'score': score,
                'date': datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
            }
            json.dump(results, file, ensure_ascii=False)
            file.write('\n')
    except Exception as e:
        print(f'Ошибка записи в файл: {str(e)}')

def read_results():
    try:
        results_path = 'player_results.txt'
        with open(results_path, 'r', encoding='utf-8') as file:
            results = []
            for l in file:
                result = json.loads(l)
                results.append(result)
            return results
    except Exception as e:
        print(f'Ошибка чтения файла: {str(e)}')
        return []

def game_over():
    global game_thread
    print(f'\nGAME OVER\nВаши очки: {score}')
    game_thread = False
    write_results()
    sys.exit(0)

def board(width: int = 40, height: int = 20, pos_player_x: int = x, pos_player_y: int = y):
    global score, fruit_cord_x, fruit_cord_y, game_thread, icon_player, last2X, lastX, lastY, last2Y, elemY, elemX
    
    # Проверяем условия game over до очистки консоли
    for el in range(score):
        if pos_player_x == elemX[el] and pos_player_y == elemY[el]:
            game_over()
            return

    if not (x in range(width - 39)) and not (y in range(height - 1)) or not (x in range(width - 1)) and not (y in range(height - 19)):
        game_over()
        return

    clear()  # Очищаем консоль только если не game over
    for i in range(height):
        for j in range(width):
            if pos_player_x == fruit_cord_x and pos_player_y == fruit_cord_y:
                fruit_cord_x = random.randint(5, width - 1)
                fruit_cord_y = random.randint(5, height - 1)
                score += 1

            if j == 0:
                print('\t', end='')
                print('#', end='')
            elif i == 0:
                print('#', end='')
            elif i == height - 1:
                print('#', end='')
            elif j == width -1:
                print('#', end='')
            elif pos_player_x == j and pos_player_y == i:
                print(icon_player, end='')
            elif fruit_cord_x == j and fruit_cord_y == i:
                print('*', end='')
            else:
                pr = True
                for ls in range(score):
                    if elemX[ls] == j and elemY[ls] == i:
                        print(tail, end='')
                        pr = False
                if pr:
                    print(' ', end='')
        print()

    print(f'\tОчки: {score}\n\n\t\tWASD / Стрелочки - перемещение\n\t\t\tESC - выйти')
    lastX, lastY, = pos_player_x, pos_player_y
    if score > 0:
        for el in range(score):
            last2X, last2Y = elemX[el], elemY[el]
            elemX[el], elemY[el] = lastX, lastY
            lastX, lastY = last2X, last2Y

def button_move():
    global button_default
    if os.getenv('OS') in ['Windows_NT', 'Linux']:
        while game_thread:
            try:
                key = m.getch()
                if key == b'\x1b':  # ESC
                    button_default = 'exit'
                elif key == b'\xe0':  # Специальные клавиши (стрелки)
                    key = m.getch()
                    if key == b'H':  # Вверх
                        button_default = 'w'
                    elif key == b'P':  # Вниз
                        button_default = 's'
                    elif key == b'K':  # Влево
                        button_default = 'a'
                    elif key == b'M':  # Вправо
                        button_default = 'd'
                else:
                    button_default = key.decode('utf-8').lower()
            except:
                pass
    else:
        while game_thread:
            button_default = input('Нажмите кнопку перемещения: ')

def move():
    global x, y, game_thread, button_default, icon_player

    while game_thread:
        if button_default in ['', ' ']:
            button_default = 'd'
        elif button_default == 'w':
            y -= 1
            icon_player = '^'
        elif button_default == 'a':
            x -= 1
            icon_player = '<'
        elif button_default == 's':
            y += 1
            icon_player = 'v'
        elif button_default == 'd':
            x += 1
            icon_player = '>'
        elif button_default == 'exit':
            print(f'Вы покинули игру\nВаши очки: {score} - ваши очки не были засчитаны')
            game_thread = False
            sys.exit(0)

        board(pos_player_x=x, pos_player_y=y)
        time.sleep(0.2)

def main():
    board()
    Thread(target=move).start()
    Thread(target=button_move).start()

def menu():
    global name, game_thread
    clear()
    print(f'Программа консольная змейка | Управление - стрелки клавиатуры')
    print('\n\n\t\t'+ '-'*29 +'\n\t\t| 1 - Играть\t\t    |\n\t\t'+ '-'*29 +'\n\t\t| 2 - Посмотреть результаты |\n\t\t'+ '-'*29 +'\n\t\t| 3 - Выход\t\t    |\n\t\t'+ '-'*29)
    if os.getenv('OS') in ['Windows_NT', 'Linux']:
        btn = m.getch()[0]
    else:
        btn = input('Выберите пункт: ')
    if btn in ['1', 49]:
        status = True
        while status:
            clear()
            name = input('Придумайте имя змейке\n> ')
            if name not in [' ', ''] and len(name) != 0:
                status = False
            else:
                print('Ошибка, имя змейки не может быть пустым!!')
                time.sleep(2)
        clear()

        main()
    elif btn in ['2', 50]:
        clear()
        results = read_results()
        if results:
            for res in results:
                print('-'*23)
                print(f'Имя: {res["name"]}')
                print(f'Очки: {res["score"]}')
                print(f'Дата {res["date"]}')
            print('-'*23)        
        else:
            print('Нет результатов')
        input('\nНажмите <Enter> для выхода\n')
        clear()

        menu()
    elif btn in ['3', 51]:
        exit()

if __name__ == '__main__':
    menu()

