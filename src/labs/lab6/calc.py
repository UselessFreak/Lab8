# -*- coding: utf-8 -*-

import numpy as np

class CalculateFunc:
    # Вычисление значений для выбранной функции
    
    def __init__(self, A, B, x1, x2, step, choice):
        self.A = A
        self.B = B
        self.x1 = x1
        self.x2 = x2
        self.step = step
        self.choice = choice
        self.t = self.calculate_t()
    
    def calculate_t(self):
        # Создание массива t значений x от x1 до x2 (не включая) с шагом {step}
        return np.arange(self.x1, self.x2, self.step)

    def calculate_y(self):
        # Создание массива y значений y относительно введенных параметров

        if self.choice == 'sin(x)':
            y = self.A * np.sin(self.B * self.t)

        elif self.choice == 'cos(x)':
            y = self.A * np.cos(self.B * self.t)

        elif self.choice == 'exp(x)':
            y = self.A * np.exp(self.B * self.t)

        elif self.choice == 'x^2':
            y = self.A * np.power(self.B * self.t, 2)

        elif self.choice == 'ln(x)':
            try:
                y = self.A * np.log(self.B * self.t)
            except ValueError:
                return np.full_like(self.t, np.nan)

        return self.t, y
