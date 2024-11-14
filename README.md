# Information Pursuit: A Wikispeedia Analysis
Team *5Pack*.

**Abstract**
The Wikispeedia project explores human navigation patterns within a simplified Wikipedia network, analyzing how players find paths between articles using only hyperlinks. With a dataset of over 75,000 gameplay paths (51,000 completed, 25,000 abandoned), we aim to uncover the strategies players employ when navigating this knowledge network. Our analysis focuses on identifying navigation patterns, such as the use of hub articles and hierarchical thinking (e.g., moving from specific to general categories), and investigating how link positioning within articles influences player choices. By combining network analysis with behavioral data, we seek to understand what makes certain paths more challenging than others and how players' internal mental models of knowledge organization affect their navigation strategies. This research could provide insights into human information seeking behavior and potentially improve website navigation design.

## Research Questions
1. Wikispeedia network analysis:
   - To what extent do players rely on hub articles in their navigation?
   - Are certain types of hubs (e.g., geographical, temporal, categorical) more frequently used?
   - How does hub usage correlate with success rates?

2. Path Efficiency Analysis:
   - How do player-chosen paths compare to shortest possible paths?
   - What factors correlate with players abandoning their search?
   - Is there a relationship between path length and completion time?

3. Navigation Strategies:
   - Do players show evidence of hierarchical navigation (e.g., specific → general → specific)?
   - How does the position of links within articles affect player choices?
   - Do players prefer links at the beginning, middle, or end of articles?
   - Can we identify common patterns in successful vs. unsuccessful navigation attempts?
   - How diverse are the paths chosen for the same source-target pairs?

## Methods
1. Data Preprocessing and Network Analysis
   - Construct directed graph representation of the Wikispeedia website
   - Compute network metrics (centrality measures, clustering coefficients) to identify hubs
   - Extract link positions from HTML source code

2. Path Analysis
   - Compare actual paths with shortest paths found computationally
   - Develop metrics for path "efficiency" considering both length and completion time
   - Create visualization tools for path comparison and analysis
   - Analyze distribution of successful vs. abandoned paths

3. Player Strategy Analysis
   - Implement algorithms to detect hierarchical navigation patterns
   - Analyze correlation between link positions and player choices
   - Develop metrics for path similarity to identify common strategies
   - Create heat maps of most traversed edges/nodes

4. Statistical Analysis
   - Apply statistical tests to validate hypotheses about hub usage
   - Perform time series analysis on path completion times
   - Use clustering algorithms to identify distinct navigation strategies
   - Calculate confidence intervals for identified patterns

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

\
\
**Note:** we used [Claude](https://claude.ai) in order to refine the redaction of some parts of this README.
https://edstem.org/eu/courses/1490/discussion/130908
