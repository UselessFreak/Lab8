# -*- coding: utf-8 -*-

import sys, os

from PyQt5.QtWidgets import (QMainWindow, QAction, QApplication, QFileDialog, QMessageBox, QTabWidget, QWidget, QToolBar, QStatusBar, QDesktopWidget, QFontDialog, QColorDialog, QPlainTextEdit)
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette, QPainter
from PyQt5.QtCore import Qt, QSettings, QRect, QSize

# Виджет для отображения номеров строк
class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    # Возвращает размер виджета
    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)
    
    # Отрисовка виджета
    def paintEvent(self, event):
        
        self.editor.line_number_area_paint_event(event)

# Текстовый редактор с номерами строк
class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.update_line_number_area_width(0)

    # Вычисление ширины области номеров строк
    def line_number_area_width(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space
    
    # Обновление отступов для номеров строк
    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    # Обновление области номеров при прокрутке
    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    # Обработка изменения размера редактора
    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    # Отрисовка номеров строк
    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        
        # Фон области номеров
        painter.fillRect(event.rect(), QColor('#f0f0f0'))
        
        # Разделительная линия
        painter.setPen(QColor('#d0d0d0'))
        painter.drawLine(event.rect().right(), event.rect().top(), 
                        event.rect().right(), event.rect().bottom())

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = int(top + self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                if block_number == self.textCursor().blockNumber():
                    painter.setPen(QColor('#2c3e50'))
                    painter.fillRect(0, top, self.line_number_area.width(), self.fontMetrics().height(),
                                   QColor('#e8e8e8'))
                else:
                    painter.setPen(QColor('#808080'))
                
                painter.drawText(0, top, self.line_number_area.width() - 5, self.fontMetrics().height(),
                               Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = int(top + self.blockBoundingRect(block).height())
            block_number += 1

# Главный класс файлового менеджера
class FileManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.settings = QSettings('FileManager', 'Settings')
        self.load_settings()
        self.initUI()

    # Загрузка настроек приложения
    def load_settings(self):
        # Папка для сохранения (стоит по умолчанию)
        self.save_dir = self.settings.value('save_dir', os.path.join(os.path.dirname(__file__), 'saves'))

        self.default_font = self.settings.value('default_font', QFont('Arial', 10))
        self.default_color = self.settings.value('default_color', QColor('black'))
        
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    # Сохранение настроек
    def save_settings(self):
        self.settings.setValue('save_dir', self.save_dir)
        self.settings.setValue('default_font', self.default_font)
        self.settings.setValue('default_color', self.default_color)

    # Инициализация интерфейса
    def initUI(self):
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)
        
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('Готов к работе')
        
        self.create_menu()
        self.create_toolbar()
        
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Файловый менеджер')
        self.setWindowIcon(QIcon('icons/filemanager.png'))
        self.center()
        self.show()
        
    def create_menu(self):
        menubar = self.menuBar()
        
        # Меню "Файл"
        fileMenu = menubar.addMenu('Файл')
        
        # Действия для меню "Файл"
        newAction = QAction(QIcon('icons/new.png'), 'Новый файл', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('Создать новый файл')
        newAction.triggered.connect(self.new_file)
        
        openAction = QAction(QIcon('icons/open.png'), 'Открыть файл', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Открыть файл')
        openAction.triggered.connect(self.open_file)
        
        saveAction = QAction(QIcon('icons/save.png'), 'Сохранить', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Сохранить файл')
        saveAction.triggered.connect(self.save_file)
        
        saveAsAction = QAction(QIcon('icons/saveas.png'), 'Сохранить как', self)
        saveAsAction.setShortcut('Ctrl+Shift+S')
        saveAsAction.setStatusTip('Сохранить файл как')
        saveAsAction.triggered.connect(self.save_file_as)
        
        exitAction = QAction(QIcon('icons/exit.png'), 'Выход', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Выйти из приложения')
        exitAction.triggered.connect(self.close)
        
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)
        
        # Меню "Настройки"
        settingsMenu = menubar.addMenu('Настройки')
        
        # Действия для меню "Настройки"
        changeSaveDirAction = QAction(QIcon('icons/folder.png'), 'Изменить папку сохранений', self)
        changeSaveDirAction.triggered.connect(self.change_save_dir)
        settingsMenu.addAction(changeSaveDirAction)
        
        changeFontAction = QAction(QIcon('icons/font.png'), 'Шрифт по умолчанию', self)
        changeFontAction.triggered.connect(self.change_default_font)
        settingsMenu.addAction(changeFontAction)
        
        changeColorAction = QAction(QIcon('icons/color.png'), 'Цвет текста по умолчанию', self)
        changeColorAction.triggered.connect(self.change_default_color)
        settingsMenu.addAction(changeColorAction)
        
    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Добавление действий на панель инструментов
        toolbar.addAction(QAction(QIcon('icons/new.png'), 'Новый файл', self, triggered=self.new_file))
        toolbar.addAction(QAction(QIcon('icons/open.png'), 'Открыть файл', self, triggered=self.open_file))
        toolbar.addAction(QAction(QIcon('icons/save.png'), 'Сохранить', self, triggered=self.save_file))
        toolbar.addAction(QAction(QIcon('icons/saveas.png'), 'Сохранить как', self, triggered=self.save_file_as))
        
        toolbar.addSeparator()
        
        # Кнопки для шрифта и цвета
        fontAction = QAction(QIcon('icons/font.png'), 'Шрифт', self)
        fontAction.triggered.connect(self.change_font)
        toolbar.addAction(fontAction)
        
        colorAction = QAction(QIcon('icons/color.png'), 'Цвет текста', self)
        colorAction.triggered.connect(self.change_color)
        toolbar.addAction(colorAction)
        
    # Создать файл
    def new_file(self):
        text_edit = CodeEditor()
        text_edit.setFont(self.default_font)
        text_edit.setStyleSheet(f"color: {self.default_color.name()}")
        text_edit.textChanged.connect(self.update_statistics)
        self.tabs.addTab(text_edit, "Новый файл")
        self.tabs.setCurrentWidget(text_edit)
        self.statusBar.showMessage('Создан новый файл')
        self.update_statistics()
        
    # Открыть файл
    def open_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Открыть файл', '', 'Текстовые файлы (*.txt);;Python файлы (*.py);;Все файлы (*)')[0]
        if fname:
            try:
                with open(fname, 'r', encoding='utf-8') as f:
                    text = f.read()
                text_edit = CodeEditor()
                text_edit.setPlainText(text)
                text_edit.setFont(self.default_font)
                text_edit.setStyleSheet(f"color: {self.default_color.name()}")
                text_edit.textChanged.connect(self.update_statistics)
                self.tabs.addTab(text_edit, os.path.basename(fname))
                self.tabs.setCurrentWidget(text_edit)
                self.statusBar.showMessage(f'Файл {fname} открыт')
                self.update_statistics()
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Не удалось открыть файл: {str(e)}')
                
    # Сохраненить файл
    def save_file(self):
        current_tab = self.tabs.currentWidget()
        if not current_tab:
            return
            
        if not hasattr(current_tab, 'file_path'):
            # Если файл еще не сохранен, предлагаем сохранить в папке saves
            default_name = os.path.join(self.save_dir, "Новый файл.txt")
            fname = QFileDialog.getSaveFileName(self, 'Сохранить файл', default_name, 'Текстовые файлы (*.txt);;Python файлы (*.py);;Все файлы (*)')[0]
            if fname:
                try:
                    with open(fname, 'w', encoding='utf-8') as f:
                        f.write(current_tab.toPlainText())
                    current_tab.file_path = fname
                    self.tabs.setTabText(self.tabs.currentIndex(), os.path.basename(fname))
                    self.statusBar.showMessage(f'Файл {fname} сохранен')
                except Exception as e:
                    QMessageBox.warning(self, 'Ошибка', f'Не удалось сохранить файл: {str(e)}')
        else:
            try:
                with open(current_tab.file_path, 'w', encoding='utf-8') as f:
                    f.write(current_tab.toPlainText())
                self.statusBar.showMessage(f'Файл {current_tab.file_path} сохранен')
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Не удалось сохранить файл: {str(e)}')
                
    # Сохранить файл как...
    def save_file_as(self):
        current_tab = self.tabs.currentWidget()
        if not current_tab:
            return
            
        fname = QFileDialog.getSaveFileName(self, 'Сохранить файл', '', 'Текстовые файлы (*.txt);;Python файлы (*.py);;Все файлы (*)')[0]
        if fname:
            try:
                with open(fname, 'w', encoding='utf-8') as f:
                    f.write(current_tab.toPlainText())
                current_tab.file_path = fname
                self.tabs.setTabText(self.tabs.currentIndex(), os.path.basename(fname))
                self.statusBar.showMessage(f'Файл {fname} сохранен')
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Не удалось сохранить файл: {str(e)}')
                
    def close_tab(self, index):
        current_tab = self.tabs.widget(index)
        if current_tab and current_tab.toPlainText():
            reply = QMessageBox.question(self, 'Подтверждение', 'Сохранить изменения перед закрытием?', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            
            if reply == QMessageBox.Yes:
                self.save_file()
            elif reply == QMessageBox.Cancel:
                return
                
        self.tabs.removeTab(index)
        
    def closeEvent(self, event):
        has_unsaved = False
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            if tab and tab.toPlainText():
                has_unsaved = True
                break

        if has_unsaved:
            reply = QMessageBox.question(self, 'Подтверждение', 'Есть несохраненные изменения. Сохранить перед выходом?', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            
            if reply == QMessageBox.Yes:
                self.save_file()
            elif reply == QMessageBox.Cancel:
                event.ignore()
                return
        else:
            reply = QMessageBox.question(self, 'Подтверждение', 'Вы уверены, что хотите выйти?', QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.No:
                event.ignore()
                return
                
        event.accept()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Изменение папки для сохранения в настройках
    def change_save_dir(self):
        new_dir = QFileDialog.getExistingDirectory(self, 'Выберите папку для сохранений', self.save_dir)
        if new_dir:
            self.save_dir = new_dir
            self.save_settings()
            self.statusBar.showMessage(f'Папка сохранений изменена на: {new_dir}')

    # Изменение базоого шрифта в настройках
    def change_default_font(self):
        font, ok = QFontDialog.getFont(self.default_font, self)
        if ok:
            self.default_font = font
            self.save_settings()
            self.statusBar.showMessage('Шрифт по умолчанию изменен')

    # Изменение базового цвета в настройках
    def change_default_color(self):
        color = QColorDialog.getColor(self.default_color, self, 'Выберите цвет текста')
        if color.isValid():
            self.default_color = color
            self.save_settings()
            self.statusBar.showMessage('Цвет текста по умолчанию изменен')

    # Изменить шрифт
    def change_font(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            font, ok = QFontDialog.getFont(current_tab.font(), self)
            if ok:
                current_tab.setFont(font)

    # Изменить цвет
    def change_color(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            color = QColorDialog.getColor(QColor(current_tab.palette().color(QPalette.Text)), self, 'Выберите цвет текста')
            if color.isValid():
                current_tab.setStyleSheet(f"color: {color.name()}")
                
    # Статистика файла
    def update_statistics(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            text = current_tab.toPlainText()
            lines = text.count('\n') + 1
            chars = len(text)
            words = len(text.split())
            self.statusBar.showMessage(f'Строк: {lines} | Слов: {words} | Символов: {chars}')

def main():
    app = QApplication(sys.argv)
    ex = FileManager()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 