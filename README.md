# Тестовое задание
## Инструкция по разворачиванию локально
git clone https://github.com/Wafflya/test_task.git

cd ./test_task/

python -m venv venv

venv\Scripts\activate  или  sourse venv/bin/activate

pip install -r requirements.txt

python user_polls\manage.py makemigrations 


python user_polls\manage.py migrate

python user_polls\manage.py createsuperuser

python user_polls\manage.py runserver
