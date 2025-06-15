all: setup-env-variables install test

.PHONY: install
install:
	npm install

.PHONY: lint
lint:
	npm lint

.PHONY: test
test:
	npm test

.PHONY: setup-env-variables
setup-env-variables:
	cp .env.example .env