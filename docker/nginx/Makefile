SHELL := /bin/bash

MAJOR = 1
MINOR = 10
PATCH = 2
NS = brianmorgan
NAME = nginx

build:
	for v in latest $(MAJOR) $(MAJOR).$(MINOR) $(MAJOR).$(MINOR).$(PATCH); do \
		docker build -q -t $(NS)/$(NAME):$$v .; \
	done

push: build
	for v in latest $(MAJOR) $(MAJOR).$(MINOR) $(MAJOR).$(MINOR).$(PATCH); do \
		docker push $(NS)/$(NAME):$$v; \
	done

