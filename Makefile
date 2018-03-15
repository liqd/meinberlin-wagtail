VIRTUAL_ENV ?= venv

.PHONY: release
release: export DJANGO_SETTINGS_MODULE ?= meinberlin_wagtail.settings.build
release:
	$(VIRTUAL_ENV)/bin/python3 -m pip install -r requirements.txt -q
	$(VIRTUAL_ENV)/bin/python3 manage.py collectstatic --noinput -v0
