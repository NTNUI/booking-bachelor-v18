rasmus:
	python manage.py runserver 0.0.0.0:3000

runenv:
	python3 manage.py runserver 0.0.0.0:8000

run:
	docker-compose up

run-background:
	docker-compose up -d

stop:
	docker-compose down

test:
	docker-compose run web python manage.py test

migrations:
	docker-compose run web python manage.py makemigrations

migrate:
	docker-compose run web python manage.py migrate

superuser:
	docker-compose run web python manage.py createsuperuser

build:
	docker-compose build

testenv:
	rm -f mydatabase
	make migrate
	docker-compose run web python manage.py loaddata users.json groups.json memberships.json

run-selenium:
	

test-integration:
	make testenv
	make run-background
	make run-selenium
	make stop
