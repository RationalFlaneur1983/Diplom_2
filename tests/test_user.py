import requests
import allure
from api.endpoints import Endpoints
from helpers.user_helpers import UserRegistration

class TestCreateUser:

    @allure.title('Успешное создание учетной записи пользователя с корректными данными')
    def test_valid_user_registration(self, registered_user):
        access_token = registered_user['access_token']
        payload = registered_user['payload']
        assert access_token is not None
        assert payload is not None

    @allure.title('Система не позволяет создать пользователя, который уже зарегистрирован')
    def test_invalid_user_registration_already_exists(self, registered_user):
        payload = registered_user['payload']
        url = Endpoints.POST_USER_REGISTER_ENDPOINT
        response_repeat = requests.post(url, data=payload)
        assert response_repeat.status_code == 403 and response_repeat.json()['success'] == False


    @allure.title('Система не позволяет создать пользователя с незаполненным полем email')
    def test_invalid_user_registration_empty_email(self):
        url = Endpoints.POST_USER_REGISTER_ENDPOINT
        payload = UserRegistration.generate_user_data('no_email')
        response = requests.post(url, data=payload)
        assert (response.status_code == 403 and response.json()['success'] == False)


    @allure.title('Система не позволяет создать пользователя с незаполненным полем email')
    def test_invalid_user_registration_empty_password(self):
        url = Endpoints.POST_USER_REGISTER_ENDPOINT
        payload = UserRegistration.generate_user_data('no_password')
        response = requests.post(url, data=payload)
        assert (response.status_code == 403 and response.json()['success'] == False)


class TestLoginUser:

    @allure.title('Успешная авторизация пользователя с корректными данными')
    def test_valid_user_authorization(self, registered_user):
        payload = registered_user['payload']
        url_authorize = Endpoints.POST_USER_AUTHORIZATION_ENDPOINT
        response_authorize = requests.post(url_authorize, data=payload)
        assert response_authorize.status_code == 200 and response_authorize.json()['success'] == True

    @allure.title('Система не позволяет авторизоваться с неправильным паролем')
    def test_invalid_user_authorization_wrong_password(self, registered_user):
        payload = registered_user['payload']
        wrong_password_data = UserRegistration.generate_user_data('wrong_password')
        wrong_password = wrong_password_data['password']

        payload_authorize = {
            'email': payload['email'],
            'password': wrong_password
        }
        url_authorize = Endpoints.POST_USER_AUTHORIZATION_ENDPOINT
        response_authorize = requests.post(url_authorize, data=payload_authorize)
        assert response_authorize.status_code == 401 and response_authorize.json()['success'] == False

    @allure.title('Система не позволяет авторизоваться с неправильным логином')
    def test_invalid_user_authorization_wrong_email(self, registered_user):
        payload = registered_user['payload']
        wrong_login_data = UserRegistration.generate_user_data('wrong_login')
        wrong_email = wrong_login_data['email']
        payload_authorize = {
            'email': wrong_email,
            'password': payload['password']
        }
        url_authorize = Endpoints.POST_USER_AUTHORIZATION_ENDPOINT
        response_authorize = requests.post(url_authorize, data=payload_authorize)
        assert response_authorize.status_code == 401 and response_authorize.json()['success'] == False

class TestChangeUserData:

    @allure.title('Успешное изменение email авторизованного пользователя')
    def test_valid_user_authorization_and_update_email(self, registered_user):
        payload = registered_user['payload']
        access_token = registered_user['access_token']
        new_email = UserRegistration.generate_user_data()['email']
        url_update = Endpoints.PATCH_USER_DATA_ENDPOINT
        update_payload = {
            'name': payload['name'],
            'email': new_email
        }
        response_update = requests.patch(url_update, json=update_payload, headers={'Authorization': access_token})
        assert response_update.status_code == 200 and response_update.json()['success'] == True

    @allure.title('Успешное изменение имени авторизованного пользователя')
    def test_valid_user_authorization_and_update_name(self, registered_user):
        payload = registered_user['payload']
        access_token = registered_user['access_token']
        new_name = UserRegistration.generate_user_data()['name']
        url_update = Endpoints.PATCH_USER_DATA_ENDPOINT
        update_payload = {
            'name': new_name,
            'email': payload['email']
        }
        response_update = requests.patch(url_update, json=update_payload, headers={'Authorization': access_token})
        assert response_update.status_code == 200 and response_update.json()['success'] == True

    @allure.title('Система не дает изменить данные не авторизованного пользователя')
    def test_valid_user_authorization_and_update_name(self):
        email = UserRegistration.generate_user_data()['email']
        name = UserRegistration.generate_user_data()['name']
        url_update = Endpoints.PATCH_USER_DATA_ENDPOINT
        update_payload = {
            'name': name,
            'email': email
        }
        response_update = requests.patch(url_update, json=update_payload, headers={'Authorization': None})
        assert response_update.status_code == 401 and response_update.json()['message'] == 'You should be authorised'
