# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QDesktopWidget, QPushButton, QGridLayout, QMessageBox, QLineEdit
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt


class CalculatorForm(QWidget):
    # Инициализация формы калькулятора с заданными размерами
    def __init__(self, wdt, hgt, parnt=None):
        super().__init__()
        self.wdt = wdt - 50
        self.hgt = hgt
        self.main_form = parnt
        self.current_number = ''
        self.first_number = ''
        self.operation = None
        self.new_number = False
        self.decimal_point = False
        self.result = 0
        self.memory = 0
        self.expression = ''
        self.MAX_NUMBER_LENGTH = 13
        self.set_icon()
        self.initUI()
        
    # Инициализация пользовательского интерфейса калькулятора
    def initUI(self):
        main_grid = QGridLayout()
        main_grid.setContentsMargins(5, 5, 5, 5)
        main_grid.setSpacing(0)

        self.display = QLineEdit()
        self.display.setStyleSheet('''
            QLineEdit {
                background-color: #1a1a1a; /* Темный фон как на скрине */
                color: white; /* Белый текст */
                border: none;
                padding: 20px; /* Отступы внутри поля */
                font-size: 40px; /* Большой шрифт */
            }
            QLineEdit[error="true"] {
                font-size: 20px; /* Меньший шрифт для ошибок */
            }
        ''')
        self.display.setReadOnly(True)
        self.display.setText('0')
        self.display.setAlignment(Qt.AlignRight)
        main_grid.addWidget(self.display, 0, 0, 1, 4)

        buttons_grid = QGridLayout()
        buttons_grid.setSpacing(2)
        
        # Стили кнопок
        button_style = '''
            QPushButton {
                background-color: #333333;
                color: white;
                border: none;
                padding: 19px;
                font-size: 19px;
                border-radius: 5px; /* Добавляем скругление углов */
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
        '''

        # Стиль кнопки '='
        equals_style = '''
            QPushButton {
                background-color: #9b59b6; /* Фиолетовый цвет */
                color: white;
                border: none;
                padding: 19px;
                font-size: 19px;
                border-radius: 5px; /* Добавляем скругление углов */
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
            QPushButton:pressed {
                background-color: #7d3c98;
            }
        '''

        buttons_layout_data = [
            ['(', ')', '\u00f7', '<'],
            ['7', '8', '9', '\u2715'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['C', '0', ',', '=']
        ]

        for r, row in enumerate(buttons_layout_data):
            for c, text in enumerate(row):
                button = QPushButton(text)
                
                if text in ['\u00f7', '\u2715', '-', '+']:
                    button.setStyleSheet(button_style)
                    button.clicked.connect(lambda checked, op=text: self.operation_clicked(op))
                elif text == '=':
                    button.setStyleSheet(equals_style)
                    button.clicked.connect(self.equals_clicked)
                elif text == '<':
                    button.setStyleSheet(button_style)
                    button.clicked.connect(self.backspace_clicked)
                else:
                    button.setStyleSheet(button_style)
                    if text.isdigit() or text == ',':
                        if text == ',':
                            button.clicked.connect(self.decimal_clicked)
                        else:
                            button.clicked.connect(lambda checked, arg=text: self.digit_clicked(arg))
                    elif text == 'C':
                        button.clicked.connect(self.clear_clicked)
                    elif text in ['(', ')']:
                        button.clicked.connect(lambda checked, arg=text: self.parenthesis_clicked(arg))

                buttons_grid.addWidget(button, r, c)

        main_grid.addLayout(buttons_grid, 1, 0, 1, 4)

        self.setLayout(main_grid)
        self.setStyleSheet('background-color: #1a1a1a;')

        self.resize(self.wdt, self.hgt)
        self.center()
        self.setWindowTitle('Калькулятор')
        self.show()

    # Центрирование окна на экране
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Обработка события закрытия окна
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Выход', 'Вы уверены, что хотите выйти?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.hide()
            self.main_form.show()
        else:
            event.ignore()

    # Установка иконки для окна калькулятора
    def set_icon(self):
        try:
            icon = QIcon("icons/calculator.png")
            self.setWindowIcon(icon)
        except Exception as e:
            print(f"Ошибка при загрузке иконки: {e}")

    # Проверка длины числа
    def check_length(self, text):
        if ',' not in text:
            return len(text) <= 13
        
        before_comma, after_comma = text.split(',')
        
        if len(text) > 13:
            return False
            
        if len(after_comma) > 13:
            return False
            
        return True

    # Получение длины текущего числа
    def get_current_number_length(self):
        expr = self.display.text()
        parts = expr.split()
        if parts:
            last_part = parts[-1]
            if last_part.replace(',', '').replace('-', '').isdigit():
                return len(last_part)
        return 0

    # Обработка нажатия цифровой кнопки
    def digit_clicked(self, digit):
        if 'Ошибка' in self.display.text():
            self.display.setText('0')
            self.display.setProperty('error', None)
            self.display.style().polish(self.display)
            
        if self.new_number:
            current = self.display.text()
            if current == '0':
                self.display.setText(digit)
            else:
                self.display.setText(current + digit)
            self.new_number = False
        else:
            if self.get_current_number_length() >= 13:
                return
                
            current = self.display.text()
            parts = current.split()
            if parts:
                last_number = parts[-1]
                if last_number == '0' and ',' not in last_number:
                    if digit == '0':
                        return
                    else:
                        parts[-1] = digit
                        self.display.setText(' '.join(parts))
                        self.current_number = self.display.text()
                        self.expression = self.display.text()
                        return
                
            if current == '0':
                self.display.setText(digit)
            else:
                self.display.setText(current + digit)
                
        self.current_number = self.display.text()
        self.expression = self.display.text()

    # Обработка нажатия кнопки операции
    def operation_clicked(self, op):
        if 'Ошибка' in self.display.text():
            self.display.setText('0')
            self.display.setProperty('error', None)
            self.display.style().polish(self.display)
            
        if self.display.text().count('(') > self.display.text().count(')'):
            display_op = op
            if op == '\u2715':
                display_op = '*'
            elif op == '\u00f7':
                display_op = '/'
            self.display.setText(self.display.text() + ' ' + display_op + ' ')
            self.operation = op
            self.new_number = True
            self.expression = self.display.text()
            return

        if self.first_number == '':
            self.first_number = self.current_number
        else:
            self.equals_clicked()
        
        display_op = op
        if op == '\u2715':
            display_op = '*'
        elif op == '\u00f7':
            display_op = '/'
            
        if self.new_number:
            current = self.display.text()
            if current.endswith(' + ') or current.endswith(' - ') or current.endswith(' * ') or current.endswith(' / '):
                self.display.setText(current[:-3] + ' ' + display_op + ' ')
            else:
                self.display.setText(current + ' ' + display_op + ' ')
        else:
            self.display.setText(self.display.text() + ' ' + display_op + ' ')
            
        self.operation = op
        self.new_number = True
        self.expression = self.display.text()

    # Обработка нажатия кнопки десятичной точки
    def decimal_clicked(self):
        if 'Ошибка' in self.display.text():
            self.display.setText('0')
            self.display.setFont(QFont('Arial', 40))
            
        if self.new_number:
            self.display.setText('0,')
            self.new_number = False
        else:
            current = self.display.text()
            parts = current.split()
            if parts:
                last_number = parts[-1]
                if ',' not in last_number:
                    if len(last_number) < 13:
                        self.display.setText(current + ',')
            else:
                if len(current) < 13:
                    self.display.setText(current + ',')
        self.current_number = self.display.text()
        self.expression = self.display.text()

    # Отображение ошибки
    def show_error(self, message):
        self.display.setText(message)
        self.display.setProperty('error', 'true')
        self.display.style().polish(self.display)
        self.clear_clicked()

    # Валидация числа
    def validate_number(self, number):
        if ',' in number:
            before_comma, after_comma = number.split(',')
            if len(before_comma) > self.MAX_NUMBER_LENGTH:
                return False, 'Ошибка: число слишком длинное'
            if len(after_comma) > self.MAX_NUMBER_LENGTH:
                return False, 'Ошибка: слишком много знаков после запятой'
        else:
            if len(number) > self.MAX_NUMBER_LENGTH:
                return False, 'Ошибка: число слишком длинное'
        
        return True, ''

    # Валидация выражения
    def validate_expression(self, expr):
        if expr.count('(') != expr.count(')'):
            return False, 'Ошибка: незакрытые скобки'
            
        if '/0' in expr or '/ 0' in expr or '/0,' in expr or '/ 0,' in expr:
            return False, 'Ошибка: деление на ноль'
            
        return True, ''

    # Обработка нажатия кнопки равно
    def equals_clicked(self):
        try:
            if self.display.text() == '0':
                return
                
            is_valid, error_message = self.validate_expression(self.expression)
            if not is_valid:
                self.show_error(error_message)
                return
                
            expr = self.expression.replace('\u2715', '*').replace('\u00f7', '/')
            
            try:
                result = eval(expr.replace(',', '.'))
            except ZeroDivisionError:
                self.show_error('Ошибка: деление на ноль')
                return
            except SyntaxError:
                self.show_error('Ошибка: некорректное выражение')
                return
            except:
                self.show_error('Ошибка: некорректное выражение')
                return
            
            if abs(result) > 1e15:
                self.show_error('Ошибка: переполнение')
                return
            
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            result_str = str(result).replace('.', ',')
            
            is_valid, error_message = self.validate_number(result_str)
            if not is_valid:
                self.show_error(error_message)
                return
            
            if len(result_str) > self.MAX_NUMBER_LENGTH:
                if ',' in result_str:
                    before_comma, after_comma = result_str.split(',')
                    available_length = self.MAX_NUMBER_LENGTH - len(before_comma) - 1
                    if available_length > 0:
                        result_str = before_comma + ',' + after_comma[:available_length]
                    else:
                        result_str = before_comma
                else:
                    result_str = result_str[:self.MAX_NUMBER_LENGTH]
            
            self.display.setText(result_str)
            self.display.setProperty('error', None)
            self.display.style().polish(self.display)
            self.first_number = result_str
            self.current_number = result_str
            self.operation = None
            self.new_number = True
            self.expression = result_str
        except:
            self.show_error('Ошибка: неизвестная ошибка')

    # Обработка нажатия кнопки очистки
    def clear_clicked(self):
        error_message = self.display.text() if 'Ошибка' in self.display.text() else '0'
        self.display.setText(error_message)
        if 'Ошибка' not in error_message:
             self.display.setProperty('error', None)
             self.display.style().polish(self.display)
             
        self.current_number = ''
        self.first_number = ''
        self.operation = None
        self.new_number = False
        self.decimal_point = False
        self.result = 0
        self.expression = ''

    # Обработка нажатия кнопки backspace
    def backspace_clicked(self):
        if 'Ошибка' in self.display.text():
            self.display.setText('0')
            self.display.setProperty('error', None)
            self.display.style().polish(self.display)
            self.current_number = '0'
            self.expression = '0'
            return
            
        current = self.display.text()
        if len(current) > 1:
            self.display.setText(current[:-1])
        else:
            self.display.setText('0')
        self.current_number = self.display.text()
        self.expression = self.display.text()

    # Обработка нажатия скобок
    def parenthesis_clicked(self, paren):
        if 'Ошибка' in self.display.text():
            self.display.setText('0')
            self.display.setProperty('error', None)
            self.display.style().polish(self.display)
            
        if self.new_number:
            current = self.display.text()
            if paren == '(':
                last_char = current[-1]
                if last_char.isdigit() or last_char == ')':
                    self.display.setText(current + ' * ' + paren)
                else:
                    self.display.setText(current + paren)
            else:
                self.display.setText(current + paren)
            self.new_number = False
        else:
            current = self.display.text()
            if current == '0':
                self.display.setText(paren)
            else:
                if paren == '(':
                    last_char = current[-1]
                    if last_char.isdigit() or last_char == ')':
                        self.display.setText(current + ' * ' + paren)
                    else:
                        self.display.setText(current + paren)
                else:
                    self.display.setText(current + paren)
        self.expression = self.display.text()

    # Обработка нажатия клавиш клавиатуры
    def keyPressEvent(self, event):
        key = event.text()
        
        if key.isdigit():
            self.digit_clicked(key)
        elif key in ['+', '-', '*', '/']:
            if key == '*':
                self.operation_clicked('\u2715')
            elif key == '/':
                self.operation_clicked('\u00f7')
            else:
                self.operation_clicked(key)

        elif key in [',', '.']:
            self.decimal_clicked()
        elif key in ['\r', '\n', '=']:
            self.equals_clicked()
        elif event.key() == Qt.Key_Escape:
            self.clear_clicked()
        elif event.key() == Qt.Key_Backspace:
            self.backspace_clicked()
        elif key in ['(', ')']:
            self.parenthesis_clicked(key)