install-deps:
	pip install -r requirements.txt

gunicorn-post-app:
	gunicorn --bind=0.0.0.0:$(GUNICORN_POST_PORT) --timeout=$(GUNICORN_POST_TIMEOUT) --workers=$(GUNICORN_POST_WORKERS) apps.post.app:app

gunicorn-status-app:
	gunicorn --bind=0.0.0.0:$(GUNICORN_STATUS_PORT) --timeout=$(GUNICORN_STATUS_TIMEOUT) --workers=$(GUNICORN_STATUS_WORKERS) apps.status.app:app


GUNICORN_POST_WORKERS ?= 3
GUNICORN_POST_TIMEOUT ?= 5000
GUNICORN_POST_PORT ?= 80

GUNICORN_STATUS_WORKERS ?= 3
GUNICORN_STATUS_TIMEOUT ?= 5000
GUNICORN_STATUS_PORT ?= 8000
