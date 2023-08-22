### Участники:

> [Dmitriy](https://github.com/feym4n-git) - teamleader | [Slava](https://github.com/slavajet) - разработчик | [Vitaliy](https://github.com/VitalRu) - разработчик
 
![Static Badge](https://img.shields.io/badge/python-3.9.10-blue?style=for-the-badge&logo=python&labelColor=yellow) ![Static Badge](https://img.shields.io/badge/Django-2.2.16-%23156741?style=for-the-badge&logo=Django&labelColor=%231d915c) ![Static Badge](https://img.shields.io/badge/REST_API-%25?style=for-the-badge&color=279EFF) ![Static Badge](https://img.shields.io/badge/JWT_authentication-C70039?style=for-the-badge&logo=JWT&labelColor=%231d915c)


## Описание:

Проект YaMDb собирает отзывы пользователей на произведения. 
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
К произведениям можно оставить отзыв и поставить оценку. К отзывам можно писать комментарии.

## Установка:

Находясь в каталоге проекта, создать и активировать виртуальное окружение:


для Linux
```
python3 -m venv venv

source env/bin/activate
```

для Windows
```
python -m venv venv

source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

Выполнить миграции:
```
python manage.py makemigrations
python manage.py migrate
```

Запустить проект:
```
python manage.py runserver
```

Документация проекта: 
```
http://127.0.0.1:8000/redoc/
http://127.0.0.1:8000/swagger/
```

## Примеры запросов

### Регистрация нового пользователя

POST-запрос
```
http://127.0.0.1:8000/api/v1/auth/signup/
```
```
{
    "username": "user_one",
    "email": "user@example.com"
}
```
На указанную почту приходит код подтверждения который нужно отправить на следующий endpoint

### Получение JWT-токена

POST-запрос
```
http://127.0.0.1:8000/api/v1/auth/token/


{
    "username": "user_one",
    "confirmation_code": "Usyieuy_dsHLSDHJKFAd_Dfhsjldh"
}

```

В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом. После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт /api/v1/users/me/ и заполнить поля в своём профайле (описание полей — в документации).

Остальные запросы можно посмотреть в документации в Redoc или Swagger.