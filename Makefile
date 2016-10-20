SHELL := /bin/bash

build:
	docker build -t foo .

run: build
	docker run -it --rm --name running-foo foo /bin/bash


#docker-compose down -v
#docker volume ls -f dangling=true
