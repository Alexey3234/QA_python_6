from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import allure


class BasePage:
    def __init__(self, driver):
        """Инициализация базовой страницы"""
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout=10)

    # Основные методы взаимодействия
    @allure.step("Кликнуть на элемент")
    def click(self, locator, timeout=10):
        """Клик по элементу с ожиданием кликабельности"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    @allure.step("Безопасный клик на элемент")
    def safe_click(self, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            self.click(locator, timeout)
        except:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator))
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Ввести текст в элемент")
    def send_keys(self, locator, text, timeout=10):
        """Ввод текста с очисткой поля"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    @allure.step("Очистить и ввести текст")
    def clear_and_send_keys(self, locator, text, timeout=10):
        """Явная очистка и ввод текста"""
        element = self.wait_for_clickable(locator, timeout)
        element.clear()
        element.send_keys(text)

    @allure.step("Получить текст из элемента")
    def get_text(self, locator, timeout=10):
        """Получение текста элемента"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator))
        return element.text

    @allure.step("Получить значение атрибута элемента")
    def get_attribute(self, locator, attribute, timeout=10):
        """Получение значения атрибута"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator))
        return element.get_attribute(attribute)

    @allure.step("Получить список элементов")
    def get_elements(self, locator, timeout=10):
        """Получение списка элементов"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator))

    @allure.step("Проверить видимость элемента")
    def is_element_visible(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @allure.step("Проверить, что элемент невидим")
    def is_element_not_visible(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator))
            return True
        except:
            return False

    @allure.step("Проверить наличие элемента")
    def is_element_present(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator))
            return True
        except:
            return False

    @allure.step("Проверить текущий URL")
    def is_current_url(self, expected_url, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.current_url == expected_url
            )
            return True
        except:
            return False

    @allure.step("Ожидание появления элемента")
    def wait_for_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator))

    @allure.step("Ожидание кликабельности элемента")
    def wait_for_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator))

    @allure.step("Ожидание видимости элемента")
    def wait_for_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator))

    @allure.step("Ожидание URL содержащего часть")
    def wait_for_url_contains(self, url_part, timeout=15):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains(url_part))
            return True
        except:
            return False

    # Методы навигации
    @allure.step("Переключение на новую вкладку")
    def switch_to_new_window(self, timeout=15):
        WebDriverWait(self.driver, timeout).until(
            lambda d: len(d.window_handles) > 1)
        self.driver.switch_to.window(self.driver.window_handles[-1])

    @allure.step("Переключиться на окно по индексу")
    def switch_to_window_by_index(self, index):
        if len(self.driver.window_handles) > index:
            self.driver.switch_to.window(self.driver.window_handles[index])
            return True
        return False

    @allure.step("Закрыть текущее окно и вернуться")
    def close_current_window(self):
        if len(self.driver.window_handles) > 1:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            return True
        return False

    @allure.step("Прокрутить к элементу (по локатору)")
    def scroll_to_locator(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return element

    @allure.step("Прокрутить к элементу (WebElement)")
    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    @allure.step("Навести курсор на элемент")
    def hover_to_element(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator))
        ActionChains(self.driver).move_to_element(element).perform()

    @allure.step("Принять alert")
    def accept_alert(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.accept()

    @allure.step("Отклонить alert")
    def dismiss_alert(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.dismiss()

    @allure.step("Закрыть datepicker")
    def close_datepicker(self):
        try:
            self.driver.execute_script("""
                document.querySelectorAll('.react-datepicker').forEach(el => {
                    el.style.display = 'none';
                });
            """)
        except:
            pass

    @allure.step("Получить текущий URL")
    def get_current_url(self):
        return self.driver.current_url

    @allure.step("Обновить страницу")
    def refresh_page(self):
        self.driver.refresh()