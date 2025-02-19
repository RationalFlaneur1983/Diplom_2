user_data_sets = {
    'valid': {
        'description': 'Тест с валидными данными',
        'data': {
            'email': 'test4_user_qa@example.com',
            'password': 'securep@$$word123',
            'name': 'alexander_the_not_so_great',
        }
    },
    'no_email': {
        'description': 'Тест без email',
        'data': {
            'email': '',
            'password': 'securep@$$word123',
            'name': 'alexander_the_not_so_great',
        }
    },
    'no_password': {
        'description': 'Тест без пароля',
        'data': {
            'email': 'test4_user_qa@example.com',
            'password': '',
            'name': 'alexander_the_not_so_great',
        }
    },
    'wrong_password': {
        'description': 'Неправильный пароль',
        'data': {
            'email': 'test4_user_qa@example.com',
            'password': 'qwerty',
            'name': 'alexander_the_not_so_great',
        }
    },
    'wrong_login': {
        'description': 'Неправильный логин (логин происходит по email)',
        'data': {
            'email': 'wrong@example.com',
            'password': 'securep@$$word123',
            'name': 'alexander_the_not_so_great',
        }
    }
}
