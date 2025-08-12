import sys
import os
import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.locators import OrderPageLocators
from pages.base_page import BasePage

class OrderPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = OrderPageLocators()
    
    @allure.step("Заполнить информацию о клиенте")
    def fill_customer_info(self, name, lastname, address, metro_station, phone):
        self.send_keys(self.locators.NAME_INPUT, name, timeout=20)
        self.send_keys(self.locators.LASTNAME_INPUT, lastname)
        self.send_keys(self.locators.ADDRESS_INPUT, address)
        self.safe_click(self.locators.METRO_INPUT)
        self.click_metro_station(self.locators.METRO_STATION, metro_station)
        self.send_keys(self.locators.PHONE_INPUT, phone)

    @allure.step("Нажать кнопку 'Далее'")
    def click_next_button(self):
        self.safe_click(self.locators.NEXT_BUTTON, timeout=20)

    @allure.step("Установить дату доставки: {date}")
    def set_delivery_date(self, date):
        self.close_datepicker()
        element = self.wait_for_clickable(self.locators.DATE_INPUT, timeout=20)
        element.clear()
        element.send_keys(date)
        self.close_datepicker()

    @allure.step("Выбрать период аренды: {period_index}")
    def select_rental_period(self, period_index):
        self.close_datepicker()
        self.safe_click(self.locators.RENTAL_PERIOD, timeout=20)
        periods = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_all_elements_located(self.locators.PERIOD_OPTION)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", periods[period_index])
        self.driver.execute_script("arguments[0].click();", periods[period_index])

    @allure.step("Выбрать цвет самоката: {color_index}")
    def select_scooter_color(self, color_index):
        colors = self.get_elements(self.locators.COLOR_CHECKBOX, timeout=20)
        self.driver.execute_script("arguments[0].click();", colors[color_index])

    @allure.step("Добавить комментарий: {comment}")
    def add_comment(self, comment):
        self.send_keys(self.locators.COMMENT_INPUT, comment)

    @allure.step("Подтвердить заказ")
    def confirm_order(self):
        self.safe_click(self.locators.ORDER_BUTTON, timeout=20)
        self.safe_click(self.locators.CONFIRM_BUTTON, timeout=20)

    @allure.step("Проверить создание заказа")
    def is_order_created(self):
        return self.is_element_visible(self.locators.SUCCESS_MESSAGE, timeout=20)