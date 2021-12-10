## REST API для сервиса YaMDb — базы отзывов о фильмах, книгах и музыке. (Совместный проект 3 студентов Яндекс.Практикума)

# Описание
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором.

В каждой категории есть произведения: книги, фильмы или музыка.

Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы (Review) и выставляют произведению рейтинг (оценку в диапазоне от одного до десяти). Из множества оценок автоматически высчитывается средняя оценка произведения.

# Стек технологий
Python3, Django 3, Django REST Framework, SQLite3, Simple JWT, Django Filter.

# Запуск проекта
Создание и активация виртуального окружения:
```
python3 -m venv venv
source venv/Scripts/activate
```
Установка зависимостей из файла requirements.txt:
```
pip install -r requirements.txt
```
Применить миграции:
```
python manage.py migrate
```
Запустить сервер:
```
python manage.py runserver
```
# Документация
Чтобы открыть документацию, запустите сервер и перейдите по ссылке:
```
http://127.0.0.1:8000/redoc/
```
