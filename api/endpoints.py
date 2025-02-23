class Endpoints:
    """Класс, содержащий все эндпоинты API для Stellar Burgers."""

    MAIN_URL = 'https://stellarburgers.nomoreparties.site'

    POST_USER_REGISTER_ENDPOINT = f'{MAIN_URL}/api/auth/register'  # Нужно передать "email", "password", "name"
    POST_USER_AUTHORIZATION_ENDPOINT = f'{MAIN_URL}/api/auth/login'  # Нужно передать "email", "password"
    GET_USER_DATA_ENDPOINT = f'{MAIN_URL}/api/auth/user'  # Передать accessToken
    PATCH_USER_DATA_ENDPOINT = f'{MAIN_URL}/api/auth/user'  # Передать accessToken, "email", "name"
    DELETE_USER_DATA_ENDPOINT = f'{MAIN_URL}/api/auth/user'  # Передать accessToken
    GET_INGREDIENTS_LIST_ENDPOINT = f'{MAIN_URL}/api/ingredients'
    POST_CREATE_ORDER_ENDPOINT = f'{MAIN_URL}/api/orders'  # Нужно передать хеши ингредиентов "ingredients":
    GET_USER_ORDERS_ENDPOINT = f'{MAIN_URL}/api/orders'
    GET_ALL_ORDERS_ENDPOINT = f'{MAIN_URL}/api/orders/all'
