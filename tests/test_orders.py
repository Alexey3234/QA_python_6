import sys
import os
import pytest
import allure
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.main_page import MainPage
from pages.order_page import OrderPage
from pages.base_page import BasePage


class TestOrderFlow:
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

    @allure.feature('Оформление заказа')
    @allure.story('Заказ через кнопку в шапке')
    @allure.title('Проверка оформления заказа через кнопку в шапке сайта')
    @pytest.mark.parametrize("order_data", ORDER_DATA)
    def test_order_flow_from_header(self, driver, order_data):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)

        with allure.step('Открытие формы заказа через кнопку в шапке'):
            main_page.click_order_button_header()

        with allure.step('Заполнение информации о клиенте'):
            order_page.fill_customer_info(
                order_data["name"],
                order_data["lastname"],
                order_data["address"],
                order_data["metro_station"],
                order_data["phone"]
            )

        with allure.step('Переход к следующему шагу оформления'):
            order_page.click_next_button()

        with allure.step('Указание даты доставки'):
            order_page.set_delivery_date(order_data["date"])

        with allure.step('Выбор периода аренды'):
            order_page.select_rental_period(order_data["period"])

        with allure.step('Выбор цвета самоката'):
            order_page.select_scooter_color(order_data["color"])

        with allure.step('Добавление комментария'):
            order_page.add_comment(order_data["comment"])

        with allure.step('Подтверждение заказа'):
            order_page.confirm_order()

        with allure.step('Проверка успешного оформления заказа'):
            assert order_page.is_order_created(), "Заказ не был успешно создан"

    @allure.feature('Оформление заказа')
    @allure.story('Заказ через кнопку в подвале')
    @allure.title('Проверка оформления заказа через кнопку в подвале сайта')
    def test_order_flow_from_footer(self, driver):
        order_data = self.ORDER_DATA[0]
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        base_page = BasePage(driver)

        with allure.step('Закрытие куки-баннера, если он есть'):
            base_page.close_cookie_banner()
    
        with allure.step('Открытие формы заказа через кнопку в подвале'):
            main_page.click_order_button_footer()

        with allure.step('Заполнение информации о клиенте'):
            order_page.fill_customer_info(
                order_data["name"],
                order_data["lastname"],
                order_data["address"],
                order_data["metro_station"],
                order_data["phone"]
            )

        with allure.step('Переход к следующему шагу оформления'):
            order_page.click_next_button()

        with allure.step('Указание даты доставки'):
            order_page.set_delivery_date(order_data["date"])

        with allure.step('Выбор периода аренды'):
            order_page.select_rental_period(order_data["period"])

        with allure.step('Выбор цвета самоката'):
            order_page.select_scooter_color(order_data["color"])

        with allure.step('Добавление комментария'):
            order_page.add_comment(order_data["comment"])

        with allure.step('Подтверждение заказа'):
            order_page.confirm_order()

        with allure.step('Проверка успешного оформления заказа'):
            assert order_page.is_order_created(), "Заказ не был успешно создан"


class TestNavigation:
    @allure.feature('Навигация')
    @allure.story('Редирект по логотипу Самоката')
    @allure.title('Проверка редиректа на главную страницу по логотипу Самоката')
    def test_scooter_logo_redirect(self, driver):
        main_page = MainPage(driver)
        base_page = BasePage(driver)

        with allure.step('Клик по логотипу Самоката'):
            main_page.click_scooter_logo()

        with allure.step('Проверка редиректа на главную страницу'):
            assert base_page.is_current_url("https://qa-scooter.praktikum-services.ru/")

    @allure.feature('Навигация')
    @allure.story('Редирект по логотипу Яндекса')
    @allure.title('Проверка редиректа на Dzen по логотипу Яндекса')
    def test_yandex_logo_redirect(self, driver):
        main_page = MainPage(driver)
        base_page = BasePage(driver)

        with allure.step('Клик по логотипу Яндекса'):
            main_page.click_yandex_logo()

        with allure.step('Переключение на новую вкладку'):
            base_page.switch_to_new_window()

        with allure.step('Проверка редиректа на Dzen'):
            base_page.wait_for_url_contains("dzen.ru")
    
        with allure.step('Закрытие новой вкладки и возврат'):
            driver.close()
            driver.switch_to.window(driver.window_handles[0])