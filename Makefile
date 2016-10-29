SHELL := /bin/bash

NAME = todo

dump-schema:
	docker exec $(NAME)_db_1 /bin/bash -c 'mysql -u root -p"$$MYSQL_ROOT_PASSWORD" -e "DROP DATABASE IF EXISTS db_0; CREATE DATABASE db_0;"'
	docker exec $(NAME)_db_1 /bin/bash -c 'mysql -u root -p"$$MYSQL_ROOT_PASSWORD" -v -e "GRANT ALL PRIVILEGES ON db_0.* TO web_user@\"%\";"'
	docker exec $(NAME)_web_1 /bin/bash -c 'flask initdb --uri="mysql://$$MYSQL_USER:$$MYSQL_PASSWORD@db:3306/db_0"'
	docker exec $(NAME)_db_1 /bin/bash -c 'mysqldump -u root -p"$$MYSQL_ROOT_PASSWORD" --no-data db_0' > flask/schema.sql

db-shell:
	docker exec -it $(NAME)_db_1 /bin/bash

web-shell:
	docker exec -it $(NAME)_web_1 /bin/bash

down:
	docker-compose -f nginx-flask-mysql.yml -f local.yml -p $(NAME) down

up:
	docker-compose -f nginx-flask-mysql.yml -f local.yml -p $(NAME) up
