# *Проект QRKot spreadsheets*

## Авторы
 - [Павел Тыртин](https://github.com/R1Sen007)

## Технологии
### backend
 - fastapi==0.78.0
 - fastapi-users[sqlalchemy]==10.0.4
 - sqlalchemy==1.4.36
 - alembic==1.7.7
 - aiogoogle==4.2.0
 - pytest==7.1.3

## Описание:

***Пользователи сервиса QRKot spreadsheets могут донатить на благотворительные проекты, размещенные на проекте!***

## Как развернуть проект:

- Клонировать репозиторий
```
git clone https://github.com/R1Sen007/QRkot_spreadsheets.git
```

- Перейти в корень проекта и создать файл ".env" с переменными окружения 
```
touch .env
```

- Файл должен содержать следующие переменные:
```
APP_TITLE=...
DATABASE_URL=...
SECRET=...
FIRST_SUPERUSER_EMAIL=...
FIRST_SUPERUSER_PASSWORD=...

TYPE=...
PROJECT_ID=...
PRIVATE_KEY_ID=...
PRIVATE_KEY=...
CLIENT_EMAIL=...
CLIENT_ID=...
AUTH_URI=...
TOKEN_URI=...
AUTH_PROVIDER_X509_CERT_URL=...
CLIENT_X509_CERT_URL=...

EMAIL=...
```


- Cоздать и активировать виртуальное окружение:
```
python -m venv env
```
```
source venv/Scripts/activate
```

- Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```

Выполнить миграции:
```
alembic upgrade head
```

Запустить проект:
```
uvicorn app.main:app --reload
```

- Ввести в адресной строке браузера localhost

## Дополнительные возможности:

- По адресу ```/docs``` есть возможность просмотреть Swagger документацию по API.
- Формирование отчёта в гугл таблицах, через эндпоинт ```/google```
- При запуске ```python setup_for_postman.py``` создаётся первый суперюзер.