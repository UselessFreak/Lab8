# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QLabel, QDesktopWidget, QToolTip, QPushButton
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QRadioButton, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

class BaseTestForm(QWidget):
    # Инициализация базовой формы теста с заданными размерами
    def __init__(self, wdt, hgt, parnt=None, i=0):
        super().__init__()
        self.wdt = wdt
        self.hgt = hgt
        self.i = i
        self.main_form = parnt
        self.ans_buttons = []
        self.us_answers = {}
        self.initUI()
        self.res_label = QLabel()
        self.res_label.hide()

    # Инициализация пользовательского интерфейса теста
    def initUI(self):
        layout = QGridLayout()
        
        self.main_label = QLabel()
        self.main_label.setStyleSheet('''
            QLabel {
                font-size: 14px;
                color: #2c3e50;
                padding: 20px;
                background-color: white;
                border-radius: 10px;
                margin: 10px;
            }
        ''')
        self.main_label.setAlignment(Qt.AlignTop)
        
        self.nextbtn = QPushButton('Далее', self)
        self.quitbtn = QPushButton('Выход', self)
        
        # Стиль кнопки 'Далее'
        next_style = '''
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                min-width: 100px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2472a4;
            }
        '''
        self.nextbtn.setStyleSheet(next_style)
        
        # Стиль кнопки 'Выход'
        quit_style = '''
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                min-width: 100px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        '''
        self.quitbtn.setStyleSheet(quit_style)
        
        QToolTip.setFont(QFont('SansSerif', 10))
        self.nextbtn.setToolTip('<b>Перейти к следующему вопросу</b>')
        self.quitbtn.setToolTip('<b>Выйти в главное меню</b>')
        
        self.nextbtn.clicked.connect(self.nextbtn_clicked)
        self.quitbtn.clicked.connect(self._quitbtn)
        
        layout.addWidget(self.main_label, 0, 0, 1, 3)
        
        self.ansbtn_layout = QVBoxLayout()
        radio_style = '''
            QRadioButton {
                font-size: 14px;
                color: #2c3e50;
                padding: 10px;
                margin: 5px;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                background-color: white;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #3498db;
                border-radius: 10px;
                background-color: #3498db;
            }
        '''
        for i in range(4):
            ans_button = QRadioButton()
            ans_button.setStyleSheet(radio_style)
            ans_button.clicked.connect(self._answ_selected)
            self.ans_buttons.append(ans_button)
            self.ansbtn_layout.addWidget(ans_button)
            ans_button.hide()
            
        layout.addLayout(self.ansbtn_layout, 1, 0, 1, 3)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.nextbtn)
        button_layout.addStretch()
        button_layout.addWidget(self.quitbtn)
        layout.addLayout(button_layout, 2, 0, 1, 3)
        
        self.setLayout(layout)
        self.setStyleSheet('background-color: #f5f6fa;')
        
        self.resize(self.wdt, self.hgt)
        self.center()
        self.show()

    # Установка иконки для окна теста
    def set_icon(self):
        try:
            icon = QIcon('.png')
            self.setWindowIcon(icon)
        except Exception as e:
            print(f"Ошибка при загрузке иконки: {e}")

    # Центрирование окна на экране
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Обработка выбора ответа
    def _answ_selected(self):
        button = self.sender()
        answ = button.text().strip()
        self.us_answers[self.i] = answ
        for btn in self.ans_buttons:
            if btn != button:
                btn.setChecked(False)

    # Отображение вопроса
    def _show_question(self):
        pass

    # Расчет результатов
    def calc_results(self):
        pass

    # Форматирование результатов
    def txt_results(self):
        pass

    # Обработка нажатия кнопки "Далее"
    def nextbtn_clicked(self):
        self.i += 1
        self._show_question()

    # Обработка нажатия кнопки 'Выход'
    def _quitbtn(self):
        self.hide()
        self.main_form.show()

    # Обработка события закрытия окна
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Выход', 'Вы уверены, что хотите выйти?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self._quitbtn()
        else:
            event.ignore() 