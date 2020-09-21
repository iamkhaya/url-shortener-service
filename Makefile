checkfiles = url_shortener_service/ tests/ setup.py
devenv = PYTHONPATH=.
export ROLE=DEV
export ENVIRONMENT=TEST
export PROVIDER=SELF-HOSTED

help:
	@echo  "usage: make <target>"
	@echo  "Targets:"
	@echo  "    up          Updates dev/test dependencies"
	@echo  "    deps        Ensure dev/test dependencies are installed"
	@echo  "    lint	Reports all linter violations"
	@echo  "    test	Runs all tests"
	@echo  "    ci		Runs linter and tests"
	@echo  "    run         Runs in development mode(localhost)"

up:
	pip install -q pip-tools
	pip-compile -U --no-emit-index-url --no-emit-trusted-host requirements.in
	pip-compile -U --no-emit-index-url --no-emit-trusted-host tests/requirements.in

deps:
	@pip install --upgrade pip
	@pip install -q pip-tools
	@pip-sync requirements.txt tests/requirements.txt
	@pip install --no-cache-dir -qe  .

isort:
	isort -rc url_shortener_service tests

lint:
	flake8 $(checkfiles)
	pylint $(checkfiles)
	mypy $(checkfiles)
	python setup.py check -mr

style:
	isort -rc $(checkfiles)
	black $(checkfiles)


test:
	pytest --disable-warnings --cov=url_shortener_service --cov-report term tests

ci: deps lint test

run:
	uwsgi  --ini-paste-logged  url_shortener_service/config/pyramid/dev.ini
