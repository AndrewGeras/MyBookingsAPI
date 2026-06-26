from datetime import date, timedelta


df_exmp = date.today()
dt_exmp = date.today() + timedelta(days=1)

hotel_example = {
    "valid": {
        "summary": "Валидные данные",
        "description": "Пример **валидных** данных отеля.",
        "value": {"title": "Отель-Шмотель", "location": "in_the_middle_of_nowhere"},
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
        "value": {
            "nickname": "VasPup",
            "email": "vpupkin@qwerty.bzd",
            "password": "pupkin123",
            "first_name": "Василий",
            "last_name": "Пупкин",
        },
    },
    "user_2": {
        "summary": "Пример пользователя 2",
        "description": "Пример **валидных** данных пользователя 2.",
        "value": {
            "nickname": "FedZub",
            "email": "fzubkin@qwerty.bzd",
            "password": "zubkin123",
            "first_name": "Фёдор",
            "last_name": "Зубкин",
        },
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
            "quantity": 1,
            "facilities_ids": [],
        },
    },
}


test_user_data = {
    "nickname": "TestUser",
    "email": "test@user.xyz",
    "password": "test_password",
    "first_name": "Name",
    "last_name": "Surname",
}

test_auth_data = [
    # ("nickname, email, password, first_name, last_name, auth_status, login, pass_code, login_status, logged_status")
    (
        "TestUser",
        "test@user.xyz",
        "test_password",
        "Name",
        "Surname",
        201,
        "test@user.xyz",
        "test_password",
        200,
        200,
    ),
    (
        "TestUser",
        "test2@user.xyz",
        "test_password",
        "Name",
        "Surname",
        400,
        "test2@user.xyz",
        "test_password",
        404,
        401,
    ),  # повторный nickname, не найден login
    (
        "TestUser2",
        "test@user.xyz",
        "test_password",
        "Name",
        "Surname",
        400,
        "test@user.xyz",
        "test_pass",
        401,
        401,
    ),  # повторный email. неверный pass_code
    (
        "TestUser2",
        "test2@user.xyz",
        "test_password2",
        None,
        None,
        201,
        "test2@user.xyz",
        "test_password2",
        200,
        200,
    ),
    (
        "TestUser3",
        "test3user.xyz",
        "test_password3",
        None,
        None,
        422,
        "test2user.xyz",
        "test_password2",
        422,
        401,
    ),  # некорректный email, некорректный login
    (
        "TestUser3",
        "test3@userxyz",
        "test_password3",
        None,
        None,
        422,
        "test2@userxyz",
        "test_password2",
        422,
        401,
    ),  # некорректный email, некорректный login
    (
        "TestUser3",
        "",
        "test_password3",
        "Name3",
        "Surname3",
        422,
        "",
        "test_password2",
        422,
        401,
    ),  # некорректный email, пустая строка login
    (
        "TestUser3",
        None,
        "test_password3",
        None,
        None,
        422,
        None,
        "test_password4",
        422,
        401,
    ),  # отсутствует email, отсутствует login
    (
        None,
        "test3@user.xyz",
        "test_password3",
        None,
        None,
        422,
        "test4@user.xyz",
        None,
        422,
        401,
    ),  # отсутствует nickname, отсутствует pass_code
    (
        "",
        "test3@user.xyz",
        "test_password3",
        None,
        None,
        201,
        "test3@user.xyz",
        "",
        401,
        401,
    ),  # пустая строка nickname*, неверный pass_code
    (
        "TestUser4",
        "test4@user.xyz",
        None,
        None,
        None,
        422,
        "test4@user.xyz",
        "test_password4",
        404,
        401,
    ),  # отсутствует password, не найден login
    (
        "TestUser4",
        "test4@user.xyz",
        "",
        None,
        None,
        201,
        "test4@user.xyz",
        "",
        200,
        200,
    ),  # пустая строка password*
]
