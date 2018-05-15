rasmus:
	python manage.py runserver 0.0.0.0:3000

ask:
	docker-compose run web python manage.py dumpdata groups.Contract > contracts.json

envrun:
	python3 manage.py runserver 0.0.0.0:8000

envstyle:
	autopep8 --in-place --recursive --max-line-length=100 accounts forms groups ntnui hs
	prospector --uses django --max-line-length=100

start:
	docker-compose up web

start-background:
	docker-compose up web -d

run-browser:
	docker-compose up -d selenium

stop:
	docker-compose down

test:
	docker-compose run web python manage.py test
	docker-compose down

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
	docker-compose run web python manage.py loaddata users.json groups.json locations.json memberships.json boards.json invitations.json forms.json mainboard.json hs-memberships.json bookings.json

browser-tests:
	docker-compose up -d chrome
	docker-compose up -d firefox
	docker-compose run tester python3 manage.py test ntnui.tests.browser

browser-tests-local:
	BROWSER=local python3 manage.py test ntnui.tests.browser

style:
	docker-compose run web autopep8 --in-place --recursive --max-line-length=100 accounts forms groups ntnui
	docker-compose run web prospector --uses django --max-line-length=100
