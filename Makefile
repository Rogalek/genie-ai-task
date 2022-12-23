.PHONY:  package
SHELL := /bin/bash

init:
	python -m venv .venv
	source .venv/bin/activate \
	&& pip install --upgrade pip \
	&& pip install poetry \
	&& pip install pre-commit \
	&& poetry install

run:
	source .venv/bin/activate \
	&& python -m home_assignment

clean:
	rm -rf .venv

package:
	rm -rf .assignment_package
	mkdir .assignment_package
	cp .env .assignment_package/
	cp .pre-commit-config.yaml .assignment_package/
	cp ASSIGNMENT.md .assignment_package/
	cp docker-compose.yml .assignment_package/
	cp LICENSE.md .assignment_package/
	cp Makefile .assignment_package/
	cp README.md .assignment_package/
	cp poetry.lock .assignment_package/
	cp pyproject.toml .assignment_package/
	cp setup.cfg .assignment_package/
	find ./home_assignment -name '*.py' -exec cp --parents "{}" .assignment_package/ \;
	cd .assignment_package && zip -r ../assignment.zip .


pre_commit:
	source .venv/bin/activate \
	&& pre-commit run --all
