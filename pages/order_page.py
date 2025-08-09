import sys
import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.locators import OrderPageLocators

class OrderPage:
    def __init__(self, driver):
        self.driver = driver
        self.locators = OrderPageLocators()
    
    def fill_customer_info(self, name, lastname, address, metro_station, phone):
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.locators.NAME_INPUT)
        ).send_keys(name)
        
        self.driver.find_element(*self.locators.LASTNAME_INPUT).send_keys(lastname)
        self.driver.find_element(*self.locators.ADDRESS_INPUT).send_keys(address)
        
        metro_input = self.driver.find_element(*self.locators.METRO_INPUT)
        metro_input.click()
        
        stations = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located(self.locators.METRO_STATION)
        )
        stations[metro_station].click()
        
        self.driver.find_element(*self.locators.PHONE_INPUT).send_keys(phone)
    
    def fill_rent_info(self, date, period, color, comment):
        date_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.locators.DATE_INPUT)
        )
        date_input.clear()
        date_input.send_keys(date)
        
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.locators.RENTAL_PERIOD)
        )
        dropdown.click()
        
        periods = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located(self.locators.PERIOD_OPTION)
        )
        periods[period].click()
        
        if color is not None:
            colors = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located(self.locators.COLOR_CHECKBOX)
            )
            colors[color].click()
        
        if comment:
            comment_input = self.driver.find_element(*self.locators.COMMENT_INPUT)
            comment_input.send_keys(comment)
        
        order_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.locators.ORDER_BUTTON)
        )
        order_button.click()
        
        confirm_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.locators.CONFIRM_BUTTON)
        )
        confirm_button.click()
    
    def is_order_created(self):
        try:
            return WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(self.locators.SUCCESS_MESSAGE)
            ).is_displayed()
        except:
            return False