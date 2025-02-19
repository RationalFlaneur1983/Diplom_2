import requests
import allure
from api.endpoints import Endpoints
from helpers.user_helpers import UserRegistration
from helpers.order_helpers import OrderHelpers


class TestCreateOrder:

    url = Endpoints.POST_CREATE_ORDER_ENDPOINT

    @allure.title('Успешное создание заказа с авторизацией и ингредиентами')
    def test_valid_order_created(self, registered_user):
        headers = {'Authorization': registered_user['access_token']}
        payload = {'ingredients': OrderHelpers.generate_ingredient_list()}
        response = requests.post(self.url, headers=headers, json=payload)

        assert response.status_code == 200

    @allure.title('Успешное создание заказа без авторизации и с ингредиентами')
    def test_valid_order_created_not_authorized(self):
        headers = {'Authorization': None}
        payload = {'ingredients': OrderHelpers.generate_ingredient_list()}
        response = requests.post(self.url, headers=headers, json=payload)

        assert response.status_code == 200

    @allure.title('Неуспешное создание заказа без ингредиентов')
    def test_invalid_create_order_without_ingredients_(self, registered_user):
        headers = {'Authorization': registered_user['access_token']}
        payload = {'ingredients': None}
        response = requests.post(self.url, headers=headers, json=payload)

        assert response.status_code == 400

    @allure.title('Неуспешное создание заказа с неверным хешем ингредиентов')
    def test_invalid_create_order_wrong_ingredient_hash(self, registered_user):
        headers = {'Authorization': registered_user['access_token']}
        payload = {'ingredients': OrderHelpers.generate_random_string()}
        response = requests.post(self.url, headers=headers, json=payload)

        assert response.status_code == 500


class TestGetOrders:

    url = Endpoints.GET_USER_ORDERS_ENDPOINT

    @allure.title('Получение заказов неавторизованного пользователя')
    def test_invalid_get_unauthorized_user_order(self):
        headers = {'Authorization': None}
        response = requests.get(self.url, headers=headers)

        assert response.status_code == 401

    @allure.title('Получение заказов авторизованного пользователя')
    def test_valid_get_unauthorized_user_order(self, registered_user):
        headers = {'Authorization': registered_user['access_token']}
        response = requests.get(self.url, headers=headers)

        assert response.status_code == 200