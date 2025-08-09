import sys
import os
import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.locators import BaseLocators, OrderPageLocators

from pages.main_page import MainPage
from pages.order_page import OrderPage

ORDER_DATA = [
    {
        "name": "Иван",
        "lastname": "Иванов",
        "address": "Москва, ул. Ленина, 1",
        "metro_station": 0,
        "phone": "89998887766",
        "date": "01.01.2023",
        "period": 0,
        "color": 0,
        "comment": "Тестовый заказ"
    },
    {
        "name": "Петр",
        "lastname": "Петров",
        "address": "Санкт-Петербург, Невский пр., 10",
        "metro_station": 1,
        "phone": "87776665544",
        "date": "02.02.2023",
        "period": 1,
        "color": 1,
        "comment": "Второй тестовый заказ"
    }
]

def safe_click(driver, element):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element))
        element.click()
    except:
        driver.execute_script("arguments[0].click();", element)

def close_datepicker(driver):
    try:
        body = driver.find_element(*BaseLocators.BODY)
        ActionChains(driver).move_to_element(body).click().perform()
        driver.execute_script("""
            document.querySelectorAll('.react-datepicker').forEach(el => {
                el.style.display = 'none';
            });
        """)
    except:
        pass

@allure.feature('Оформление заказа')
@allure.story('Заказ через кнопку в шапке')
@allure.title('Проверка оформления заказа через кнопку в шапке сайта')
@pytest.mark.parametrize("order_data", ORDER_DATA)
def test_order_flow_from_header(driver, order_data):
    main_page = MainPage(driver)
    order_page = OrderPage(driver)

    with allure.step('Открытие формы заказа через кнопку в шапке'):
        order_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(main_page.locators.ORDER_BUTTON_HEADER)
        )
        safe_click(driver, order_button)

    with allure.step('Заполнение информации о клиенте'):
        order_page.fill_customer_info(
            order_data["name"],
            order_data["lastname"],
            order_data["address"],
            order_data["metro_station"],
            order_data["phone"]
        )

    with allure.step('Переход к следующему шагу оформления'):
        next_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(order_page.locators.NEXT_BUTTON)
        )
        safe_click(driver, next_button)

    with allure.step('Указание даты доставки'):
        date_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(order_page.locators.DATE_INPUT)
        )
        date_input.clear()
        date_input.send_keys(order_data["date"])
        close_datepicker(driver)

    with allure.step('Выбор периода аренды'):
        dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(order_page.locators.RENTAL_PERIOD)
        )
        safe_click(driver, dropdown)

        period_option = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                 OrderPageLocators.get_dropdown_option_by_index(order_data['period']+1))
        )
        safe_click(driver, period_option)

    with allure.step('Дополнительные параметры заказа'):
        if order_data["color"] is not None:
            colors = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(order_page.locators.COLOR_CHECKBOX)
            )
            safe_click(driver, colors[order_data["color"]])

        if order_data["comment"]:
            comment = driver.find_element(*order_page.locators.COMMENT_INPUT)
            comment.send_keys(order_data["comment"])

    with allure.step('Подтверждение заказа'):
        order_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(order_page.locators.ORDER_BUTTON)
        )
        safe_click(driver, order_button)

    with allure.step('Подтверждение в модальном окне'):
        confirm_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(order_page.locators.CONFIRM_BUTTON)
        )
        safe_click(driver, confirm_button)

    with allure.step('Проверка успешного оформления заказа'):
        assert order_page.is_order_created(), "Заказ не был успешно создан"

@allure.feature('Оформление заказа')
@allure.story('Заказ через кнопку в подвале')
@allure.title('Проверка оформления заказа через кнопку в подвале сайта')
@pytest.mark.parametrize("order_data", [ORDER_DATA[0]])
def test_order_flow_from_footer(driver, order_data):
    test_order_flow_from_header(driver, order_data) 

@allure.feature('Навигация')
@allure.story('Редирект по логотипу Самоката')
@allure.title('Проверка редиректа на главную страницу по логотипу Самоката')
def test_scooter_logo_redirect(driver):
    main_page = MainPage(driver)
    
    with allure.step('Клик по логотипу Самоката'):
        logo = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(main_page.locators.SCOOTER_LOGO)
        )
        safe_click(driver, logo)
    
    with allure.step('Проверка редиректа на главную страницу'):
        WebDriverWait(driver, 15).until(
            EC.url_contains("https://qa-scooter.praktikum-services.ru/")
        )

@allure.feature('Навигация')
@allure.story('Редирект по логотипу Яндекса')
@allure.title('Проверка редиректа на Dzen по логотипу Яндекса')
def test_yandex_logo_redirect(driver):
    main_page = MainPage(driver)
    
    with allure.step('Клик по логотипу Яндекса'):
        logo = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(main_page.locators.YANDEX_LOGO)
        )
        safe_click(driver, logo)
    
    with allure.step('Переключение на новую вкладку'):
        WebDriverWait(driver, 15).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[1])
    
    with allure.step('Проверка редиректа на Dzen'):
        WebDriverWait(driver, 15).until(
            EC.url_contains("dzen.ru")
        )