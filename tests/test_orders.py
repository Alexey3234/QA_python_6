import sys
import os
import pytest
import allure

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.data import ORDER_DATA


class TestOrderFlow:
    @allure.feature('Оформление заказа')
    @allure.story('Заказ через кнопку в шапке')
    @allure.title('Проверка оформления заказа через кнопку в шапке сайта')
    @pytest.mark.parametrize("order_data", ORDER_DATA)
    def test_order_flow_from_header(self, main_page, order_page, order_data):
        with allure.step('Открытие формы заказа через кнопку в шапке'):
            main_page.click_order_button_header()

        with allure.step('Заполнение информации о клиенте'):
            order_page.fill_customer_info(
                name=order_data["name"],
                lastname=order_data["lastname"],
                address=order_data["address"],
                metro_station=order_data["metro_station"],
                phone=order_data["phone"]
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
    def test_order_flow_from_footer(self, main_page, order_page):
        order_data = ORDER_DATA[0]

        with allure.step('Закрытие куки-баннера, если он есть'):
            main_page.close_cookie_banner()
                
        with allure.step('Открытие формы заказа через кнопку в подвале'):
            main_page.click_order_button_footer()
            

        with allure.step('Заполнение информации о клиенте'):
            order_page.fill_customer_info(
                name=order_data["name"],
                lastname=order_data["lastname"],
                address=order_data["address"],
                metro_station=order_data["metro_station"],
                phone=order_data["phone"]
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
    def test_scooter_logo_redirect(self, main_page):
        with allure.step('Клик по логотипу Самоката'):
            main_page.click_scooter_logo()

        with allure.step('Проверка редиректа на главную страницу'):
            assert main_page.is_main_page_opened()

    @allure.feature('Навигация')
    @allure.story('Редирект по логотипу Яндекса')
    @allure.title('Проверка редиректа на Dzen по логотипу Яндекса')
    def test_yandex_logo_redirect(self, main_page):
        with allure.step('Клик по логотипу Яндекса'):
            main_page.click_yandex_logo()

        with allure.step('Переключение на новую вкладку'):
            main_page.switch_to_new_window()

        with allure.step('Проверка редиректа на Dzen'):
            assert main_page.is_dzen_page_opened()
    
        with allure.step('Закрытие новой вкладки и возврат'):
            main_page.close_current_window()
            
        with allure.step('Проверка, что вернулись на исходную страницу'):
            assert main_page.is_main_page_opened()