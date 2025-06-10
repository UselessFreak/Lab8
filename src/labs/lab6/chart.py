# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import math as m
import numpy as np

class DrawChart:
    # Класс для отрисовки выбранной функции

    def __init__(self, x, y, X1, X2, Y1, Y2, choice):
        self.x = x
        self.y = y
        self.X1 = X1
        self.X2 = X2
        self.Y1 = Y1
        self.Y2 = Y2
        self.choice = choice

    def _calculate_y(self, k):
        # Вычисляет значения y для базового графика в зависимости от выбранной функции

        if self.choice == 'sin(x)':
            _y = np.sin(m.pi * k)
        elif self.choice == 'cos(x)':
            _y = np.cos(m.pi * k)
        elif self.choice == 'exp(x)':
            _y = np.exp(k)
        elif self.choice == 'x^2':
            _y = k**2
        elif self.choice == 'ln(x)':
            _y = np.log(k)
        else:
            _y = np.zeros_like(k)
        return _y

    def _add_labels(self, ax):
        # Добавляет заголовок, подписи осей и текст с формулой функции на график

        font = {'fontname': 'Times New Roman'}
        ax.set_xlabel('Значения по x', color='gray')
        ax.set_ylabel('Значения по y', color='gray')

        if self.choice == 'sin(x)':
            ax.set_title('Синусоида', fontsize=20, **font)
            ax.text(self.x[-1] + 0.5, self.y[-1], r'$y = sin(x)$', fontsize=10, bbox={'facecolor':'gray', 'alpha':0.2}, clip_on=True)
        elif self.choice == 'cos(x)':
            ax.set_title('Косинусоида', fontsize=20, **font)
            ax.text(self.x[-1] + 0.5, self.y[-1], r'$y = cos(x)$', fontsize=10, bbox={'facecolor':'gray', 'alpha':0.2}, clip_on=True)
        elif self.choice == 'exp(x)':
            ax.set_title('Экспонента', fontsize=20, **font)
            ax.text(self.x[-1] + 0.5, self.y[-1], r'$y = exp$', fontsize=10, bbox={'facecolor':'gray', 'alpha':0.2}, clip_on=True)
        elif self.choice == 'x^2':
            ax.set_title('x в квадрате', fontsize=20, **font)
            ax.text(self.x[-1] + 0.5, self.y[-1], r'$y = x^2$', fontsize=10, bbox={'facecolor':'gray', 'alpha':0.2}, clip_on=True)
        elif self.choice == 'ln(x)':
            ax.set_title('Логарифм', fontsize=20, **font)
            ax.text(self.x[-1] + 0.5, self.y[-1], r'$y = ln(x)$', fontsize=10, bbox={'facecolor':'gray', 'alpha':0.2}, clip_on=True)
        
    def _draw_points(self, ax):
        # Отрисовывает точки графика и их координаты, и соединяет их линией

        ax.plot(self.x, self.y, 'ko')
        for i in range(len(self.x)):
            ax.text(self.x[i], self.y[i] + 0.5, f'({self.x[i]:.2f}, {self.y[i]:.2f})', ha='center', va='bottom', clip_on=True)
        ax.plot(self.x, self.y, 'b-')

    def draw_chart(self):
        # Создает и отображает график выбранной функции

        fig, ax = plt.subplots()
        k = np.arange(-40, 60, 0.1)

        ax.grid(True)

        ax.axis([self.X1, self.X2, self.Y1, self.Y2])

        self._add_labels(ax)

        _y = self._calculate_y(k)

        self._draw_points(ax)

        # Базовый график (пунктирная линия)
        ax.plot(k, _y, 'k--', alpha=0.2)
        ax.legend(['Точки графика'], loc=2)

        # Оси Ox и Oy
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=0.8)

        def on_close(event):
            plt.close('all')
            return

        fig.canvas.mpl_connect('close_event', on_close)
        plt.show(block=False)
        plt.pause(0.1)




