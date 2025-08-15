import allure
from pages.base_page import BasePage
from pages.locators import OrderPageLocators
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent  # Получаем путь к корню проекта
sys.path.append(str(project_root))  # Добавляем в PYTHONPATH



class OrderPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = OrderPageLocators()
    
    @allure.step("Кликнуть на элемент из списка по индексу {index}")
    def click_element_from_list(self, locator, index):
        elements = self.get_elements(locator)
        if not elements:
            raise ValueError("Список элементов пуст")
        if index < 0 or index >= len(elements):
            raise ValueError(f"Недопустимый индекс: {index}. Доступно элементов: {len(elements)}")
        
        self.scroll_to_element(elements[index])
        self.click(elements[index])
    
    @allure.step("Заполнить информацию о клиенте")
    def fill_customer_info(self, name, lastname, address, metro_station, phone):
        self.send_keys(self.locators.NAME_INPUT, name)
        self.send_keys(self.locators.LASTNAME_INPUT, lastname)
        self.send_keys(self.locators.ADDRESS_INPUT, address)
        self.safe_click(self.locators.METRO_INPUT)
        self.click_element_from_list(self.locators.METRO_STATION, metro_station)
        self.send_keys(self.locators.PHONE_INPUT, phone)

    @allure.step("Нажать кнопку 'Далее'")
    def click_next_button(self):
        self.safe_click(self.locators.NEXT_BUTTON)

    @allure.step("Установить дату доставки: {date}")
    def set_delivery_date(self, date):
        self.close_datepicker()
        self.clear_and_send_keys(self.locators.DATE_INPUT, date)
        self.close_datepicker()

    @allure.step("Выбрать период аренды: {period_index}")
    def select_rental_period(self, period_index):
        self.close_datepicker()
        self.safe_click(self.locators.RENTAL_PERIOD)
        self.click_element_from_list(self.locators.PERIOD_OPTION, period_index)

    @allure.step("Выбрать цвет самоката: {color_index}")
    def select_scooter_color(self, color_index):
        self.click_element_from_list(self.locators.COLOR_CHECKBOX, color_index)

    @allure.step("Добавить комментарий: {comment}")
    def add_comment(self, comment):
        self.send_keys(self.locators.COMMENT_INPUT, comment)

    @allure.step("Подтвердить заказ")
    def confirm_order(self):
        self.safe_click(self.locators.ORDER_BUTTON)
        self.safe_click(self.locators.CONFIRM_BUTTON)

    @allure.step("Проверить создание заказа")
    def is_order_created(self):
        return self.is_element_visible(self.locators.SUCCESS_MESSAGE)