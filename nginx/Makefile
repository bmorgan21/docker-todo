NS = brianmorgan
VERSION ?= latest

REPO = nginx
NAME = nginx
INSTANCE = default

MAJOR = 2
MINOR = 1
PATCH = 0

.PHONY: build push shell run start stop rm release

build:
	docker build -t $(NS)/$(REPO):$(VERSION) .

push:
	docker push $(NS)/$(REPO):$(VERSION)

shell:
	docker run --rm --name $(NAME)-$(INSTANCE) -i -t $(PORTS) $(VOLUMES) $(ENV) $(NS)/$(REPO):$(VERSION) /bin/bash

run:
	docker run --rm --name $(NAME)-$(INSTANCE) $(PORTS) $(VOLUMES) $(ENV) $(NS)/$(REPO):$(VERSION)

start:
	docker run -d --name $(NAME)-$(INSTANCE) $(PORTS) $(VOLUMES) $(ENV) $(NS)/$(REPO):$(VERSION)

stop:
	docker stop $(NAME)-$(INSTANCE)

rm:
	docker rm $(NAME)-$(INSTANCE)

release: build
	make push -e VERSION=$(VERSION)
	docker tag $(NS)/$(REPO):latest $(NS)/$(REPO):$(MAJOR)
	make push -e VERSION=$(MAJOR)
	docker tag $(NS)/$(REPO):latest $(NS)/$(REPO):$(MAJOR).$(MINOR)
	make push -e VERSION=$(MAJOR).$(MINOR)
	docker tag $(NS)/$(REPO):latest $(NS)/$(REPO):$(MAJOR).$(MINOR).$(PATCH)
	make push -e VERSION=$(MAJOR).$(MINOR).$(PATCH)

default: build
