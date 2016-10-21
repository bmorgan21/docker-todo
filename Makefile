SHELL := /bin/bash

web-build:
	docker build -f docker/flask-uwsgi/Dockerfile -t brianmorgan/flask-uwsgi:latest .

web-run:
	docker run -it brianmorgan/flask-uwsgi

web-run-shell:
	docker run -it brianmorgan/flask-uwsgi /bin/bash

down:
	docker-compose -f docker/compose/nginx-flask-mysql.yml down

up:
	docker-compose -f docker/compose/nginx-flask-mysql.yml up
