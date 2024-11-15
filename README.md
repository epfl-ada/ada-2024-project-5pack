# Information Pursuit: A Wikispeedia Analysis
Team *5Pack* - Applied Data Analysis 2024 EPFL

**Abstract**
The Wikispeedia project explores human navigation patterns within a simplified Wikipedia network, analyzing how players find paths between articles using only hyperlinks. With a dataset of over 75,000 gameplay paths (51,000 completed, 25,000 abandoned), we aim to uncover the strategies players employ when navigating this knowledge network. Our analysis focuses on identifying navigation patterns, such as the use of hub articles and hierarchical thinking (e.g., moving from specific to general categories), and investigating how link positioning within articles influences player choices. By combining network analysis with behavioral data, we seek to understand what makes certain paths more challenging than others and how players' internal mental models of knowledge organization affect their navigation strategies. This research could provide insights into human information seeking behavior and potentially improve website navigation design.

## Research Questions

1. To what extent do players rely on their world mental model in their navigation?
   - Are certain types of hubs (e.g., geographical, temporal, categorical) more frequently used?
   - How does hub usage correlate with success rates?

2. What impacts the most the success rates of the players?
   - How do player-chosen paths compare to shortest possible paths?
   - What factors correlate with players abandoning their search?
   - Is there a relationship between path length and completion time?

3. What common strategies distinguish humans from optimal paths?
   - Do players show evidence of hierarchical navigation (e.g., specific → general → specific)?
   - How does the position of links within articles affect player choices?
   - Can we identify common patterns in successful vs. unsuccessful navigation attempts?
   - How diverse are the paths chosen for the same source-target pairs?

## Additional Datasets

For this project, no additonal external dataset is required.
However, we do plan to work with LLMs in order to generate some data as needed. This is particularly handy for repetitive labeling work based on human knowledge. This is something we explore in order to understand what could drive users to prefer some hyperlinks to some others.

In `src/utils/llm.py` you will find that we successfully managed to setup the environment and can retrieve next token prediction distributions. One usage example is the automatic labelling of pairs of articles to bucket them in four distinct categories. This work is externalized from the core library in `src/scripts/generate_pairs_category.py` for efficiency reasons, as it still take quite some time to generate the data.

## Methods

1. Data Preprocessing and Network Analysis
   - Construct directed graph representation of the Wikispeedia website
   - Compute network metrics (centrality measures, clustering coefficients) to identify hubs
   - Extract link positions from HTML source code
   - We identified many of the tools we will use from NetworkX (page rank, HITS algorithm...) and lxml

2. Path Analysis
   - Develop metrics for path "efficiency" considering both length and completion time
   - Analyze distribution of successful vs. abandoned paths, and determine the most statistically significant features
   - At this step with plan to use ANOVA for Linear Models or Generalized Linear Models

3. Player Strategy Analysis
   - Implement algorithms to detect hierarchical navigation patterns
   - Analyze correlation between link positions and player choices
   - Develop metrics for path similarity to identify common strategies
   - Create heatmaps of most traversed edges/nodes
   - Use clustering algorithms to identify distinct navigation strategies
   - Subgames extraction already done through the analysis of paths
     (which we use/compare with actual games and determine interesting insights from)

\
**Note:** at the beginning we had the idea of analyzing data related to the time players spend on different articles during in their paths. It would have provided additional interesting insights about how they play, the potential impact of time-pressure, etc. However, this information is not present in the original dataset, so we dropped this idea but note that it could have given us some additional perspectives on human navigation patterns.

## Proposed timeline

There are five weeks between the deadline of the Milestone 2 and the final deadline of the project.

Details are subject to some changes, but as of today this is how we plan to organize our timeline, starting from next week:

Week 1: Further development of the initial exploratory work

Explore more deeply new ideas that came from the initial analysis performed for the Milestone 2. One example of this could be the use of spectral graph theory to complement our understanding of the extracted Wikispeedia graph.

Week 2: Brainstorming of the first findings

The second week will be used to brainstorm about our results so far. As an important point of research in general, we might adapt our schedule/direction depending on the results that we are getting. Especially here, taking a step back and estimating whether, a priory, our intuitions were right, will allow us to smoothly change the details of the main sections already determined by Milestone 2.

Week 3: Selection of the main points of focus

From this week onwards, we will be hardly slowing down the exploratory phase of the project. We anticipate to have enough directions already explored to start pruning our ideas/results and select the most promising/relevant ones. This will help us make sure that we build a coherent progression from the introduction of the project to the conclusion, answer the research questions we highlighted above.

Week 4: Preparation of the data story

Finalize the main notebook and the analysis to focus on the coherence of the story we want to tell.
Start choosing the most important visualizations we want to highlight and start preparing the website (using ADA Template or Jekyll).

Week 5: Finalization of the project

Remove any temporary code from GitHub and finalize the data story website on GitHub pages.
This will leave us with some extra time to review parts we were not able to anticipate.

## Organization within the team

Most of the content of the project will be put on this repository, apart from some files that help us in our meetings that we keep externally. One notebook keeps the sole purpose of being the general presentation and summary of the project (`analysis.ipynb`). Because of the way the notebooks are encoded, it is not straightforward to share notebooks between us via GitHub when working on our individual tasks. For this reason, the library is maintained and developed by all the team, but we decided to also work on individual notebooks, pushed to GitHub if needed.

## Quickstart for the project

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
│   └── scripts                         <- Shell scripts
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
