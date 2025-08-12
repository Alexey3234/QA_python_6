from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import allure
from selenium.webdriver.common.action_chains import ActionChains
from .locators import BaseLocators

class BasePage:
    def __init__(self, driver):
        self.driver = driver
    
    @allure.step("Кликнуть на элемент {locator}")
    def click(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
    
    @allure.step("Ввести текст '{text}' в элемент {locator}")
    def send_keys(self, locator, text, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator))
        element.send_keys(text)
    
    @allure.step("Получить текст из элемента {locator}")
    def get_text(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator))
        return element.text
    
    @allure.step("Проверить видимость элемента {locator}")
    def is_element_visible(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator))
            return True
        except:
            return False
    
    @allure.step("Проверить текущий URL")
    def is_current_url(self, expected_url, timeout=10):
        """Проверяет, что текущий URL соответствует ожидаемому"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.current_url == expected_url
            )
            return True
        except:
            return False
    
    @allure.step("Кликнуть станцию метро (индекс {station_index})")
    def click_metro_station(self, stations_locator, station_index, timeout=10):
        stations = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_all_elements_located(stations_locator))
        stations[station_index].click()
    
    @allure.step("Выбрать период аренды (индекс {period_index})")
    def select_rental_period(self, dropdown_locator, options_locator, period_index, timeout=10):
        self.click(dropdown_locator)
        periods = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_all_elements_located(options_locator))
        periods[period_index].click()
    
    @allure.step("Выбрать цвет самоката (индекс {color_index})")
    def select_scooter_color(self, checkboxes_locator, color_index, timeout=10):
        colors = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_all_elements_located(checkboxes_locator))
        colors[color_index].click()
    
    @allure.step("Очистить и ввести дату '{date}'")
    def clear_and_enter_date(self, locator, date, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator))
        element.clear()
        element.send_keys(date)
    
    @allure.step("Подтвердить заказ")
    def confirm_order(self, button_locator, timeout=15):
        self.click(button_locator, timeout)

    @allure.step("Прокрутить к элементу {locator}")
    def scroll_to_element(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        WebDriverWait(self.driver, 5).until(
            lambda d: element.location_once_scrolled_into_view['y'] < 100)
        return element

    @allure.step("Ожидание URL содержащего {url_part}")
    def wait_for_url_contains(self, url_part, timeout=15):
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(url_part))

    @allure.step("Переключение на новую вкладку")
    def switch_to_new_window(self, timeout=15):
        WebDriverWait(self.driver, timeout).until(
            lambda d: len(d.window_handles) > 1)
        self.driver.switch_to.window(self.driver.window_handles[1])

    @allure.step("Закрыть datepicker")
    def close_datepicker(self, body_locator=None):
        try:
            if body_locator:
                body = self.driver.find_element(*body_locator)
                ActionChains(self.driver).move_to_element(body).click().perform()
            
            self.driver.execute_script("""
                document.querySelectorAll('.react-datepicker').forEach(el => {
                    el.style.display = 'none';
                });
            """)
        except:
            pass

    @allure.step("Безопасный клик на элемент {locator}")
    def safe_click(self, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            self.click(locator, timeout)
        except:
            element = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Проверить, что элемент {locator} невидим")
    def is_element_not_visible(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator))
            return True
        except:
            return False

    @allure.step("Получить список элементов {locator}")
    def get_elements(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator))

    @allure.step("Ожидание появления элемента {locator}")
    def wait_for_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator))

    @allure.step("Ожидание кликабельности элемента {locator}")
    def wait_for_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator))
    
    @allure.step("Закрыть куки-баннер")
    def close_cookie_banner(self, timeout=5):
        try:
            # Используем локатор из BaseLocators вместо жестко заданного
            if self.is_element_visible(BaseLocators.COOKIE_BANNER, timeout):
                self.click(BaseLocators.COOKIE_BANNER)
                return True
        except Exception as e:
            allure.attach(f"Ошибка при закрытии куки-баннера: {str(e)}", name="cookie_banner_error")
            pass
        return False