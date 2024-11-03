## Setup

### Environment setup

We provide here the instructions for setting up the Python virtual environment using [Poetry](https://python-poetry.org).

In the root of this repository, run the following:
```
poetry config virtualenvs.in-project true
poetry install
```

The first line makes it easy to detect the right kernel for running the different notebooks.

### Data setup

Put the uncompressed Wikispeedia data in `data/`.