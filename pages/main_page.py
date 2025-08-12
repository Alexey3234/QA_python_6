import sys
import os
import allure

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.locators import MainPageLocators
from pages.base_page import BasePage

class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = MainPageLocators
    
    @allure.step("Нажать кнопку 'Заказать' в хедере")
    def click_order_button_header(self):
        self.click(self.locators.ORDER_BUTTON_HEADER)
    
    @allure.step("Нажать кнопку 'Заказать' в футере")
    def click_order_button_footer(self):
        self.click(self.locators.ORDER_BUTTON_FOOTER)
    
    @allure.step("Нажать логотип 'Самокат'")
    def click_scooter_logo(self):
        self.click(self.locators.SCOOTER_LOGO)
    
    @allure.step("Нажать логотип 'Яндекс'")
    def click_yandex_logo(self):
        self.click(self.locators.YANDEX_LOGO)

    @allure.step("Кликнуть на вопрос с индексом {question_index}")
    def click_question(self, question_index):
        locator = self.locators.question_by_index(question_index)
        self.click(locator, timeout=20)

    @allure.step("Получить текст ответа на вопрос {question_index}")
    def get_answer_text(self, question_index):
        locator = self.locators.answer_by_index(question_index)
        return self.get_text(locator, timeout=20)

    @allure.step("Проверить видимость ответа на вопрос {question_index}")
    def is_answer_visible(self, question_index):
        locator = self.locators.answer_by_index(question_index)
        return self.is_element_visible(locator, timeout=5)

    @allure.step("Проверить, что все ответы свернуты")
    def are_all_answers_collapsed(self):
        answers = self.get_elements(self.locators.QUESTION_PANEL, timeout=20)
        return all(not answer.is_displayed() for answer in answers)

    @allure.step("Прокрутить к разделу вопросов")
    def scroll_to_questions_section(self):
        self.scroll_to_element(self.locators.QUESTIONS_SECTION)