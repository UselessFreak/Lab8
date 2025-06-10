# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMessageBox
from src.labs.lab7.for_tests import BaseTestForm
from src.labs.lab7.test_data import LANGUAGE_QUESTIONS, LANGUAGE_DESCRIPTIONS
from PyQt5.QtGui import QIcon

class TestProgg(BaseTestForm):
    # Инициализация теста на определение языка программирования
    def __init__(self, wdt, hgt, parnt=None, i=0):
        super().__init__(wdt, hgt - 100, parnt, i)
        self.setWindowTitle('Тест на определение языка программирования')
        self.set_icon()
        self.unanswered_questions = []
        self.is_initial_screen = True
        self.warning_shown = False
        
        com_text = (
            '<div style="text-align: center; padding: 20px;">'
            '<h2 style="color: #2c3e50; margin-bottom: 20px;">Тест на определение языка программирования</h2>'
            '<p style="color: #34495e; font-size: 14px; line-height: 1.6;">'
            'Этот тест поможет определить, какой язык программирования<br>'
            'лучше всего подходит для ваших целей и предпочтений.'
            '</p>'
            '<p style="color: #7f8c8d; margin-top: 20px;">'
            '<b>Нажмите "Далее", чтобы начать тест</b><br>'
            '<b>Нажмите "Выход", чтобы вернуться в главное меню</b>'
            '</p>'
            '</div>'
        )
        self.main_label.setText(com_text)
    
    # Установка иконки для окна теста
    def set_icon(self):
        try:
            icon = QIcon("icons/programming.png")
            self.setWindowIcon(icon)
        except Exception as e:
            print(f"Ошибка при загрузке иконки: {e}")

    # Отображение текущего вопроса
    def _show_question(self):
        if self.i < len(LANGUAGE_QUESTIONS):
            self.is_initial_screen = False
            self.warning_shown = False
            question_data = LANGUAGE_QUESTIONS[self.i]
            self.main_label.setText(question_data['question'])
            answers = question_data["answers"]

            for button in self.ans_buttons:
                button.hide()
                button.setAutoExclusive(False)
                button.setChecked(False)
                button.setAutoExclusive(True)

            for j, answer in enumerate(answers):
                self.ans_buttons[j].setText(answer)
                self.ans_buttons[j].show()
                
        else:
            for button in self.ans_buttons:
                button.hide()
                button.setChecked(False)
            self.calc_results()

    # Обработка нажатия кнопки "Далее"
    def nextbtn_clicked(self):
        if self.is_initial_screen:
            self.i = 0
            self._show_question()
            return
            
        if self.i >= len(LANGUAGE_QUESTIONS):
            return
            
        answer_selected = any(button.isChecked() for button in self.ans_buttons)
        
        if not answer_selected and not self.warning_shown:
            QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста, выберите один из вариантов ответа!')
            self.warning_shown = True
            if self.i not in self.unanswered_questions:
                self.unanswered_questions.append(self.i)
            return
        
        for j, button in enumerate(self.ans_buttons):
            if button.isChecked():
                self.us_answers[self.i] = LANGUAGE_QUESTIONS[self.i]["answers"][j]
                if self.i in self.unanswered_questions:
                    self.unanswered_questions.remove(self.i)
                break
            
        self.i += 1
        self._show_question()

    # Расчет результатов теста
    def calc_results(self):
        self.result = {'C#': 0, 'Python': 0, 'JavaScript': 0, 'Java': 0}
        for q_i, answer in self.us_answers.items():
            try:
                weights = LANGUAGE_QUESTIONS[q_i]["weights"][answer]
                for lang in weights:
                    self.result[lang] += 1
            except KeyError as e:
                print(f"Ошибка: Не найден ключ '{answer}' для вопроса {q_i}.")
                print("Убедитесь, что этот ответ правильно указан в QUESTIONS.")
                print(f"Детали ошибки: {e}")
                return
            except IndexError as e:
                print(f"Ошибка: Некорректный индекс вопроса: {q_i}")
                print("Убедитесь, что question_index находится в пределах допустимых значений.")
                print(f"Детали ошибки: {e}")
                return
            
        self.txt_results()
        self.nextbtn.hide()

    # Форматирование и отображение результатов теста
    def txt_results(self):
        results_string = '<b>Результаты теста</b><br><br>'
        
        if not self.us_answers:
            results_string += '<b>Вы не ответили ни на один вопрос!</b><br>'
            results_string += 'Попробуйте пройти тест еще раз и ответить на все вопросы.'
            self.main_label.setText(results_string)
            return
        
        max_score = max(self.result.values())
        
        max_languages = [lang for lang, score in self.result.items() if score == max_score]
        
        if len(max_languages) == 1:
            lang_info = LANGUAGE_DESCRIPTIONS[max_languages[0]]
            results_string += f'<b>{lang_info["title"]}</b><br>'
            results_string += lang_info["description"].replace('\n', '<br>')
        else:
            results_string += f'<b>Вам подходят следующие языки программирования:</b><br><br>'
            for lang in max_languages:
                lang_info = LANGUAGE_DESCRIPTIONS[lang]
                results_string += f'<b>{lang_info["title"]}</b><br>'
                results_string += lang_info["description"].replace('\n', '<br>')
                results_string += '<br><br>'
        
        results_string += '<br><br><b>Статистика по всем языкам:</b><br>'
        for lang, score in sorted(self.result.items(), key=lambda x: x[1], reverse=True):
            results_string += f'• {lang}: {score} баллов<br>'
        
        if self.unanswered_questions:
            results_string += '<br><b>Внимание!</b> Вы не ответили на следующие вопросы:<br>'
            for q_num in self.unanswered_questions:
                results_string += f'• Вопрос {q_num + 1}: {LANGUAGE_QUESTIONS[q_num]["question"]}<br>'
            
        self.main_label.setText(results_string)
        