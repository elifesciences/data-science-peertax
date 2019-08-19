# PeerTax

This is a Data Science project looking into the Peer Review Taxonomy.

As open data sources it is looking at the reviews from [F1000](https://f1000research.com/) and validating against the [BMJ Open](https://bmjopen.bmj.com/).

## Setup

The project provides configuration for either using a Python virtual environment or Docker.

### Setup using Virtual Environment

#### Pre-requisites

- Python 3

#### Create Virtual Environment

```bash
make dev-venv
```

#### Run Tests

```bash
make dev-test
```

#### Start Jupyter

```bash
make dev-jupyter-start
```

### Setup using Docker

#### Pre-requisites (Docker)

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)

#### Build and start Jupyter

```bash
make jupyter-start
```

This will build the Jupyter image and and start it via Docker.

#### Run Tests (Docker)

```bash
make test
```

## Project Structure

The project is structured in the following directories:

- [data](data): data downloaded from other sources
- [LDA](LDA): Notebooks related to [LDA](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation)
- [notebooks](notebooks): Notebooks related to preprocessing the text (sentence and token splitting)
- [peertax](peertax): Python package used by the notebooks
- [pickles](pickles): Intermediate output files
- [scripts](scripts): Other scripts (to run LDA models in parallel)
- [tests](tests): Python tests for the [peertax](peertax) package
