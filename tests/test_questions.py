import sys
import os
import pytest
import allure
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.main_page import MainPage
from pages.base_page import BasePage


@allure.feature('Раздел "Вопросы о важном"')
class TestQuestionsSection:
    
    QUESTIONS_DATA = [
        (0, "Сутки — 400 рублей. Оплата курьеру — наличными или картой."),
        (1, "Пока что у нас так: один заказ — один самокат. Если хотите покататься с друзьями, можете просто сделать несколько заказов — один за другим."),
        (2, "Допустим, вы оформляете заказ на 8 мая. Мы привозим самокат 8 мая в течение дня. Отсчёт времени аренды начинается с момента, когда вы оплатите заказ курьеру. Если мы привезли самокат 8 мая в 20:30, суточная аренда закончится 9 мая в 20:30."),
        (3, "Только начиная с завтрашнего дня. Но скоро станем расторопнее."),
        (4, "Пока что нет! Но если что-то срочное — всегда можно позвонить в поддержку по красивому номеру 1010."),
        (5, "Самокат приезжает к вам с полной зарядкой. Этого хватает на восемь суток — даже если будете кататься без передышек и во сне. Зарядка не понадобится."),
        (6, "Да, пока самокат не привезли. Штрафа не будет, объяснительной записки тоже не попросим. Все же свои."),
        (7, "Да, обязательно. Всем самокатов! И Москве, и Московской области.")
    ]

    @allure.step('Прокрутить к разделу вопросов')
    def scroll_to_questions(self, driver):
        main_page = MainPage(driver)
        main_page.scroll_to_questions_section()

    @allure.story('Проверка ответов на вопросы')
    @allure.title('Проверка ответа для вопроса №{question_index}')
    @pytest.mark.parametrize("question_index, expected_answer", QUESTIONS_DATA)
    def test_question_displays_correct_answer(self, driver, question_index, expected_answer):
        main_page = MainPage(driver)

        with allure.step('Прокрутить к разделу вопросов'):
            self.scroll_to_questions(driver)
        
        with allure.step(f'Найти и кликнуть на вопрос №{question_index}'):
            main_page.click_question(question_index)
        
        with allure.step('Проверить отображение правильного ответа'):
            answer_text = main_page.get_answer_text(question_index)
            assert answer_text == expected_answer, \
                f"Ожидался текст: '{expected_answer}', получен: '{answer_text}'"

    @allure.story('Проверка состояния по умолчанию')
    @allure.title('Проверка, что все ответы свернуты по умолчанию')
    def test_all_questions_collapsed_by_default(self, driver):
        main_page = MainPage(driver)

        with allure.step('Прокрутить к разделу вопросов'):
            self.scroll_to_questions(driver)
        
        with allure.step('Проверить все ответы'):
            assert main_page.are_all_answers_collapsed(), "Ответы должны быть свернуты по умолчанию"

    @allure.story('Проверка поведения аккордеона')
    @allure.title('Проверка переключения между вопросами')
    def test_answer_toggle_behavior(self, driver):
        main_page = MainPage(driver)

        with allure.step('Прокрутить к разделу вопросов'):
            self.scroll_to_questions(driver)
        
        with allure.step('Проверить переключение между вопросами 0 и 1'):
            main_page.click_question(0)
            assert main_page.is_answer_visible(0), "Ответ 0 должен быть видим после клика"
            
            for i in range(1, 8):
                assert not main_page.is_answer_visible(i), f"Ответ {i} не должен быть видим"
        
        with allure.step('Проверить переключение на вопрос 1'):
            main_page.click_question(1)
            assert main_page.is_answer_visible(1), "Ответ 1 должен быть видим после клика"
            assert not main_page.is_answer_visible(0), "Ответ 0 должен быть скрыт"