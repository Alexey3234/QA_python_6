import sys
import os
import pytest
import allure
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.data import QUESTIONS_DATA
from helpers import QuestionHelpers


@allure.feature('Раздел "Вопросы о важном"')
class TestQuestionsSection:
    
    @allure.step('Прокрутить к разделу вопросов')
    def scroll_to_questions(self, main_page):
        main_page.scroll_to_questions_section()

    @allure.story('Проверка ответов на вопросы')
    @allure.title('Проверка ответа для вопроса №{question_index}')
    @pytest.mark.parametrize("question_index, expected_answer", QUESTIONS_DATA)
    def test_question_displays_correct_answer(self, main_page, question_index, expected_answer):
        with allure.step('Прокрутить к разделу вопросов'):
            self.scroll_to_questions(main_page)
        
        with allure.step(f'Найти и кликнуть на вопрос №{question_index}'):
            main_page.click_question(question_index)
        
        with allure.step('Проверить отображение правильного ответа'):
            answer_text = main_page.get_answer_text(question_index)
            assert answer_text == expected_answer, \
                f"Ожидался текст: '{expected_answer}', получен: '{answer_text}'"

    @allure.story('Проверка состояния по умолчанию')
    @allure.title('Проверка, что все ответы свернуты по умолчанию')
    def test_all_questions_collapsed_by_default(self, main_page):
        with allure.step('Прокрутить к разделу вопросов'):
            self.scroll_to_questions(main_page)
        
        with allure.step('Проверить все ответы'):
            assert QuestionHelpers.verify_all_answers_collapsed(main_page), "Ответы должны быть свернуты по умолчанию"

    @allure.story('Проверка поведения аккордеона')
    @allure.title('Проверка переключения между вопросами')
    def test_answer_toggle_behavior(self, main_page):
        with allure.step('Прокрутить к разделу вопросов'):
            self.scroll_to_questions(main_page)
    
        with allure.step('Проверить переключение между вопросами 0 и 1'):
            main_page.click_question(0)
            assert QuestionHelpers.verify_only_one_answer_visible(main_page, 0), "Должен быть видим только ответ 0"
    
        with allure.step('Проверить переключение на вопрос 1'):
            main_page.click_question(1)
            assert QuestionHelpers.verify_only_one_answer_visible(main_page, 1), "Должен быть видим только ответ 1"