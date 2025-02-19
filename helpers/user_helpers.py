import requests
import allure
from faker import Faker
from api.endpoints import Endpoints
from helpers.user_data_sets import user_data_sets


class UserRegistration:
    """Класс, содержащий помощников для тестирования манипуляций с учетной записью пользователя"""

    @staticmethod
    @allure.step('Генерация данных пользователя')
    # Принимает аргументы valid, no_mail, no_password, а без них генерирует данные через Faker
    def generate_user_data(test_type=None):
        fake = Faker()
        if test_type is None or test_type not in user_data_sets:
            return {
                'email': fake.email(),
                'password': fake.password(),
                'name': fake.name()
            }
        return user_data_sets[test_type]['data']

    @staticmethod
    @allure.step('Регистрация нового пользователя')
    def register_new_user(test_type='valid'):
        payload = UserRegistration.generate_user_data(test_type)
        response = requests.post(Endpoints.POST_USER_REGISTER_ENDPOINT, data=payload)

        assert response.status_code == 200, f"Ожидался статус код 200, но получили {response.status_code}"
        assert response.json()['success'] == True, "Регистрация пользователя не удалась"

        access_token = response.json().get('accessToken')
        return {
            'access_token': access_token,
            'payload': payload
        }


    @staticmethod
    @allure.step('Удаление пользователя')
    def delete_user(access_token):
        url = Endpoints.DELETE_USER_DATA_ENDPOINT
        headers = {'Authorization': access_token}
        response = requests.delete(url, headers=headers)
        return response


