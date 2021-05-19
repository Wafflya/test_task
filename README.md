# Тестовое задание

Задача: спроектировать и разработать API для системы опросов пользователей.

Функционал для администратора системы:

- авторизация в системе (регистрация не нужна)
- добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание. После создания поле "дата старта" у опроса менять нельзя
- добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)

Функционал для пользователей системы:

- получение списка активных опросов
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

Использовать следующие технологии: Django 2.2.10, Django REST framework.

Результат выполнения задачи:
- исходный код приложения в github (только на github, публичный репозиторий)
- инструкция по разворачиванию приложения (в docker или локально)
- документация по API

## Инструкция по разворачиванию локально

### 1. Клонируем репозиторий
`git clone https://github.com/Wafflya/test_task.git`

### 2. Переходим в папку проекта
`cd ./test_task/`
### 3. Создаём виртаульную машину 
`python -m venv venv`

 
### 4. Активируем
`venv\Scripts\activate` (Win) или  `sourse venv/bin/activate`  (Linux)


### 5. Устанавливаем зависимости
 `pip install -r requirements.txt`
### 6. Создаём миграции

 `python user_polls\manage.py makemigrations `

### 7. Применяем миграции
`python user_polls\manage.py migrate`
### 8. Создаём суперпользователя(опционально)
 `python user_polls\manage.py createsuperuser`
### 9. Запускаем сервер 
`python user_polls\manage.py runserver`
### 10. Готово! Документацию по использованию смотреть здесь:
https://github.com/Wafflya/test_task/blob/master/API_doc.md
