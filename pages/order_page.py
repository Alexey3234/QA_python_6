import allure
import sys
from pathlib import Path

current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root))

from pages.base_page import BasePage
from pages.locators import OrderPageLocators

class OrderPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = OrderPageLocators()
    
    @allure.step("Закрыть datepicker")
    def close_datepicker(self):
        try:
            self.execute_script("""
                const picker = document.querySelector('.react-datepicker');
                if (picker) picker.style.display = 'none';
            """)
        except Exception as e:
            allure.attach(f"Failed to close datepicker: {str(e)}", name="Datepicker Error")
            print(f"Не удалось закрыть datepicker: {e}")

    @allure.step("Кликнуть на элемент из списка по индексу {index}")
    def click_element_from_list(self, locator, index):
        elements = self.get_elements(locator)
        if not elements:
            raise ValueError("Список элементов пуст")
        if index < 0 or index >= len(elements):
            raise ValueError(f"Недопустимый индекс: {index}. Доступно элементов: {len(elements)}")
        
        self.scroll_to_element(elements[index])
        elements[index].click()  

    @allure.step("Заполнить информацию о клиенте")
    def fill_customer_info(self, name, lastname, address, metro_station, phone):
        self.clear_and_send_keys(self.locators.NAME_INPUT, name)
        self.clear_and_send_keys(self.locators.LASTNAME_INPUT, lastname)
        self.clear_and_send_keys(self.locators.ADDRESS_INPUT, address)
        self.safe_click(self.locators.METRO_INPUT)
        self.click_element_from_list(self.locators.METRO_STATION, metro_station)
        self.clear_and_send_keys(self.locators.PHONE_INPUT, phone)

    @allure.step("Нажать кнопку 'Далее'")
    def click_next_button(self):
        self.safe_click(self.locators.NEXT_BUTTON, timeout=15)

    @allure.step("Установить дату доставки: {date}")
    def set_delivery_date(self, date):
        self.close_datepicker()
        self.clear_and_send_keys(self.locators.DATE_INPUT, date)
        self.close_datepicker()

    @allure.step("Выбрать период аренды: {period_index}")
    def select_rental_period(self, period_index):
        self.safe_click(self.locators.RENTAL_PERIOD)
        self.click_element_from_list(self.locators.PERIOD_OPTION, period_index)

    @allure.step("Выбрать цвет самоката: {color_index}")
    def select_scooter_color(self, color_index):
        checkboxes = self.get_elements(self.locators.COLOR_CHECKBOX)
        if color_index < len(checkboxes):
            if not checkboxes[color_index].is_selected():
                checkboxes[color_index].click()

    @allure.step("Добавить комментарий: {comment}")
    def add_comment(self, comment):
        self.clear_and_send_keys(self.locators.COMMENT_INPUT, comment)

    @allure.step("Подтвердить заказ")
    def confirm_order(self):
        self.safe_click(self.locators.ORDER_BUTTON, timeout=15)
        self.wait_for_clickable(self.locators.CONFIRM_BUTTON, timeout=15).click()

    @allure.step("Проверить создание заказа")
    def is_order_created(self):
        return self.is_element_visible(self.locators.SUCCESS_MESSAGE, timeout=20)