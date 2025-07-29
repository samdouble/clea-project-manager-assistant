# project-manager-assistant (Cléa)

[![CI](https://github.com/samdouble/clea-project-manager-assistant/actions/workflows/checks.yml/badge.svg)](https://github.com/samdouble/clea-project-manager-assistant/actions/workflows/checks.yml)
[![PyPI version](https://img.shields.io/pypi/v/clea-pma)](https://pypi.org/project/clea-pma/)
[![Python](https://img.shields.io/pypi/pyversions/clea-pma)](https://pypi.org/project/clea-pma/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Coverage Status](https://coveralls.io/repos/samdouble/clea-project-manager-assistant/badge.svg?branch=master&service=github)](https://coveralls.io/github/samdouble/clea-project-manager-assistant?branch=master)

## Installation

Install from PyPI:
```sh
pip install clea-pma
```

## Setup

Optionally, create a `.env` file like this:
```
ANTHROPIC_API_KEY=
LINEAR_API_KEY=
```
If you don't, you are going to be asked the informations through the CLI.

Make sure you have Python 3.11 installed.

Install Poetry:
```sh
pip install poetry
```

Run in a terminal window:
```sh
poetry install
poetry run clea
```

Ask questions:
```
>: Hi Cléa, I'd like to see my issues for next cycle

>: How much points to you think the unestimated tasks are worth?
```

TODO
- Sauvegarder l'historique des conversations
- Faire un éxécutable pour simplifier l'installation
- Questions sur les projets
- Questions sur les membres de l'équipe



Hey Clea, what are my issues for next cycle?
I'd like to see the ones with an empty description
Could you try filling a description for one of these issues?

