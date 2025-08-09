import sys
import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.locators import MainPageLocators

class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.locators = MainPageLocators
    
    def click_order_button_header(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.locators.ORDER_BUTTON_HEADER)
        ).click()
    
    def click_order_button_footer(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.locators.ORDER_BUTTON_FOOTER)
        ).click()
    
    def click_scooter_logo(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.locators.SCOOTER_LOGO)
        ).click()
    
    def click_yandex_logo(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.locators.YANDEX_LOGO)
        ).click()