SHELL := /bin/bash

build-flask-uwsgi:
	docker build -f docker/flask-uwsgi/Dockerfile -t brianmorgan/flask-uwsgi:latest . 
