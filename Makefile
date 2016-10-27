SHELL := /bin/bash

dump-schema:
	docker exec dockertodo_db_1 /bin/bash -c 'mysql -u root -p"$$MYSQL_ROOT_PASSWORD" -e "DROP DATABASE IF EXISTS db_0; CREATE DATABASE db_0;"'
	docker exec dockertodo_db_1 /bin/bash -c 'mysql -u root -p"$$MYSQL_ROOT_PASSWORD" -v -e "GRANT ALL PRIVILEGES ON db_0.* TO web_user@\"%\";"'
	docker exec dockertodo_web_1 /bin/bash -c 'flask initdb --uri="mysql://$$MYSQL_USER:$$MYSQL_PASSWORD@db:3306/db_0"'
	docker exec dockertodo_db_1 /bin/bash -c 'mysqldump -u root -p"$$MYSQL_ROOT_PASSWORD" --no-data db_0' > flask/schema.sql

db-shell:
	docker exec -it dockertodo_db_1 /bin/bash

web-shell:
	docker exec -it dockertodo_web_1 /bin/bash

down:
	docker-compose -f nginx-flask-mysql.yml -f local.yml down

up:
	docker-compose -f nginx-flask-mysql.yml -f local.yml up
