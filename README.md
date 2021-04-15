# Тестовое задание
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
### 10. Готово
