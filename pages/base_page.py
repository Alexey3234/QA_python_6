from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import allure

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout=10)

    @allure.step("Открыть URL {url}")
    def get_url(self, url):
        self.driver.get(url)

    @allure.step("Кликнуть на элемент")
    def click(self, locator, timeout=10):
        element = self.wait_for_clickable(locator, timeout)
        element.click()

    @allure.step("Безопасный клик на элемент")
    def safe_click(self, locator, timeout=10):
        try:
            element = self.wait_for_presence(locator, timeout)
            self.scroll_to_element(element)
            self.click(locator, timeout)
        except:
            element = self.wait_for_presence(locator, timeout)
            self.execute_script("arguments[0].click();", element)

    @allure.step("Ввести текст в элемент")
    def send_keys(self, locator, text, timeout=10):
        element = self.wait_for_visible(locator, timeout)
        element.clear()
        element.send_keys(text)

    @allure.step("Очистить и ввести текст")
    def clear_and_send_keys(self, locator, text, timeout=10):
        element = self.wait_for_clickable(locator, timeout)
        element.clear()
        element.send_keys(text)

    @allure.step("Получить текст из элемента")
    def get_text(self, locator, timeout=10):
        element = self.wait_for_visible(locator, timeout)
        return element.text

    @allure.step("Получить значение атрибута элемента")
    def get_attribute(self, locator, attribute, timeout=10):
        element = self.wait_for_presence(locator, timeout)
        return element.get_attribute(attribute)

    @allure.step("Получить список элементов")
    def get_elements(self, locator, timeout=10):
        return self.wait_for_all_elements_present(locator, timeout)

    @allure.step("Получить список окон")
    def get_window_handles(self):
        return self.driver.window_handles

    @allure.step("Получить количество окон")
    def get_windows_count(self):
        return len(self.get_window_handles())

    @allure.step("Переключиться на окно по индексу {index}")
    def switch_to_window_by_index(self, index):
        handles = self.get_window_handles()
        if index < len(handles):
            self.driver.switch_to.window(handles[index])
            return True
        return False

    @allure.step("Закрыть текущее окно")
    def close_window(self):
        self.driver.close()

    @allure.step("Ожидание нового окна")
    def wait_for_new_window(self, original_count, timeout=15):
        try:
            self.wait.until(lambda d: len(d.window_handles) > original_count)
            return True
        except:
            return False

    @allure.step("Переключение на новую вкладку")
    def switch_to_new_window(self, timeout=15):
        WebDriverWait(self.driver, timeout).until(
            lambda d: len(d.window_handles) > 1)
        self.driver.switch_to.window(self.driver.window_handles[-1])

    @allure.step("Проверить видимость элемента")
    def is_element_visible(self, locator, timeout=10):
        try:
            self.wait_for_visible(locator, timeout)
            return True
        except:
            return False

    @allure.step("Проверить видимость элементов из списка")
    def is_element_visible_from_list(self, elements):
        return all(self.is_element_visible(element) for element in elements)

    @allure.step("Проверить, что элемент невидим")
    def is_element_not_visible(self, locator, timeout=10):
        try:
            self.wait_for_invisible(locator, timeout)
            return True
        except:
            return False

    @allure.step("Проверить наличие элемента")
    def is_element_present(self, locator, timeout=10):
        try:
            self.wait_for_presence(locator, timeout)
            return True
        except:
            return False

    @allure.step("Проверить текущий URL")
    def is_current_url(self, expected_url, timeout=10):
        try:
            self.wait.until(lambda d: d.current_url == expected_url)
            return True
        except:
            return False

    @allure.step("Ожидание появления элемента")
    def wait_for_presence(self, locator, timeout=10):
        return self.wait.until(EC.presence_of_element_located(locator))

    @allure.step("Ожидание кликабельности элемента")
    def wait_for_clickable(self, locator, timeout=10):
        return self.wait.until(EC.element_to_be_clickable(locator))

    @allure.step("Ожидание видимости элемента")
    def wait_for_visible(self, locator, timeout=10):
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Ожидание невидимости элемента")
    def wait_for_invisible(self, locator, timeout=10):
        return self.wait.until(EC.invisibility_of_element_located(locator))

    @allure.step("Ожидание всех элементов")
    def wait_for_all_elements_present(self, locator, timeout=10):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    @allure.step("Ожидание URL содержащего часть")
    def wait_for_url_contains(self, url_part, timeout=15):
        try:
            self.wait.until(EC.url_contains(url_part))
            return True
        except:
            return False

    @allure.step("Прокрутить к элементу (по локатору)")
    def scroll_to_locator(self, locator, timeout=10):
        element = self.wait_for_presence(locator, timeout)
        self.execute_script("arguments[0].scrollIntoView(true);", element)
        return element

    @allure.step("Прокрутить к элементу (WebElement)")
    def scroll_to_element(self, element):
        self.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    @allure.step("Выполнить JavaScript")
    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    @allure.step("Навести курсор на элемент")
    def hover_to_element(self, locator, timeout=10):
        element = self.wait_for_presence(locator, timeout)
        ActionChains(self.driver).move_to_element(element).perform()

    @allure.step("Получить текущий URL")
    def get_current_url(self):
        return self.driver.current_url

    @allure.step("Обновить страницу")
    def refresh_page(self):
        self.driver.refresh()