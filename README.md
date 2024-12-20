# Are We Playing Wikispeedia All Wrong?
Team *5Pack* - Applied Data Analysis 2024 EPFL
[**Visit the Project Website**](https://epfl-ada.github.io/ada-2024-project-5pack/)

## Abstract
The Wikispeedia game challenges players to navigate from one Wikipedia article to another using only hyperlinks. Through analysis of over 75,000 gameplay paths (51,000 completed, 25,000 abandoned), we investigate what makes a successful navigation strategy. Our findings show that players typically take paths 2.4 times longer than optimal, suggesting significant room for improvement in navigation strategies. We analyze several key strategies including hub-based navigation, semantic-guided choices, and backtracking patterns to determine their effectiveness. By combining network analysis with player behavior data, we aim to uncover what distinguishes successful navigation attempts from failures and provide insights into optimal playing strategies.

## Research Questions

### 1. How does the network structure impact navigation behavior?
- What role do **hub articles** play in guiding players’ navigation? Are hubs central to successful paths?
- Do players exhibit **hierarchical navigation patterns**, moving from specific to general topics before narrowing down to the target?
- How does the **connectivity of articles** (e.g., isolated articles or low in-degree nodes) contribute to game difficulty?

### 2. Which navigation strategies improve success rates?
- How effective are the following strategies:
  - **Hub-based navigation**: Relying on high-PageRank nodes.
  - **Semantic guidance**: Choosing links that are semantically closer to the target.
  - **Link positioning**: Clicking on top-ranked hyperlinks within the page.
  - **backtracking behavior**: Going back to previous articles, more streamlined or exploratory path.

### 3. How can navigation strategies be quantified and evaluated?
- Can we model the effectiveness of strategies using regression analysis to account for **confounding variables** like target difficulty?
- How do random effects (e.g., target article difficulty) influence the success of navigation strategies?

## Additional Datasets
No additional external datasets required. We leverage network analysis tools (NetworkX for PageRank, centrality measures) and natural language processing techniques (TF-IDF for semantic analysis) to extract insights from the existing Wikispeedia dataset.

## Methods

### 1. Strategy Analysis Framework

To evaluate player navigation behavior, we focus on four core strategies:

- **Hub Strategy**: Analyze the extent to which players rely on high-PageRank articles (hub nodes) as navigation landmarks. These hubs represent highly connected and influential articles in the Wikipedia network.
- **Semantic Strategy**: Measure the semantic similarity between articles using TF-IDF embeddings and cosine similarity. This assesses whether players select links that progressively move closer in meaning to the target.
- **Link Position Strategy**: Investigate whether players prioritize clicking on links located at the top of the page and the impact of this behavior on navigation efficiency.
- **Backtracking Analysis**: Quantify exploratory behavior by analyzing the frequency and impact of revisiting previously visited articles. This behavior is captured using the **Backtrack Ratio**.

### 2. Performance Metrics

To measure the effectiveness of these strategies, we employ the following metrics:

- **Hub Usage Ratio (HUR)**: The proportion of high-PageRank articles in a navigation path.
- **Semantic Increase Score (SIS)**: Spearman’s rank correlation to quantify whether semantic similarity increases as players approach the target.
- **Top Links Click Ratio**: The proportion of clicks on top-ranked hyperlinks within articles.
- **Backtrack Ratio (BR)**: The ratio of backtracking steps to total steps in a path.

### 3. Comparative Analysis

We evaluate the performance of navigation strategies by analyzing:

- **Success Rates**: The proportion of completed paths for each strategy.
- **Completion Times**: The average time taken to complete a path under each strategy.

### 4. Regression Analysis

To quantify and isolate the effects of navigation strategies, we use a **Mixed Linear Model (MLM)** that accounts for confounding variables, such as target article difficulty. The MLM is defined as:

$GameTime_{ij} = \beta_0 + \beta_1 \cdot SIS_{ij} + \beta_2 \cdot TopLinksRatio_{ij} + \beta_3 \cdot HUR_{ij} + \beta_4 \cdot BR_{ij} + interaction terms + u_i + \epsilon_{ij}$

Where:

- $\beta_0$ is the intercept (baseline completion time).
- $\beta_1, \beta_2, \beta_3, \beta_4$ are coefficients representing the global effects of the strategies.
- ***Interaction terms***: Statistically significant interactions (e.g., $\text{SIS} \times \text{HUR}$) are identified through backward selection to evaluate how strategies influence each other.
- $u_i$ captures random effects (e.g., difficulty of the target article).
- $\epsilon_{ij}$ represents the residual error.

We use backward selection in our regression analysis to identify significant predictors and ensure that the strategies we include in the model are not highly correlated, allowing us to isolate the independent effects of each strategy on game performance.

Thus, this model allows us to:

- Compare strategy effectiveness while controlling for game difficulty.
- Quantify the impact of individual strategies on navigation success and efficiency.

## Timeline

Week 1: Prepare the dataset, set up the workflow, and implement strategy metrics.

Week 2: Perform network analysis, generate initial statistics, and compare strategies.

Week 3: Refine visualizations and develop the data story framework.

Week 4: Conduct causal analysis, build the mixed linear model, and apply backward selection.

Week 5: Finalize regression analysis, polish the report, and complete visualizations.

## Organization

- Peter: Problem formulation, Implementing and analyzing the Hub Strategy and Backtrack Strategy, refining methodologies, writing the conclusion and coding up the algorithms.
- Gabriel: Conducting shortest path analysis, generating initial statistics, analyzing the connectivity of articles and assisting in evaluating article centrality metrics such as PageRank
- Timothée: Implementing the Link Position Strategy and contributing to discussions on identifying the best strategy and coding up the algorithms.
- Frédéric: Performing Causal/Regression with backward selection Analysis, implementing the Semantic Strategy and coding up the algorithms.
- Antoine: Writing the introduction, setting up the website and workflow, implementing backward selection in regression analysis, and creating JavaScript-based regression plots.
- Team: Defining performance metrics, producing most visualizations, and collaboratively writing the final report and data story.

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
│   ├── utils                           <- Utility directory contains all the strategies=
│   └── scripts                         <- Shell scripts + plotting
│
│
├── results.ipynb               <- a well-structured notebook showing the results
│
├── .gitignore                  <- List of files ignored by git
├── .pyproject.toml             <- Configuration file for Poetry
├── README.md
├── setup_website_**.sh         <- Used to install dependencies for website setup
└── WEBSITE_SETUP.md            <- How to setup the website and get the plots locally
```

\
\
**Note:** we used [Claude](https://claude.ai) in order to refine the redaction of some parts of this README.
https://edstem.org/eu/courses/1490/discussion/130908
