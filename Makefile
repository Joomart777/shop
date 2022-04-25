run:
	./manage.py runserver

## можно так запускать, сохраненную команду  ---> make run  (корректировка через нано на лишние пробелы)

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate
user:
	python3 manage.py createsuperuser

## убить занятый порт 8000:
kill:
	fuser -k 8000/tcp
