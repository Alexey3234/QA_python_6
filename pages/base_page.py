from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class BasePage:
    def __init__(self, driver):
        self.driver = driver
    
    def click(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
    
    def send_keys(self, locator, text, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator))
        element.send_keys(text)
    
    def get_text(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator))
        return element.text
    
    def is_element_visible(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator))
            return True
        except:
            return False