DOCKER_COMPOSE_DEV = docker-compose
DOCKER_COMPOSE_CI = docker-compose -f docker-compose.yml
DOCKER_COMPOSE = $(DOCKER_COMPOSE_DEV)

VENV = venv
PIP = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python

JUPYTER_DOCKER_COMPOSE = NB_UID="$(NB_UID)" NB_GID="$(NB_GID)" $(DOCKER_COMPOSE)
JUPYTER_RUN = $(JUPYTER_DOCKER_COMPOSE) run --rm jupyter

PEERTAX_JUPYTER_PORT = 8891

NB_UID = $(shell id -u)
NB_GID = $(shell id -g)

ARGS =


venv-clean:
	@if [ -d "$(VENV)" ]; then \
		rm -rf "$(VENV)"; \
	fi


venv-create:
	python3 -m venv $(VENV)


dev-install:
	$(PIP) install -r requirements.jupyter.txt
	$(PIP) install -r requirements.txt


dev-nlp-model-download:
	$(PYTHON) -m spacy download en_core_web_sm
	$(PYTHON) -m spacy download en_core_web_lg
	$(PYTHON) -m nltk.downloader stopwords


dev-venv: venv-create dev-install dev-nlp-model-download


dev-jupyter-configure:
	$(VENV)/bin/jupyter nbextension enable --py widgetsnbextension


dev-jupyter-start: dev-jupyter-configure
	$(VENV)/bin/jupyter lab -y --port=$(PEERTAX_JUPYTER_PORT)


jupyter-build:
	@if [ "$(NO_BUILD)" != "y" ]; then \
		$(JUPYTER_DOCKER_COMPOSE) build jupyter; \
	fi


jupyter-shell: jupyter-build
	$(JUPYTER_RUN) bash


jupyter-start: jupyter-build
	$(JUPYTER_DOCKER_COMPOSE) up -d jupyter


jupyter-logs:
	$(JUPYTER_DOCKER_COMPOSE) logs -f jupyter


jupyter-stop:
	$(JUPYTER_DOCKER_COMPOSE) down
