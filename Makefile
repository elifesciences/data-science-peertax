DOCKER_COMPOSE_DEV = docker-compose
DOCKER_COMPOSE_CI = docker-compose -f docker-compose.yml
DOCKER_COMPOSE = $(DOCKER_COMPOSE_DEV)

VENV = venv
PIP = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python

JUPYTER_DOCKER_COMPOSE = NB_UID="$(NB_UID)" NB_GID="$(NB_GID)" $(DOCKER_COMPOSE)
JUPYTER_RUN = $(JUPYTER_DOCKER_COMPOSE) run --rm jupyter

PEERTAX_JUPYTER_PORT = 8891

PEERTAX_RUNNER_TAG = develop

NB_UID = $(shell id -u)
NB_GID = $(shell id -g)

ARGS =

LDA_ITER =
LDA_PASSES = 30
LDA_ITERATIONS = 1000
LDA_EVAL_EVERY = 10
LIMIT =
TASKS_MIN = 1
TASKS_LIMIT = 3

CLOUD_DATA_PATH =
GCP_PROJECT =
GCP_REGIONS = us-central1


venv-clean:
	@if [ -d "$(VENV)" ]; then \
		rm -rf "$(VENV)"; \
	fi


venv-create:
	python3 -m venv $(VENV)


dev-install:
	$(PIP) install -r requirements.jupyter.txt
	$(PIP) install -e .
	$(PIP) install -r requirements.dev.txt


dev-nlp-model-download:
	$(PYTHON) -m spacy download en_core_web_sm
	$(PYTHON) -m spacy download en_core_web_lg
	$(PYTHON) -m nltk.downloader stopwords


dev-venv: venv-create dev-install dev-nlp-model-download


dev-jupyter-configure:
	$(VENV)/bin/jupyter nbextension enable --py widgetsnbextension


dev-jupyter-start: dev-jupyter-configure
	$(VENV)/bin/jupyter lab -y --port=$(PEERTAX_JUPYTER_PORT)


dev-flake8:
	$(PYTHON) -m flake8 peertax tests setup.py


dev-pylint:
	$(PYTHON) -m pylint peertax tests setup.py


dev-lint: dev-flake8 dev-pylint


dev-pytest:
	$(PYTHON) -m pytest -p no:cacheprovider $(ARGS)


dev-watch:
	$(PYTHON) -m pytest_watch -- -p no:cacheprovider $(ARGS)


dev-test: dev-lint dev-pytest


.require-LDA_ITER:
	@if [ -z "$(LDA_ITER)" ]; then \
		echo "LDA_ITER required"; \
		exit 1; \
	fi


dev-run-lda-local: .require-LDA_ITER
	$(eval OUTPUT_DIRECTORY = ./data/lda-runs/f1000_LDA_Sentence_Run_$(LDA_ITER))
	$(eval LOGGING_DIR = $(OUTPUT_DIRECTORY)/logs)
	$(PYTHON) -m dsub.commands.dsub \
		--provider local \
		--logging "$(LOGGING_DIR)" \
		--input INPUT_FILE=./data/tokenized/peertax_f1000_tokenized_LDA_sentence_$(LDA_ITER).tsv \
		--output-recursive OUTPUT_DIRECTORY=$(OUTPUT_DIRECTORY) \
		--env LDA_PASSES=$(LDA_PASSES) \
		--env LDA_ITERATIONS=$(LDA_ITERATIONS) \
		--env LDA_EVAL_EVERY=$(LDA_EVAL_EVERY) \
		--env LIMIT=$(LIMIT) \
		--tasks scripts/tasks.tsv $(TASKS_MIN)-$(TASKS_LIMIT) \
		--image=elifesciences/data-science-peertax-runner:develop \
		--script ./scripts/lda_sentence_run.py \
		--wait
	cat $(LOGGING_DIR)/*
	ls -l $(OUTPUT_DIRECTORY)


.require-CLOUD_DATA_PATH:
	@if [ -z "$(CLOUD_DATA_PATH)" ]; then \
		echo "CLOUD_DATA_PATH required"; \
		exit 1; \
	fi


.require-GCP_PROJECT:
	@if [ -z "$(GCP_PROJECT)" ]; then \
		echo "GCP_PROJECT required"; \
		exit 1; \
	fi


dev-run-lda-cloud: .require-LDA_ITER .require-CLOUD_DATA_PATH .require-GCP_PROJECT
	$(eval OUTPUT_DIRECTORY = $(CLOUD_DATA_PATH)/lda-runs/f1000_LDA_Sentence_Run_$(LDA_ITER))
	$(eval LOGGING_DIR = $(OUTPUT_DIRECTORY)/logs)
	$(PYTHON) -m dsub.commands.dsub \
		--provider google-v2 \
		--project "$(GCP_PROJECT)" \
		--regions "$(GCP_REGIONS)" \
		--logging "$(LOGGING_DIR)" \
		--input INPUT_FILE=$(CLOUD_DATA_PATH)/peertax_f1000_tokenized_LDA_sentence_$(LDA_ITER).tsv \
		--output-recursive OUTPUT_DIRECTORY=$(OUTPUT_DIRECTORY) \
		--env LDA_PASSES=$(LDA_PASSES) \
		--env LDA_ITERATIONS=$(LDA_ITERATIONS) \
		--env LDA_EVAL_EVERY=$(LDA_EVAL_EVERY) \
		--env LIMIT=$(LIMIT) \
		--tasks scripts/tasks.tsv $(TASKS_MIN)-$(TASKS_LIMIT) \
		--image=elifesciences/data-science-peertax-runner:$(PEERTAX_RUNNER_TAG) \
		--script ./scripts/lda_sentence_run.py \
		--wait
	gsutil -l $(OUTPUT_DIRECTORY)


runner-build:
	@if [ "$(NO_BUILD)" != "y" ]; then \
		$(DOCKER_COMPOSE) build runner; \
	fi


runner-shell: runner-build
	$(DOCKER_COMPOSE) run --rm runner bash


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


pylint:
	$(JUPYTER_RUN) pylint peertax tests setup.py


flake8:
	$(JUPYTER_RUN) flake8 peertax tests setup.py


pytest:
	$(JUPYTER_RUN) pytest -p no:cacheprovider $(PYTEST_ARGS)


lint: \
	flake8 \
	pylint


test: lint pytest


ci-build-and-test:
	$(MAKE) DOCKER_COMPOSE="$(DOCKER_COMPOSE_CI)" jupyter-build test


ci-clean:
	$(DOCKER_COMPOSE_CI) down -v
