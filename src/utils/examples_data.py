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
    "valid": {
        "summary": "Валидные данные",
        "description": "Пример **валидных** данных пользователя.",
        "value": {"nickname": "VasPup",
                  "email": "vpupkin@qwerty.bzd",
                  "password": "pupkin123",
                  "first_name": "Василий",
                  "last_name": "Пупкин"
                  }
    }
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
