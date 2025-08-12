from selenium.webdriver.common.by import By

class MainPageLocators:
    # Локаторы для главной страницы
    ORDER_BUTTON_HEADER = (By.XPATH, "//button[contains(@class, 'Button_Button__ra12g')]")
    ORDER_BUTTON_FOOTER = (By.XPATH, "(//button[contains(text(), 'Заказать')])[2]")
    QUESTIONS_SECTION = (By.XPATH, "//div[contains(text(), 'Вопросы о важном')]")
    QUESTION_ITEMS = (By.XPATH, "//div[@class='accordion__item']")
    QUESTION = (By.XPATH, ".//div[contains(@class, 'accordion__button')]")
    ANSWER = (By.XPATH, ".//div[contains(@class, 'accordion__panel')]")
    SCOOTER_LOGO = (By.XPATH, "//a[@class='Header_LogoScooter__3lsAR']")
    YANDEX_LOGO = (By.XPATH, "//a[@class='Header_LogoYandex__3TSOI']")
    QUESTION_HEADER = (By.CSS_SELECTOR, "[data-accordion-component='AccordionItemButton']")
    QUESTION_PANEL = (By.CSS_SELECTOR, "[data-accordion-component='AccordionItemPanel']")
    @staticmethod
    def question_by_index(index):
        return (By.ID, f"accordion__heading-{index}")
    
    @staticmethod
    def answer_by_index(index):
        return (By.ID, f"accordion__panel-{index}")

class OrderPageLocators:
    # Локаторы для страницы заказа
    NAME_INPUT = (By.XPATH, "//input[@placeholder='* Имя']")
    LASTNAME_INPUT = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS_INPUT = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_INPUT = (By.XPATH, "//input[@placeholder='* Станция метро']")
    METRO_STATION = (By.XPATH, "//div[@class='select-search__select']//li")
    PHONE_INPUT = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.XPATH, "//button[contains(text(), 'Далее')]")
    DATE_INPUT = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    RENTAL_PERIOD = (By.XPATH, "//div[contains(@class, 'Dropdown-root')]")
    PERIOD_OPTION = (By.XPATH, "//div[contains(@class, 'Dropdown-option')]")
    COLOR_CHECKBOX = (By.XPATH, "//input[@type='checkbox']")
    COMMENT_INPUT = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
    ORDER_BUTTON = (By.XPATH, "//button[contains(@class, 'Button_Middle') and text()='Заказать']")
    CONFIRM_BUTTON = (By.XPATH, "//button[text()='Да' and contains(@class, 'Button_Middle')]")
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class, 'Order_ModalHeader')]")
    DROPDOWN_OPTION = (By.XPATH, "//div[@class='Dropdown-option']")
    @staticmethod
    def get_dropdown_option_by_index(index):
        return (By.XPATH, f"//div[@class='Dropdown-option'][{index}]")
    
class BaseLocators:
    BODY = (By.TAG_NAME, 'body')
    COOKIE_BANNER = (By.ID, "rcc-confirm-button")
    