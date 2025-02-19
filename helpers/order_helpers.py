import allure
import random
import string
from api.endpoints import Endpoints
import requests


class OrderHelpers:
    """Класс, содержащий помощников для тестирования создания заказов"""

    @allure.step('Создание списка ингредиентов')
    def generate_ingredient_list():
        url = Endpoints.GET_INGREDIENTS_LIST_ENDPOINT  # Формируем URL
        response = requests.get(url)  # Отправляем GET-запрос

        # Проверяем успешность ответа
        if response.status_code != 200:
            raise Exception(f'Ошибка при получении ингредиентов: {response.status_code}')

        data = response.json().get('data', [])  # Получаем список ингредиентов, если он есть

        if len(data) < 1:
            raise Exception('Недостаточно ингредиентов для создания заказа')  # Проверяем, достаточно ли ингредиентов

        # Случайное количество ингредиентов от 1 до 5
        num_ingredients = random.randint(1, min(5, len(data)))

        # Случайный выбор ингредиентов
        ingredient_list = random.sample([ingredient['_id'] for ingredient in data], num_ingredients)

        return ingredient_list  # Возвращаем список ингредиентов


    @allure.step('Генерируем рандомный неправильный хеш')
    def generate_random_string(length=24): # Генерируем рандомный хеш
        characters = string.ascii_letters + string.digits

        return ''.join(random.choice(characters) for _ in range(length))

