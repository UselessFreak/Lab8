# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import sys, os, time
import subprocess

from PyQt5.QtWidgets import (QWidget, QMessageBox, QDesktopWidget, QApplication, QToolTip, QPushButton, QVBoxLayout, QLabel, QMainWindow, QAction, QToolBar, QStatusBar)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

from src.labs.lab6.graphs import main as graphs_main

class MainWindow(QMainWindow):
    def __init__(self, wdt, hgt):
        super().__init__()
        self.wdt = wdt
        self.hgt = hgt
        self.initUI()

    # Инициализация интерфейса
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.create_menu_bar()
        
        self.create_tool_bar()
        
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('Готов к работе')

        layout = QVBoxLayout(central_widget)
        
        title_label = QLabel('Добро пожаловать в тестовую систему!', self)
        title_label.setStyleSheet('font-size: 18px; font-weight: bold; color: #2c3e50; margin: 20px;')
        title_label.setAlignment(Qt.AlignCenter)
        
        desc_label = QLabel('Выберите один из доступных модулей:', self)
        desc_label.setStyleSheet('font-size: 14px; color: #34495e; margin: 10px;')
        desc_label.setAlignment(Qt.AlignCenter)

        # Создаем кнопки для лабораторных работ
        self.btn_snake = QPushButton('Змейка', self)
        self.btn_tetris = QPushButton('Тетрис', self)
        self.btn_graphs = QPushButton('Графики', self)
        self.btn_app = QPushButton('Тесты и калькулятор', self)
        self.btn_filemanager = QPushButton('Файловый менеджер', self)
        self.quitbtn = QPushButton('Выход', self)
        
        # Установка иконок
        self.set_icon(self.btn_snake, "icons/snake.png")
        self.set_icon(self.btn_tetris, "icons/tetris.png")
        self.set_icon(self.btn_graphs, "icons/graph.png")
        self.set_icon(self.btn_app, "icons/app.png")
        self.set_icon(self.btn_filemanager, "icons/filemanager.png")

        # Стили для кнопок
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
        self.btn_snake.setStyleSheet(button_style)
        self.btn_tetris.setStyleSheet(button_style)
        self.btn_graphs.setStyleSheet(button_style)
        self.btn_app.setStyleSheet(button_style)
        self.btn_filemanager.setStyleSheet(button_style)
        
        # Стиль кнопки "Выход"
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

        # Подсказки
        QToolTip.setFont(QFont('SansSerif', 10))
        self.btn_snake.setToolTip('Запустить игру <b>Змейка</b>')
        self.btn_tetris.setToolTip('Запустить игру <b>Тетрис</b>')
        self.btn_graphs.setToolTip('Открыть <b>Графики</b>')
        self.btn_app.setToolTip('Открыть <b>Тесты и калькулятор</b>')
        self.btn_filemanager.setToolTip('Открыть <b>Файловый менеджер</b>')
        self.quitbtn.setToolTip('<b>Выйти из приложения</b>')

        self.btn_snake.clicked.connect(self.open_snake)
        self.btn_tetris.clicked.connect(self.open_tetris)
        self.btn_graphs.clicked.connect(self.open_graphs)
        self.btn_app.clicked.connect(self.open_app)
        self.btn_filemanager.clicked.connect(self.open_filemanager)
        self.quitbtn.clicked.connect(self._quitbtn)
        
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addSpacing(20)
        layout.addWidget(self.btn_snake)
        layout.addWidget(self.btn_tetris)
        layout.addWidget(self.btn_graphs)
        layout.addWidget(self.btn_app)
        layout.addWidget(self.btn_filemanager)
        layout.addSpacing(20)
        layout.addWidget(self.quitbtn, alignment=Qt.AlignRight)
        layout.addStretch()
        
        self.setStyleSheet('background-color: #f5f6fa;')
        self.resize(self.wdt, self.hgt)
        self.center()
        self.setWindowTitle('Лабораторные работы')
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

    # Создание основной менюшки
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        labs_menu = menubar.addMenu('Приложение')
        
        snake_action = QAction('Змейка', self)
        snake_action.triggered.connect(self.open_snake)
        labs_menu.addAction(snake_action)
        
        tetris_action = QAction('Тетрис', self)
        tetris_action.triggered.connect(self.open_tetris)
        labs_menu.addAction(tetris_action)
        
        graphs_action = QAction('Графики', self)
        graphs_action.triggered.connect(self.open_graphs)
        labs_menu.addAction(graphs_action)
        
        app_action = QAction('Тесты и калькулятор', self)
        app_action.triggered.connect(self.open_app)
        labs_menu.addAction(app_action)
        
        filemanager_action = QAction('Файловый менеджер', self)
        filemanager_action.triggered.connect(self.open_filemanager)
        labs_menu.addAction(filemanager_action)

    # Панель инструментов
    def create_tool_bar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        snake_action = QAction(QIcon('icons/snake.png'), 'Змейка', self)
        snake_action.triggered.connect(self.open_snake)
        toolbar.addAction(snake_action)
        
        tetris_action = QAction(QIcon('icons/tetris.png'), 'Тетрис', self)
        tetris_action.triggered.connect(self.open_tetris)
        toolbar.addAction(tetris_action)
        
        graphs_action = QAction(QIcon('icons/graph.png'), 'Графики', self)
        graphs_action.triggered.connect(self.open_graphs)
        toolbar.addAction(graphs_action)
        
        app_action = QAction(QIcon('icons/app.png'), 'Тесты и калькулятор', self)
        app_action.triggered.connect(self.open_app)
        toolbar.addAction(app_action)
        
        filemanager_action = QAction(QIcon('icons/filemanager.png'), 'Файловый менеджер', self)
        filemanager_action.triggered.connect(self.open_filemanager)
        toolbar.addAction(filemanager_action)

    # Запуск игры Змейка (lab3)
    def open_snake(self):
        self.statusBar.showMessage('Запуск игры Змейка...')
        QApplication.processEvents()
        time.sleep(1.25)
        self.hide()
        try:
            # Получение пути к файлу snake.py
            snake_path = os.path.join(os.path.dirname(__file__), 'src', 'labs', 'lab3', 'snake.py')

            snake_dir = os.path.dirname(snake_path)
            process = subprocess.Popen([sys.executable, snake_path], cwd=snake_dir)

            process.wait()

            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
        finally:
            self.show()
            self.statusBar.showMessage('Готов к работе')

    # Запуск игры Тетрис (lab5)
    def open_tetris(self):
        self.statusBar.showMessage('Запуск игры Тетрис...')
        QApplication.processEvents()
        time.sleep(1.25)
        self.hide()
        try:
            # Получение пути к файлу tetris.py
            tetris_path = os.path.join(os.path.dirname(__file__), 'src', 'labs', 'lab5', 'tetris.py')

            tetris_dir = os.path.dirname(tetris_path)
            process = subprocess.Popen([sys.executable, tetris_path], cwd=tetris_dir)

            process.wait()

            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')

        finally:
            self.show()
            self.statusBar.showMessage('Готов к работе')

    # Запуск приложения с графиками (lab6)
    def open_graphs(self):
        self.statusBar.showMessage('Открытие графиков...')
        QApplication.processEvents()
        time.sleep(1.25)
        self.hide()
        try:
            graphs_main()

            while plt.get_fignums():
                plt.pause(0.1)

        finally:
            plt.close('all')
            self.show()
            self.statusBar.showMessage('Готов к работе')

    # Запуск приложения с тестами и калькулятором (lab7)
    def open_app(self):
        self.statusBar.showMessage(f'Открытие приложения...')
        QApplication.processEvents()
        time.sleep(1.25)
        self.hide()
        try:
            # Получение пути к файлу app.py
            app_path = os.path.join(os.path.dirname(__file__), 'src', 'labs', 'lab7', 'app.py')

            app_dir = os.path.dirname(app_path)
            process = subprocess.Popen([sys.executable, app_path], cwd=app_dir)

            process.wait()

        finally:
            self.show()
            self.statusBar.showMessage('Готов к работе')

    # Запуск файлового менеджера
    def open_filemanager(self):
        self.statusBar.showMessage('Открытие файлового менеджера...')
        QApplication.processEvents()
        time.sleep(1.25)
        self.hide()
        try:
            # Получение пути к файлу filemanager.py
            filemanager_path = os.path.join(os.path.dirname(__file__), 'src', 'file_manager', 'filemanager.py')

            filemanager_dir = os.path.dirname(filemanager_path)
            process = subprocess.Popen([sys.executable, filemanager_path], cwd=filemanager_dir)
            
            process.wait()
            
        finally:
            self.show()
            self.statusBar.showMessage('Готов к работе')

    # Обработчик нажатия на кнопку выхода
    def _quitbtn(self):
        app = QApplication.instance()
        app.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow(500, 300)

    sys.exit(app.exec_())