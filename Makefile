SHELL := /bin/bash

NAME = todo

help:          ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

init:
	echo "version: '2'" > local.yml

dump-schema:
	docker exec $(NAME)_api_1 /bin/bash -c 'flask db diff'
	docker exec $(NAME)_db_1 /bin/bash -c 'mysqldump -u root -p"$$MYSQL_ROOT_PASSWORD" db_0' > flask/db/schema.sql

shell:
	docker exec -it $(NAME)_$(word 2, $(MAKECMDGOALS) )_1 /bin/bash

restart:
	docker restart $(NAME)_$(word 2, $(MAKECMDGOALS) )_1

down:
	docker-compose -f nginx-flask-mysql.yml -f local.yml -p $(NAME) down

up:
	docker-compose -f nginx-flask-mysql.yml -f local.yml -p $(NAME) up

pull:
	docker-compose -f nginx-flask-mysql.yml -f local.yml pull

reset:         ## Remove files created during container setup
	rm -f flask/instance/settings.cfg
	rm -f angularjs/app/services/api-service.js

stop:          ## Stop all docker containers
	docker ps -a -q | xargs docker stop

remove:        ## Remove all docker containers with their volumes
	docker ps -a -q | xargs docker rm -v

remove-volumes:## Remove all dangling volumes
	docker volume ls -qf dangling=true | xargs docker volume rm