class DrawDoubleChart:
    # Класс для отрисовки двух выбранных функций

    def __init__(self, x_values, y1, y2, X1, X2, Y1, Y2, choice1, choice2):
        self.x = x_values
        self.y1 = y1
        self.y2 = y2
        self.X1 = X1
        self.X2 = X2
        self.Y1 = Y1
        self.Y2 = Y2
        self.choice1 = choice1
        self.choice2 = choice2

    def find_intersections(self):
        # Находит приближенные точки пересечения

        intersections = []
        for i in range(len(self.x) - 1):  
            if (self.y1[i] - self.y2[i]) * (self.y1[i+1] - self.y2[i+1]) < 0:
                # Линейная интерполяция для нахождения координат точек пересечения
                
                x_intersection = self.x[i] + (self.x[i+1] - self.x[i]) * abs(self.y1[i] - self.y2[i]) / (abs(self.y1[i] - self.y2[i]) + abs(self.y1[i+1] - self.y2[i+1]))
                y_intersection = self.y1[i] + (self.y1[i+1] - self.y1[i]) * (x_intersection - self.x[i]) / (self.x[i+1] - self.x[i])

                intersections.append((x_intersection, y_intersection))

        # Проверка пересечения графиков в точке ноль по иксу
        for i in range(len(self.x)):
            if abs(self.x[i]) < 0.000001:
                if np.isclose(self.y1[i], self.y2[i]):
                    y_intersection = (self.y1[i] + self.y2[i]) / 2
                    intersections.append((0.0, y_intersection))
                break

        return intersections

    def _draw_graphs(self, ax):
        # Отрисовывает графики двух функций на одном графике

        ax.plot(self.x, self.y1, 'b-', label=f'{self.choice1}')
        ax.plot(self.x, self.y2, 'g-', label=f'{self.choice2}')
        ax.grid(True)

    def _add_labels(self, ax):
        # Добавляет заголовок графика с именами выбранных функций

        font = {'fontname': 'Times New Roman'}
        title = f'F1 = {self.choice1} F2 = {self.choice2}'
        ax.set_title(title, fontsize=20, **font)

    def _draw_points(self, ax):
        # Отрисовывает точки и их координаты для графиков обеих функций

        ax.plot(self.x, self.y1, 'bo', markersize=3, label=f'Точки {self.choice1}')
        for i in range(len(self.x)):
            ax.text(self.x[i], self.y1[i] + 0.5, f'({self.x[i]:.2f}, {self.y1[i]:.2f})', ha='center', va='bottom', clip_on=True)

        ax.plot(self.x, self.y2, 'go', markersize=3, label=f'Точки {self.choice2}')
        for i in range(len(self.x)):
            ax.text(self.x[i], self.y2[i] + 0.5, f'({self.x[i]:.2f}, {self.y2[i]:.2f})', ha='center', va='bottom', clip_on=True)

    def _plot_intersections(self, ax, intersections):
        # Отрисовывает точки пересечения и их координаты

        flag = True
        for x, y in intersections:
            if flag:
                ax.plot(x, y, 'ro', markersize=5, label='Точки пересечения')
                flag = False
            else:
                ax.plot(x, y, 'ro', markersize=5)

            ax.text(x, y + 0.5, f'({x:.2f}, {y:.2f})', ha='center', va='bottom', clip_on=True)

    def _draw_chart(self):
        # Создает и отображает график с двумя функциями и точками их пересечения

        fig, ax = plt.subplots()

        ax.axis([self.X1, self.X2, self.Y1, self.Y2])

        self._draw_graphs(ax)
        self._add_labels(ax)
        self._draw_points(ax)
        
        intersections = self.find_intersections()
        self._plot_intersections(ax, intersections)

        # Табличка с корнями уравнения F1(x) = F2(x); x точки пересечения графиков
        x_values = ', '.join([f'{x:.2f}' for x, y in intersections])
        ax.text(0.95, 0.95, f'Корни (x) уравнения F1(x) = F2(x): {x_values}', transform=ax.transAxes, ha='right', va='top', bbox={'facecolor': 'white', 'alpha':0.7}, clip_on=True)
        
        # Оси Ox и Oy
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=0.8)
        
        ax.legend(loc=2)

        def on_close(event):
            plt.close('all')
            return

        fig.canvas.mpl_connect('close_event', on_close)
        plt.show(block=False)
        plt.pause(0.1)
