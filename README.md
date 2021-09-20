# FastAPI Template

This repository serves as a demo for several Python libraries and design best practices.

## Features

- [FastAPI](https://fastapi.tiangolo.com/) Python web framework
- [Poetry](https://python-poetry.org/) Python dependency management
- [12 Factor](https://12factor.net/) design principles
- [Black](https://github.com/psf/black) Python code formatter

## Getting Started

Poetry is used to make development easy.
Follow the install instructions for Poetry.
In order to allow your IDE to easily find the python interpreter for the project, instruct Poetry to create the virtual environment in the project directory.
```
poetry config virtualenvs.in-project true
```
Then simply install the project dependencies.
```
poetry install
```