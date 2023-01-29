# praktikum_new_diplom
# Описание 
Проект Foodgram «Продуктовый помощник».
 
Проект Foodgram позволяет пользователям  публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд. 

# Статус
![workflow](https://github.com/Amirkhan012/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

## Ссылка на развернутый проект
http://62.84.123.70/

### Ссылка на redoc
http://62.84.123.70/api/docs/redoc.html

### ADMIN
login - pon@mail.ru
password - admin
 
 
# Установка 
 
## Как запустить проект: 
Клонировать репозиторий и перейти в него в командной строке: 
 
``` 
https://github.com/Amirkhan012/foodgram-project-react

``` 
 
``` 
cd backend/
``` 
 
Cоздать и активировать виртуальное окружение: 
 
``` 
py -m venv venv 
``` 
 
``` 
source venv/bin/activate 
``` 
 
``` 
py -m pip install --upgrade pip 
``` 
 
Установить зависимости из файла requirements.txt: 
 
``` 
pip install -r requirements.txt 
``` 
 
Выполнить миграции: 
 
``` 
py manage.py migrate 
``` 
 
Запустить проект: 
 
``` 
py manage.py runserver 
``` 
## Как запустить проект через docker:

### Шаблон наполнения env-файла
DB_ENGINE - указываем, что работаем с postgresql
DB_NAME - имя базы данных
POSTGRES_USER - логин для подключения к базе данных
POSTGRES_PASSWORD - пароль для подключения к БД
DB_HOST - название сервиса (контейнера)
DB_PORT - порт для подключения к БД

### Команда для запуска приложения
Находясь в директории где находится docker-compose:
```
docker-compose up -d --build
```

### Команда для заполнения базы данными
```
python manage.py loaddata db.json
```
