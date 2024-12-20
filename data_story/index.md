---
title: "The Wikipseedia Game: Are We Playing It All Wrong?"
layout: default
---

**Abstract**
The Wikispeedia game challenges players to navigate from one Wikipedia article to another using only hyperlinks. Through analysis of over 75,000 gameplay paths (51,000 completed, 25,000 abandoned), we investigate what makes a successful navigation strategy. Our findings show that players typically take paths 2.4 times longer than optimal, suggesting significant room for improvement in navigation strategies. We analyze several key strategies including hub-based navigation, semantic-guided choices, and backtracking patterns to determine their effectiveness. By combining network analysis with player behavior data, we aim to uncover what distinguishes successful navigation attempts from failures and provide insights into optimal playing strategies.
{: #abstract }

## Introduction

This research is based on a dataset collected in the context of [Wikispeedia](https://dlab.epfl.ch/wikispeedia/play/){:target="_blank"}, a game where players are tasked to reach one article from another only using hyperlinks on a subset of Wikipedia. A quick analysis shows that humans are not optimal, as they usually take paths longer than the shortest paths, as they visit on average **x2.4** more articles than needed.

<div class="plot">
  <iframe src="assets/plots/game_stats_intro.html" width="100%" height="550px" frameborder="0"></iframe>
</div>

This leads us to study the specificities of human navigation patterns in Wikipedia, and understand what the most efficient strategies are for browsing the Wikipedia network.

<div id="wikispeedia-stats">
  <div>Wikispeedia Website</div>
  <div>
    <div>4.5k+ articles</div>
    <div>124k+ hyperlinks</div>
  </div>
</div>

Quite naturally the network of articles reveals dominant subjects or articles in Wikispeedia. Some articles are more popular then others, thus connected to more articles. This is in adequation with humans' world model, where a topic like "Animal" would be the way more general than more specific things like "keyboard". Intuitively, players might want to pass by these articles early in their search to expand the tree of reachable articles, before diving to their target article. Using Leiden and PageRank algorithms, we determine the following important communities and articles in the network:

<div id="side-by-side-plots">
  <iframe src="assets/plots/communities_graph.html" width="100%" height="550px" frameborder="0"></iframe>
  <div>
    <p style="text-align:center;color:black;margin-top:38px;">Main hubs</p>
    <table style="display:table;table-layout:fixed;width: 100%;">
      <thead>
          <tr>
              <th>Article</th>
              <th>Pagerank Score</th>
          </tr>
      </thead>
      <tbody>
          <tr><td>United States</td><td>0.032</td></tr>
          <tr><td>Europe</td><td>0.014</td></tr>
          <tr><td>United Kingdom</td><td>0.014</td></tr>
          <tr><td>England</td><td>0.012</td></tr>
          <tr><td>Africa</td><td>0.009</td></tr>
          <tr><td>Earth</td><td>0.008</td></tr>
          <tr><td>World War II</td><td>0.008</td></tr>
      </tbody>
  </table>
  </div>
</div>

The next community is **Computer Science 🤖** with only 124 articles, far from the previous communities of articles. As seen above, main articles are linked to the main communities of articles, which makes sense as articles flourish around these subjects in the Wikispeedia and Wikipedia network.

### Game Data
The Wikispeedia dataset contains games of Wikispeedia. In this game, a player is given a pair of two articles present on the website, and his goal is to go from the first to the second article by taking hyperlinks on Wikispeedia. The dataset contains paths taken by the players for different games and players and their overall time.

**Example** Joining *Yarralumla* to *Abraham Lincoln*\
Done in 56 seconds as follows
<div class="path-example">
    <div>Yarralumla</div>
    <div>Australia</div>
    <div>United States</div>
    <div>Abraham Lincoln</div>
</div>

Importantly, we have access to both finished paths (i.e. when the target was reached, with the corresponding time) and unfinished paths. It is important to consider the latter to avoid survival bias as they also contain relevant information about the difficulty of paths and success measures of different game strategies.

## Players' strategies

We analyze here the different strategies of the players found from this dataset, understand their impact on the game results, and explain the efficiency of different strategy profiles for different kind of (source, target) pairs.

### Hub-focused strategy

In this strategy, we hypothesize that players navigate through "hub" articles - highly connected articles that serve as navigation landmarks in the Wikspeedia network. To identify these hubs, we use **PageRank**, which ranks articles based on their centrality and importance in the network. Thus, using this strategy, players can access a broad set of connections and navigate closer to the target. We then analyze whether players tend to use these hub articles in their successful navigation paths.
To see that there is a clear pattern of paths going through general articles, we analyze the behavior for an average path.

<div class="plot">
  <iframe src="assets/plots/plot_gen.html" width="100%" height="550px" frameborder="0"></iframe>
</div>

We define the generality score as the pageRank score of that article over the max pageRank score across all articles. It appears that paths follow a pattern as (specific -> general -> specific). This strategies appears very natural as we expect general articles to have more links. However, players that have more knowledge might be able to take shortcuts and bypass these general articles, by finding more links between the source and target, and that is generally how the shortest paths are formed in the network (for example, a path going from Albert Einstein to General Relativity could be shortened from Einstein -> Physics -> Relativity to Einstein -> Relativity if the player knows that Einstein is directly associated with the development of General Relativity).


<div class="plot">
  <iframe src="assets/plots/pagerank_distribution.html" width="100%" height="550px" frameborder="0"></iframe>
</div>

The choice of the top 200 articles as hubs is justified by both theoretical and empirical observations. **PageRank scores in networks often follow a power-law distribution**, where a small fraction of nodes (articles, in this case) capture a disproportionately large share of the network's importance. This is clearly visible in the distribution plot, where the PageRank scores sharply decline after the top-ranked articles.

The top 200 articles (representing only 4.3% of all articles) account for 44.1% of the total PageRank score. This aligns with the **scale-free property** of networks, where a few highly connected and influential nodes dominate the network structure. These hubs serve as natural navigation location, providing efficient access to many other articles.

By selecting the top 200 articles, we balance between capturing the most influential hubs and maintaining a manageable set. Including too many articles would dilute the concept of "hub" and reduce the navigation strategy's precision.

Moreover, examining the top 5 hubs **—United States, Europe, United Kingdom, England, and Africa—** reveals that they are broad, general-knowledge topics that naturally act as checkpoints for navigation. Beyond these, the PageRank scores drop significantly (from 0.032 for United States to 0.0093 for Africa). This supports the 200-article cutoff as an optimal choice.

To quantify the extent to which players rely on hubs in their navigation paths, we define the **Hub Usage Ratio (HUR)** as follows:

$$
\text{Hub Usage Ratio (HUR)} = \frac{\text{Number of Hub Articles in the Path}}{\text{Total Number of Articles in the Path}}
$$

Where:
- **Hub Articles**: Articles in the top 200 by PageRank.
- **Path**: The sequence of articles visited by the player during navigation.

This metric allows us to evaluate the degree to which players utilize hubs in their navigation. For example:
- A **HUR of 1.0** indicates that the player's path consists entirely of hub articles.
- A **HUR of 0.0** indicates that no hub articles were used in the path.

<div class="plot">
  <iframe src="assets/plots/hub_usage_ratios.html" width="100%" height="550px" frameborder="0"></iframe>
</div>

This plot shows that finished paths tend to have a higher mean Hub Usage Ratio (HUR) compared to unfinished paths, suggesting that using hubs is a key factor in successful navigation.

### Semantic navigation strategy

In this strategy, the player will click on links to articles that are semantically closer to the target article.

We want to check whether the semantic similarity between the current article and the target article increases as players progress along their path. If this similarity grows, it would suggest that the player is following the strategy of selecting more semantically related articles.

We will do the following steps to answer that question:
1. Compute the TF-IDF matrix to represent the documents as embeddings
2. Compute the cosine similarity between two embeddings to assess how similar two articles are.
3. Verify whether the semantic similarity increases as players progress along their path. 

To do the last step, we use Spearman's rank correlation, which evaluates how well the order of semantic similarity aligns with a strictly increasing sequence. The correlation score ranges from -1 to 1, with 1 indicating a perfect monotonic increase in similarity. We will refer to this score as the semantic_increase_score (SIS).

For instance computing the TF-IDF matrix will give us the following similarities for a given set of 5 articles:

<div class="plot">
  <iframe src="assets/plots/similarity_matrix.html" width="100%" height="550px" frameborder="0"></iframe>
</div>

Similarly, we can compute how the similarity evolves as players progress along their path.

<div class="plot">
  <iframe src="assets/plots/semantic_path_example.html" width="100%" height="550px" frameborder="0"></iframe>
</div>

Then, we can compute the final SIS score using Spearman's rank correlation. For instance, the SIS score for the above path is of **0.738** which indicates that the semantic similarity is generally increasing along the path. Computing the score on all paths, we find an average SIS score of **0.82** for finished paths and **0.65** for unfinished paths. Computed on the last 50% of each path, the scores drop to **0.69** and **0.43** respectively. This goes well with our intuition that unfinished paths tend to occur when players go semantically further from the target articles than for finished paths. Even if they are not able to reach the target, they also tend to not get closer to it at every step.

### Link strategy

Since time is the determining winning factor of the game, we consider a strategy to be to click among the first links of the page. We extract the links order from their position in the files, then we check if this strategy appears to be used by players of the game.

Since a significant portion of the clicks are among the top links of the page (which also accounts for the clicks on the side of the wikipedia web page), we can deduce that this strategy is used significantly by players, who probably don't have time to read through the whole page.

<div class="plot">
  <iframe src="assets/plots/pie_top_clicks.html" width="100%" height="550px" frameborder="0"></iframe>
</div>


We now compare players using this strategy consistently (i.e. making a significant amount of clicks on the top links), to see if they are performing better or worse than average. We compare the average completion time of 3 group of paths depending on the proportion of top clicks they have.

<div class="plot">
  <iframe src="assets/plots/link_barplot.html" width="100%" height="550px" frameborder="0"></iframe>
</div>

So clicking on the top links seems to be decreasing completion time. 



### Backtrack strategy

The **Backtrack Strategy** aims to quantify exploratory behavior in navigation paths by analyzing how frequently players revisit previously visited nodes (backtracking). This behavior is measured using the **Backtrack Ratio (BR)**.

The Backtrack Ratio (BR) is defined as:

$$
BR = \frac{\text{Number of Backtrack Steps in Path}}{\text{Total Number of Steps in Path}}
$$

Where:
- **Backtrack Steps**: Moves represented by `<` in the path.
- **Total Steps**: All moves in the path, including backtracks.

<div class="plot">
  <iframe src="assets/plots/backtrack_analysis.html" width="100%" height="550px" frameborder="0"></iframe>
</div>

The distribution of backtrack ratios reveals insights into player navigation strategies:

1. **Limited Backtracking**:
   - Most paths have very low backtrack ratios, with a significant spike at \( BR = 0 \), indicating players largely prefer forward navigation.

2. **Finished vs. Unfinished Navigation**:
   - **Finished Paths** (67.4%): Tend to cluster around BR = 0 with a lower mean backtrack ratio (green dashed line), reflecting more efficient navigation.
   - **Unfinished Paths** (32.6%): Spread across higher BR values, with a higher mean backtrack ratio (red dashed line), indicating more exploratory behavior.


## Discussing the best strategy

To measure the strengths of each strategies, we will be comparing 2 metrics : success rate (among the paths using these strategies, how many are finished), and average completion time (the average time to finish the path).

<div class="plot">
  <iframe src="assets/plots/barplot_success.html" width="100%" height="550px" frameborder="0"></iframe>
</div>

<div class="plot">
  <iframe src="assets/plots/barplot_times.html" width="100%" height="550px" frameborder="0"></iframe>
</div>

The link strategy appears to have the shortest times while the semantic strategy has the best success rate. Backtracking is increasing the time significantly, which makes sense because returning from an article takes time. We also note that while going through the most important hubs is associated with lower completion time, it is also associated with lower success rates. This is maybe because this strategy is also used by players who don't have a specific goal in mind and are trying to go to articles that they are familiar with.

### Causal Analysis

The previous two evaluation metrics provide a straightforward way to analyze the performance of each strategy.

However using global metrics like success rate and completion time might lead to misleading results because of —you guessed it—**confounding variables 😈**. One major confounder here is game difficulty: harder games naturally take longer to complete. If players tend to use a strategy in more challenging games, the average game time might be increased, even if the strategy is actually helpful. Conversely, if the strategy is primarily used in easier games, its effectiveness might appear exaggerated.

<div style="text-align:center;">
  <img src="assets/images/confounding1.png" alt="Diagram of current situation" style="width:80%;">
</div>

To address this issue, we can compare the effect of using (vs. not using) the strategy on games with the same (source, target) pair. By isolating comparisons to identical game pairs, we remove the influence of difficulty differences caused by the specific pair. This way, if the strategy consistently performs better within the same pair, we can confidently say it’s not because of a confounding variable like game difficulty.

<div style="text-align:center;">
  <img src="assets/images/confounding2.png" alt="Diagram of current situation" style="width:70%;">
</div>

Unfortunately, grouping games by (source, target) pairs has a big downside: it results in a huge loss of data. Most (source, target) pairs are only played once, so they would get discarded! To solve this, we decided to simplify our approach by grouping on just the target article to quantify game difficulty. This decision wasn’t random—it came after hours of playing Wikispeedia and noticing something interesting:

The difficulty of a game depends **mostly** on the target article and **barely** on the starting article.

Here’s why: Imagine the very isolated article "Black Robin" 🐦‍⬛.
+ If "Black Robin" is the starting article, it’s not a big deal—you can quickly hop to "Animal," a great hub, and move on from there.
+ But if "Black Robin" is the target article, you’re in trouble. Getting to an isolated article from another location is significantly harder!

Therefore, in the subsequent analysis, all metrics are calculated with the confounding variable carefully accounted for.

### Regression Analysis

Now, let's start analyzing the performance of strategy profiles.

To do that, we will use regression analysis. While using OLS might sound tempting, it doesn’t account for confounding factors such as the varying difficulty of reaching different target articles. To address this, we’ll use a more robust approach: the **Mixed Linear Model**. This model introduces a "random effect" term to account for the variability introduced by different target articles.

Let's take a look at Mixed Linear Model equation:

$$
\text{Game Time}_{ij} = \beta_0 + \beta_1 \cdot \text{semantic_increase_score}_{ij} + \beta_2 \cdot \text{top_links_usage_ratio}_{ij} + \beta_3 \cdot \text{hub_ratio}_{ij} + \beta_4 \cdot \text{backtrack_ratio}_{ij} + \text{interaction effects} + u_{i} + \epsilon
$$

Where, for a given path $j$ ending at target $i$:
- $\beta_0$ is the fixed intercept, representing the average game time when all predictors are zero.
- $\beta_1, \beta_2, \beta_3, \beta_4$: Fixed effects for the strategies. These coefficients measure the global effectiveness of each strategy.
- $\text{interaction effects}$: Interaction terms between predictors, chosen using the **backward selection** algorithm. This ensures that only statistically significant interactions are included. Those terms will help us analyze how strategies influence each other.
- $u_i$: The random effect for the i-th target, capturing the difficulty of reaching that target.
- $\epsilon_{ij}$: Residual error term.

Great! Now let us look at the results:

```
                              Mixed Linear Model Regression Results
=================================================================================================
Model:                        MixedLM           Dependent Variable:           duration_in_seconds
No. Observations:             50138             Method:                       REML               
No. Groups:                   3323              Scale:                        11902.8300         
Min. group size:              1                 Log-Likelihood:               -308371.8628       
Max. group size:              1123              Converged:                    Yes                
Mean group size:              15.1                                                               
-------------------------------------------------------------------------------------------------
                                                   Coef.   Std.Err.    z    P>|z|  [0.025  0.975]
-------------------------------------------------------------------------------------------------
Intercept                                          156.099    1.097 142.259 0.000 153.949 158.250
semantic_increase_score                            -21.262    0.546 -38.934 0.000 -22.332 -20.191
top_links_ratio                                     -8.163    0.549 -14.875 0.000  -9.239  -7.088
hub_ratio                                            2.414    0.639   3.776 0.000   1.161   3.667
backtrack_ratio                                     37.520    0.626  59.965 0.000  36.293  38.746
semantic_increase_score:hub_ratio                   -2.337    0.512  -4.564 0.000  -3.341  -1.333
semantic_increase_score:backtrack_ratio             -4.617    0.656  -7.042 0.000  -5.902  -3.332
top_links_ratio:hub_ratio                           -2.939    0.493  -5.961 0.000  -3.905  -1.972
hub_ratio:backtrack_ratio                           -4.099    0.651  -6.299 0.000  -5.374  -2.824
semantic_increase_score:hub_ratio:backtrack_ratio   -2.983    0.620  -4.809 0.000  -4.199  -1.767
Group Var                                         2448.012    0.979                              
=================================================================================================
```

Let's analyze those results:
- $\beta_1 = -21.3$: The coefficient for the _semantic increase score (SIS)_ suggests that having a semantic increase score of 1 decreases the average game completion time by 21 seconds. That’s an impressive reduction!
- $\beta_2 = -8.2$: A high _top links click ratio_ also decreases completion time on average, but to a lesser extent compared to SIS
- $\beta_3 = 2.4$: A high _hub usage_ does not seem to improve the completion time
- $\beta_4 = 37.5$: _Backtracking_, on the other hand, has a significant negative impact, increasing the game time by 37.5 seconds on average for a backtracking ratio of 1. This number makes sense in some ways as spending too much time backtracking can be a waste of precious time.

Furthermore, all of the p-values are close 0 which is great news as this indicate that the results are statistically significant.

Below is a tool to visualize how adhering to a particular strategy affects the average game duration

<div class="__vue-root player"></div>

Another advantage of the Mixed Linear Model is that it allows us to extract the random effect term for each target. This term captures how difficult it is to reach a particular target, independent of the strategies used.

<div class="plot">
  <iframe src="assets/plots/random_effect.html" width="100%" height="550px" frameborder="0"></iframe>
</div>

For instance, the target article with the highest random effect is _Cultural Diversity_, which has a random effect value of 210. This means that games ending at _Cultural Diversity_ take, on average, 210 seconds longer than the typical game duration. Upon closer examination, we observe that the article _Cultural Diversity_ has an in-degree of only one, and is only reachable from the article _Globalization_. This limited connectivity makes _Cultural Diversity_ particularly challenging to reach!

Finally, the interaction effect terms provide information into how strategies influence each other when used in combination. To explain this better, let's take a closer look at the hub usage ratio:

<div class="plot">
  <iframe src="assets/plots/hubs_impact.html" width="100%" height="550px" style="overflow:hidden" frameborder="0"></iframe>
</div>

On its own, a higher hub ratio tends to increase the average game duration. However, when combined with other strategies, it will trigger an interaction term that will reduce the average game time.


[TODO Gabriel]

We have measured the efficiency of strategies in terms of completion time and in terms of path length.

We will now measure them considering the length of the path.
This metric has the advantage that we are allowed to **explode** the game paths which allows us to increase
the number of datapoints.
To explain what we mean by exploding the game paths, let's consider the following game from `Global warming` to `Sun`:

```
Global warming > Greenhouse effect > Planet > Sun
```
Indeed, everytime thee player clicks on a new article, the player then starts to look for ways to reach
the target from the new article, which effectively means that it is playing a game from the current article
to the target.
Thus, we can **explode** the previous game into three different games:
```
Global warming > Greenhouse effect > Planet > Sun
Greenhouse effect > Planet > Sun
Planet > Sun
```
Increasing the number of datapoints has multiple advantages:
- The statistical significance of our general results is improved.
- We can condition our computations on (source, target) pairs and still have statistically significant results, which allows us to mitigate the fact that different (source, target) pairs might inherently have higher/lower difficulty and encourage specific strategies.

{analyse du shortest path}
{déterminer les stratégies qui correspondent}
```
Bird > Bird migration > El Niño-Southern Oscillation > Global warming > Solar System > Sun 
```
<div class="plot">
  <iframe src="assets/plots/spearman_rank_length_graph.html" width="100%" height="1040px" frameborder="0"></iframe>
</div>

<div class="plot">
  <iframe src="assets/plots/strategies_combinations.html" width="100%" height="550px" frameborder="0"></iframe>
</div>

## Conclusion

Our analysis reveals that while players aren't necessarily playing Wikispeedia "wrong," there's significant room for improvement in navigation strategies. The data shows that players typically take paths 2.4 times longer than optimal, suggesting that most players aren't using the most efficient strategies.
Through our analysis of different navigation approaches, we've identified several key factors about effective gameplay strategies:

1. Semantic Navigation emerges as the most successful strategy overall:
- It shows the highest success rate among all strategies. 
- The Mixed Linear Model confirms that increasing semantic similarity to the target reduces completion time by 21 seconds on average. 
- This suggests players should prioritize choosing articles semantically related to their target
2. Link Position Strategy proves surprisingly effective:
- Clicking top-positioned links reduces completion time by about 8 seconds
- 44.9% of all clicks are on the top 20% of links
- This indicates that quick scanning and using prominent links is more time-efficient than thorough article reading
3. Hub Usage requires careful consideration:
- While hub articles (like "United States" or "Europe") are natural navigation landmarks, using them alone isn't optimal
- Hub strategy becomes more effective when combined with other approaches, particularly semantic navigation
- This suggests hubs should be used as stepping stones rather than the primary navigation method
4. Backtracking should be minimized:
- Excessive backtracking significantly increases completion time (37.5 seconds per unit of backtrack ratio)
- Finished paths show notably lower backtrack ratios than unfinished ones, suggesting that unfinished paths may result from players getting lost or lacking a clear navigation strategy.
- This indicates that confident, forward-moving navigation is generally more successful

The optimal approach appears to be a hybrid strategy that:

- Prioritizes semantically relevant articles
- Makes use of prominent links
- Uses hubs strategically rather than exclusively
- Minimizes backtracking through confident forward progression

So while we're not playing entirely wrong, we could be playing much better. The key to improved performance lies not in following any single strategy, but in combining these approaches intelligently based on the specific navigation challenge at hand.
