import requests
import allure
from api.endpoints import Endpoints
from helpers.user_helpers import UserRegistration

class TestCreateUser:
    url = Endpoints.POST_USER_REGISTER_ENDPOINT

    @allure.title('Успешное создание учетной записи пользователя с корректными данными')
    def test_valid_user_registration(self):
        payload = UserRegistration.generate_user_data('valid')
        response = requests.post(self.url, data=payload)

        assert (response.status_code == 200 and response.json()['success'] == True)

        access_token = response.json().get('accessToken')
        UserRegistration.delete_user(access_token)
        

    @allure.title('Система не позволяет создать пользователя, который уже зарегистрирован')
    def test_invalid_user_registration_already_exists(self):
        payload = UserRegistration.generate_user_data('valid')
        response = requests.post(self.url, data=payload)
        response_repeat = requests.post(self.url, data=payload)

        assert (response_repeat.status_code == 403 and response_repeat.json()['success'] == False)

        access_token = response.json().get('accessToken')
        UserRegistration.delete_user(access_token)


    @allure.title('Система не позволяет создать пользователя с незаполненным полем email')
    def test_invalid_user_registration_empty_email(self):
        payload = UserRegistration.generate_user_data('no_email')
        response = requests.post(self.url, data=payload)

        assert (response.status_code == 403 and response.json()['success'] == False)


    @allure.title('Система не позволяет создать пользователя с незаполненным полем email')
    def test_invalid_user_registration_empty_password(self):
        payload = UserRegistration.generate_user_data('no_password')
        response = requests.post(self.url, data=payload)

        assert (response.status_code == 403 and response.json()['success'] == False)


class TestLoginUser:

    @allure.title('Успешная авторизация пользователя с корректными данными')
    def test_valid_user_authorization(self):
        url_register = Endpoints.POST_USER_REGISTER_ENDPOINT
        payload_register = UserRegistration.generate_user_data('valid')
        requests.post(url_register, data=payload_register)

        url_authorize = Endpoints.POST_USER_AUTHORIZATION_ENDPOINT
        payload_authorize = UserRegistration.generate_user_data('valid')
        response_authorize = requests.post(url_authorize, data=payload_authorize)

        assert (response_authorize.status_code == 200 and response_authorize.json()['success'] == True)

        access_token = response_authorize.json().get('accessToken')
        UserRegistration.delete_user(access_token)

    @allure.title('Система не позволяет создать авторизоваться с неправильным паролем')
    def test_invalid_user_authorization_wrong_password(self):
        url_register = Endpoints.POST_USER_REGISTER_ENDPOINT
        payload_register = UserRegistration.generate_user_data('valid')
        requests.post(url_register, data=payload_register)

        url_authorize = Endpoints.POST_USER_AUTHORIZATION_ENDPOINT
        payload_authorize = UserRegistration.generate_user_data('wrong_password')
        response_authorize = requests.post(url_authorize, data=payload_authorize)

        assert (response_authorize.status_code == 401 and response_authorize.json()['success'] == False)

        access_token = response_authorize.json().get('accessToken')
        UserRegistration.delete_user(access_token)

    @allure.title('Система не позволяет создать авторизоваться с неправильным логином')
    def test_invalid_user_authorization_wrong_email(self):
        url_register = Endpoints.POST_USER_REGISTER_ENDPOINT
        payload_register = UserRegistration.generate_user_data('valid')
        requests.post(url_register, data=payload_register)

        url_authorize = Endpoints.POST_USER_AUTHORIZATION_ENDPOINT
        payload_authorize = UserRegistration.generate_user_data('wrong_login')
        response_authorize = requests.post(url_authorize, data=payload_authorize)

        assert (response_authorize.status_code == 401 and response_authorize.json()['success'] == False)

        access_token = response_authorize.json().get('accessToken')
        UserRegistration.delete_user(access_token)

class TestChangeUserData:

    @allure.title('Успешное изменение email авторизованного пользователя')
    def test_valid_user_authorization_and_update_email(self):
        # Регистрация пользователя
        url_register = Endpoints.POST_USER_REGISTER_ENDPOINT
        payload_register = UserRegistration.generate_user_data('valid')
        requests.post(url_register, data=payload_register)

        # Авторизация пользователя
        url_authorize = Endpoints.POST_USER_AUTHORIZATION_ENDPOINT
        payload_authorize = UserRegistration.generate_user_data('valid')
        response_authorize = requests.post(url_authorize, data=payload_authorize)
        access_token = response_authorize.json().get('accessToken')

        # Изменение email
        name = UserRegistration.generate_user_data('valid')['name']  # Имя из списка valid
        new_email = UserRegistration.generate_user_data()['email']  # Сгенерированный email

        # Обновление данных пользователя
        url_update = Endpoints.PATCH_USER_DATA_ENDPOINT
        update_payload = {
            'name': name,
            'email': new_email
        }
        response_update = requests.patch(url_update, json=update_payload, headers={'Authorization': access_token})

        assert response_update.status_code == 200

        UserRegistration.delete_user(access_token)


    @allure.title('Успешное изменение имени авторизованного пользователя')
    def test_valid_user_authorization_and_update_name(self):
        # Регистрация пользователя
        url_register = Endpoints.POST_USER_REGISTER_ENDPOINT
        payload_register = UserRegistration.generate_user_data('valid')
        requests.post(url_register, data=payload_register)

        # Авторизация пользователя
        url_authorize = Endpoints.POST_USER_AUTHORIZATION_ENDPOINT
        payload_authorize = UserRegistration.generate_user_data('valid')
        response_authorize = requests.post(url_authorize, data=payload_authorize)
        access_token = response_authorize.json().get('accessToken')

        # Изменение имени
        email = UserRegistration.generate_user_data('valid')['email']  # Email из списка valid
        new_name = UserRegistration.generate_user_data()['name']  # Сгенерированное имя

        # Обновление данных пользователя
        url_update = Endpoints.PATCH_USER_DATA_ENDPOINT
        update_payload = {
            'name': new_name,
            'email': email
        }
        response_update = requests.patch(url_update, json=update_payload, headers={'Authorization': access_token})

        assert response_update.status_code == 200

        UserRegistration.delete_user(access_token)

    @allure.title('Система не дает изменить данные не авторизованного пользователя')
    def test_valid_user_authorization_and_update_name(self):
        email = UserRegistration.generate_user_data()['email']
        name = UserRegistration.generate_user_data()['name']

        # Обновление данных пользователя
        url_update = Endpoints.PATCH_USER_DATA_ENDPOINT
        update_payload = {
            'name': name,
            'email': email
        }
        response_update = requests.patch(url_update, json=update_payload, headers={'Authorization': None})

        assert response_update.status_code == 401
