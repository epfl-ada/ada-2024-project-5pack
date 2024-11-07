# Your project name

## Quickstart

### Cloning the project.
```
mkdir <dir>
git clone git@github.com:epfl-ada/ada-2024-project-5pack.git <dir>
cd <dir>
```
where `dir` is a name of your choice.

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


### How to use the library

Tell us how the code is arranged, any explanation goes here.

### Code quality checks

We use [pre-commit](https://pre-commit.com) to ensure code quality for any contribution to this repository.

To run all the checks before trying to commit, use
```bash
pre-commit run --all-files
```

## Project structure

The directory structure of new project looks like this:

```
├── data                        <- Project data files
│
├── src                         <- Source code
│   ├── data                            <- Data directory
│   ├── models                          <- Model directory
│   ├── utils                           <- Utility directory
│   ├── scripts                         <- Shell scripts
│
├── tests                       <- Tests of any kind
│
├── results.ipynb               <- a well-structured notebook showing the results
│
├── .gitignore                  <- List of files ignored by git
├── .pyproject.toml             <- Configuration file for Poetry
└── README.md
```
