hotel_example = {
    "valid": {
        "summary": "Валидные данные",
        "description": "Пример **валидных** данных отеля.",
        "value": {"title": "Отель-Шмотель",
                  "location": "in_the_middle_of_nowhere"}
    },
    "invalid": {
        "summary": "Невалидные данные",
        "description": "Пример **невалидных** данных отеля.",
        "value": {
            "title": 123,
            "location": 456,

        },
    },
}

user_example = {
    "user_1": {
        "summary": "Пример пользователя 1",
        "description": "Пример **валидных** данных пользователя 2.",
        "value": {"nickname": "VasPup",
                  "email": "vpupkin@qwerty.bzd",
                  "password": "pupkin123",
                  "first_name": "Василий",
                  "last_name": "Пупкин"
                  }
    },
    "user_2": {
        "summary": "Пример пользователя 2",
        "description": "Пример **валидных** данных пользователя 2.",
        "value": {"nickname": "FedZub",
                  "email": "fzubkin@qwerty.bzd",
                  "password": "zubkin123",
                  "first_name": "Фёдор",
                  "last_name": "Зубкин"
                  }
    },
}

room_data = {
    "valid": {
        "summary": "Валидные данные",
        "description": "Пример **валидных** данных для класса номеров",
        "value": {
            "title": "люкс",
            "description": "Лухари пентхаус со шлюхами и Джек Дэниэлзом",
            "price": 99999.99,
            "quantity": 1
        }
    },
}
