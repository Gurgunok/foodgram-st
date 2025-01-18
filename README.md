# Foodgram Project

## Описание

Проект "Foodgram" — это веб-приложение, которое позволяет пользователям добавлять рецепты, делиться ими и сохранять их в избранное.

## Требования

- Docker
- Docker Compose

## Установка и запуск

1.Клонируйте репозиторий:
```bash
git clone https://github.com/Gurgunok/foodgram-st.git
```
2.Запустите проект:
```bash
cd infra
docker-compose up -d
```
3.Создайте суперпользователя:
```bash
docker-compose exec backend python manage.py createsuperuser
```
4.Загрузите ингридиенты:
```bash
cd infra
docker-compose exec backend bash
python manage.py load_ingredients data/ingredients.json
```
5.Доступ к проекту:

Фронтенд доступен по адресу: http://localhost
Админ-панель Django доступна по адресу: http://localhost/admin или http://127.0.0.1:8000/admin

6.Тесты проводились в postmen по пути:
postman_collection/foodgram.postman_collection.json

7.Для остановки сервисов используйте команду:
```bash
docker-compose down
```
