import pytest
from helpers.user_helpers import UserRegistration

@pytest.fixture
def registered_user():
    user_data = UserRegistration.register_new_user()
    access_token = user_data['access_token']
    payload = user_data['payload']

    yield {
        'access_token': access_token,
        'payload': payload
    }

    UserRegistration.delete_user(access_token)


