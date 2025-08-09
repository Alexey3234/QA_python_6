import sys
import os
import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.main_page import MainPage
from pages.locators import MainPageLocators

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
        questions_section = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(MainPageLocators.QUESTIONS_SECTION)
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", questions_section)
        WebDriverWait(driver, 5).until(
            lambda d: questions_section.location_once_scrolled_into_view['y'] < 100
        )
        return questions_section

    @allure.story('Проверка ответов на вопросы')
    @allure.title('Проверка ответа для вопроса №{question_index}')
    @pytest.mark.parametrize("question_index, expected_answer", QUESTIONS_DATA)
    def test_question_displays_correct_answer(self, driver, question_index, expected_answer):
        main_page = MainPage(driver)
        
        with allure.step('Прокрутить к разделу вопросов'):
            self.scroll_to_questions(driver)
        
        with allure.step(f'Найти и кликнуть на вопрос №{question_index}'):
            question = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(MainPageLocators.question_by_index(question_index))
            )
            question.click()
        
        with allure.step('Проверить отображение правильного ответа'):
            answer = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located(MainPageLocators.answer_by_index(question_index)),
                message=f"Ответ на вопрос {question_index} не отобразился"
            )
            assert answer.text == expected_answer, \
                f"Ожидался текст: '{expected_answer}', получен: '{answer.text}'"

    @allure.story('Проверка состояния по умолчанию')
    @allure.title('Проверка, что все ответы свернуты по умолчанию')
    def test_all_questions_collapsed_by_default(self, driver):
        main_page = MainPage(driver)
        
        with allure.step('Прокрутить к разделу вопросов'):
            self.scroll_to_questions(driver)
        
        with allure.step('Проверить все ответы'):
            all_answers = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located(MainPageLocators.QUESTION_PANEL)
            )
            
            for answer in all_answers:
                assert not answer.is_displayed(), "Ответ должен быть свернут по умолчанию"

    @allure.story('Проверка поведения аккордеона')
    @allure.title('Проверка, что одновременно раскрыт только один ответ')
    def test_only_one_answer_expanded_at_time(self, driver):
        main_page = MainPage(driver)
        
        with allure.step('Прокрутить к разделу вопросов'):
            self.scroll_to_questions(driver)
        
        with allure.step('Кликнуть на первый вопрос и проверить его ответ'):
            question1 = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(MainPageLocators.question_by_index(0))
            )
            question1.click()
            
            answer0 = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located(MainPageLocators.answer_by_index(0))
            )
            assert answer0.is_displayed(), "Первый ответ должен быть видим"
            
            for i in range(1, 8):
                answer = driver.find_element(*MainPageLocators.answer_by_index(i))
                assert not answer.is_displayed(), f"Ответ {i} не должен быть видим"
        
        with allure.step('Кликнуть на второй вопрос и проверить переключение'):
            question2 = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(MainPageLocators.question_by_index(1))
            )
            question2.click()
            
            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element(answer0)
            )
            answer1 = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located(MainPageLocators.answer_by_index(1))
            )
            
            assert answer1.is_displayed(), "Второй ответ должен быть видим"
            assert not answer0.is_displayed(), "Первый ответ должен быть скрыт"