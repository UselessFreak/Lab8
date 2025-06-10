# -*- coding: utf-8 -*-

import sys
import os

# Путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from PyQt5.QtWidgets import QWidget, QMessageBox, QDesktopWidget, QApplication, QToolTip, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from src.labs.lab7.test_programming import TestProgg
from src.labs.lab7.test_musicstyle import TestMusic
from src.labs.lab7.calculator import CalculatorForm

class MainForm(QWidget):
    # Инициализация главной формы с заданными размерами
    def __init__(self, wdt, hgt):
        super().__init__()
        self.wdt = wdt
        self.hgt = hgt
        self.initUI()

    # Инициализация интерфейса
    def initUI(self):
        title_label = QLabel('Добро пожаловать в тестовую систему!', self)
        title_label.setStyleSheet('font-size: 18px; font-weight: bold; color: #2c3e50; margin: 20px;')
        title_label.setAlignment(Qt.AlignCenter)
        
        desc_label = QLabel('Выберите один из доступных тестов:', self)
        desc_label.setStyleSheet('font-size: 14px; color: #34495e; margin: 10px;')
        desc_label.setAlignment(Qt.AlignCenter)

        self.btn1 = QPushButton('Тест на определение языка программирования', self)
        self.btn2 = QPushButton('Тест на определение музыкального стиля', self)
        self.btn3 = QPushButton('Калькулятор', self)
        self.quitbtn = QPushButton('Выход', self)
        
        self.set_icon(self.btn1, "icons/programming.png")
        self.set_icon(self.btn2, "icons/music.png")
        self.set_icon(self.btn3, "icons/calculator.png")

        button_style = '''
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                min-width: 300px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2472a4;
            }
        '''
        self.btn1.setStyleSheet(button_style)
        self.btn2.setStyleSheet(button_style)
        self.btn3.setStyleSheet(button_style)
        
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
        self.btn1.setToolTip('Тест на подходящий <b>язык программирования</b>')
        self.btn2.setToolTip('Тест на подходящий <b>музыкальный стиль</b>')
        self.btn3.setToolTip('<b>Простой калькулятор</b>')
        self.quitbtn.setToolTip('<b>Выйти из приложения</b>')

        self.btn1.clicked.connect(self.btn1_clicked)
        self.btn2.clicked.connect(self.btn2_clicked)
        self.btn3.clicked.connect(self.btn3_clicked)
        self.quitbtn.clicked.connect(self._quitbtn)
        
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addSpacing(20)
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        layout.addWidget(self.btn3)
        layout.addSpacing(20)
        layout.addWidget(self.quitbtn, alignment=Qt.AlignRight)
        layout.addStretch()
        
        self.setLayout(layout)
        self.setStyleSheet('background-color: #f5f6fa;')

        self.resize(self.wdt, self.hgt)
        self.center()
        self.setWindowTitle('Тестовая система')
        self.set_icon(False, png="icons/program.png")
        self.show()

    # Установка иконки
    def set_icon(self, btn, png):
        try:
            icon = QIcon(png)
            if btn:
                btn.setIcon(icon)
                btn.setStyleSheet(btn.styleSheet() + "text-align: left; padding-left: 10px;")
            elif not btn:
                self.setWindowIcon(icon)
        except Exception as e:
            print(f"Ошибка при загрузке иконки: {e}")

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
            event.accept()
        else:
            event.ignore()

    # Обработчик нажатия на кнопку теста программирования
    def btn1_clicked(self):
        self.test1 = TestProgg(self.wdt, self.hgt, self)
        self.hide()

    # Обработчик нажатия на кнопку теста музыки
    def btn2_clicked(self):
        self.test2 = TestMusic(self.wdt, self.hgt, self)
        self.hide()

    # Обработчик нажатия на кнопку калькулятора
    def btn3_clicked(self):
        self.calculator = CalculatorForm(400, 400, self)
        self.hide()

    # Обработчик нажатия на кнопку выхода
    def _quitbtn(self):
        app = QApplication.instance()
        app.quit()

def main():
    app = QApplication(sys.argv)
    main_form = MainForm(500, 300)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()