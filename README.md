# Тестовое задание
## Инструкция по разворачиванию локально

1. Клонируем репозиторий
`git clone https://github.com/Wafflya/test_task.git`

2. Переходим в папку проекта
`cd ./test_task/`
3. Создаём виртаульную машину 
`python -m venv venv`

 
4. Активируем
`venv\Scripts\activate` (Win) или  `sourse venv/bin/activate`  (Linux)

4. `pip install -r requirements.txt`

5. `python user_polls\manage.py makemigrations `


`python user_polls\manage.py migrate`

`python user_polls\manage.py createsuperuser`

`python user_polls\manage.py runserver`
