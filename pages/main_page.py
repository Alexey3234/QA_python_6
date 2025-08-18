import sys
from pathlib import Path
import allure
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from pages.base_page import BasePage
from pages.locators import MainPageLocators

class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = MainPageLocators()
    
    @allure.step("Открыть главную страницу")
    def open(self):
        self.get_url("https://qa-scooter.praktikum-services.ru/")
        return self
    
    @allure.step("Закрыть куки-баннер")
    def close_cookie_banner(self):
        try:
            if self.is_element_visible(self.locators.COOKIE_BANNER):
                self.click(self.locators.COOKIE_BANNER)
                return True
        except:
            return False
    
    @allure.step("Нажать кнопку 'Заказать' в хедере")
    def click_order_button_header(self):
        self.click(self.locators.ORDER_BUTTON_HEADER)
    
    @allure.step("Нажать кнопку 'Заказать' в футере")
    def click_order_button_footer(self, timeout=20):
        self.wait_for_presence(self.locators.ORDER_BUTTON_FOOTER, timeout)
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.safe_click(self.locators.ORDER_BUTTON_FOOTER, timeout)
    
    @allure.step("Нажать логотип 'Самокат'")
    def click_scooter_logo(self):
        self.click(self.locators.SCOOTER_LOGO)
    
    @allure.step("Нажать логотип 'Яндекс'")
    def click_yandex_logo(self):
        self.click(self.locators.YANDEX_LOGO)
        self.switch_to_new_window()

    @allure.step("Закрыть текущее окно и вернуться")
    def close_current_window(self):
        if self.get_windows_count() > 1:
            self.close_window()
            self.switch_to_window_by_index(0)
            return True
        return False

    @allure.step("Кликнуть на вопрос с индексом {question_index}")
    def click_question(self, question_index):
        locator = self.locators.question_by_index(question_index)
        self.scroll_to_locator(locator)
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
        return all(not self.is_element_visible(answer) for answer in answers)

    @allure.step("Прокрутить к разделу вопросов")
    def scroll_to_questions_section(self):
        self.scroll_to_locator(self.locators.QUESTIONS_SECTION)

    @allure.step("Проверить, что открыта главная страница")
    def is_main_page_opened(self):
        return self.is_element_visible(self.locators.MAIN_PAGE_IDENTIFIER)

    @allure.step("Проверить, что открыта страница Dzen")
    def is_dzen_page_opened(self):
        return self.wait_for_url_contains("dzen.ru")