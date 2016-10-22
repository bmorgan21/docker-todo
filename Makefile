SHELL := /bin/bash

db-exec-shell:
	docker exec -it compose_db_1 /bin/bash

db-exec-dump-schema:
	docker exec compose_db_1 /bin/bash -c 'mysql -u root -p"$$MYSQL_ROOT_PASSWORD" -e "DROP DATABASE IF EXISTS db_0; CREATE DATABASE db_0;"'
	docker exec compose_db_1 /bin/bash -c 'mysql -u root -p"$$MYSQL_ROOT_PASSWORD" -v -e "GRANT ALL PRIVILEGES ON db_0.* TO web_user@\"%\";"'
	docker exec compose_web_1 /bin/bash -c 'flask initdb --uri="mysql://$$MYSQL_USER:$$MYSQL_PASSWORD@db:3306/db_0"'
	docker exec compose_db_1 /bin/bash -c 'mysqldump -u root -p"$$MYSQL_ROOT_PASSWORD" --no-data db_0' > schema.sql

web-build:
	docker build -f docker/flask-uwsgi/Dockerfile -t brianmorgan/flask-uwsgi:latest .

web-push: web-build
	docker push brianmorgan/flask-uwsgi:latest

web-run:
	docker run -it brianmorgan/flask-uwsgi

web-run-shell:
	docker run -it brianmorgan/flask-uwsgi /bin/bash

web-exec-shell:
	docker exec -it compose_web_1 /bin/bash

down:
	docker-compose -f docker/compose/nginx-flask-mysql.yml down

up:
	docker-compose -f docker/compose/nginx-flask-mysql.yml up
