.PHONY: all
all: install

###############################################################################

.PHONY: doctor
doctor:
	bin/verchew --exit-code

.PHONY: .envrc
.envrc:
	echo "export PYTHONBREAKPOINT=ipdb.set_trace" >> $@
	echo >> $@
	echo "export REDIS_URL=redis://localhost:6379" >> $@

###############################################################################

.PHONY: install
install: .venv/flag
.venv/flag: poetry.lock runtime.txt requirements.txt
	@ poetry config virtualenvs.in-project true || poetry config settings.virtualenvs.in-project true
	poetry install
	@ mkdir -p staticfiles
	@ touch $@

ifndef CI

poetry.lock: pyproject.toml
	poetry lock
	@ touch $@

runtime.txt: .python-version
	echo "python-$(shell cat $<)" > $@

requirements.txt: poetry.lock
	poetry export --format requirements.txt --output $@ || echo "ERROR: Poetry 1.x required to export dependencies"

endif

###############################################################################

.PHONY: run
run: install migrate
	poetry run python manage.py runserver

###############################################################################

PACKAGES := config elections tests

.PHONY: ci
ci: check test

.PHONY: format
format: install
	poetry run isort $(PACKAGES) --recursive --apply
	poetry run black $(PACKAGES)
	@ echo

.PHONY: check
check: format
ifdef CI
	git diff --exit-code
endif
	poetry run mypy $(PACKAGES) --config-file=.mypy.ini
	poetry run pylint $(PACKAGES) --rcfile=.pylint.ini

.PHONY: test
test: install
	poetry run pytest elections tests

.PHONY: watch
watch: install
	poetry run ptw

.PHONY: notebook
notebook: install
	poetry run jupyter notebook --notebook-dir=notebooks --browser=safari

###############################################################################

.PHONY: migrations
migrations: install
	poetry run python manage.py makemigrations

.PHONY: migrate
migrate: install
	poetry run python manage.py migrate
	@ echo
	poetry run python manage.py migrate_data

.PHONY: data
data: migrate
	poetry run python manage.py seed_data
	@ echo
	poetry run python manage.py scrape_data --start=1828 --limit=5
	@ echo
	poetry run python manage.py sync_data

.PHONY: reset
reset: install
	dropdb elections_dev; createdb elections_dev
	@ echo
	@ make data

.PHONY: uml
uml: install
	poetry run pyreverse elections -p elections -a 1 -f ALL -o png --ignore admin.py,migrations,management,tests
	mv -f classes_elections.png docs/classes.png
	mv -f packages_elections.png docs/packages.png
	poetry run python manage.py graph_models elections --group-models --output=docs/tables.png --exclude-models=TimeStampedModel

###############################################################################

.PHONY: clean
clean:
	rm -rf .venv
