---
title: "The Wikipedia Game: Are We Playing It All Wrong?"
layout: default
---

**Abstract**
In the Wikispeedia game players are tasked to rapidly navigate from one article to another in a simplified Wikipedia network using hyperlinks. Using over 75,000 gameplay paths, we aim to uncover strategies players employ, such as using hub articles and hierarchical thinking. We also investigate how link positioning influences player choices. Combining network analysis with behavioral data, we seek to understand what makes paths challenging and how players’ knowledge organization affects navigation strategies. Finally, we contrast human strategies with optimal paths in the network, and craft some advice for the players.
{: #abstract }

## Introduction

This research is based on a dataset collected in the context of [Wikispeedia](https://dlab.epfl.ch/wikispeedia/play/){:target="_blank"}, a game where players are tasked to reach one article from another only using hyperlinks on a subset of Wikipedia. A quick analysis shows that humans are not optimal, as they usually take paths longers than the shortest paths, as they visit on average **x2.4** more articles than needed.

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

Quite naturally the network of articles reveals dominant subjects or articles in Wikispeedia.

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
          <tr><td>England</td><td>0.0112</td></tr>
          <tr><td>Africa</td><td>0.009</td></tr>
          <tr><td>Earth</td><td>0.008</td></tr>
          <tr><td>World War II</td><td>0.008</td></tr>
      </tbody>
  </table>
  </div>
</div>

The next community is **Computer Science 🤖** with only 124 articles.

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

{network analysis: fred, debut Peter (stats generales)}

## Players' strategies

### Hub-focused strategy

Among the players we discovered a first strategy that clearly splits them into two groups, and this has to do with the hub usage of the players. During their navigation, players tend to have different behaviors in the use of hubs. When hubs are defined to be the top 200 articles by highest page rank. Indeed, we see a clear drop in the pagerank score for top articles, indicating a gap in their importance in the Wikispeedia network.

To see that there is a clear pattern of paths going through general articles, we analyze the behavior for an average path.

<div class="plot">
  <iframe src="assets/plots/plot_gen.html" width="100%" height="550px" frameborder="0"></iframe>
</div>

It appears that paths follow a pattern as (specific -> general -> specific). This strategies appears very natural as we expect general articles to have more links. However players that have more knowledge might be able to take shortcuts and bypass these general articles, by finding more links between the source and target (for example, a path going from Albert Einstein to General Relativity could be shortened from Einstein -> Physics -> Relativity to Einstein -> Relativity if the player knows that Einstein is directly associated with the development of General Relativity).


{faire plot distribution hub usage ratio}
{gabriel}
[plot of distribution of page rank among the top articles]

We perfomed an analysis on all the finished paths to determine how different players use the hubs. We observe that, many players do not tend to use hubs as defined above, while the rest of the players exhibit a normal distribution around 0.5 in the hub usage ratio for their paths.

[plot of the distribution of hub usage ratio and show clearly the two modes]

### Semantic navigation strategy

In this strategy, the player will click on links to articles that are semantically closer to the target article.

We want to check whether the semantic similarity between the current article and the target article increases as players progress along their path. If this similarity grows, it would suggest that the player is following the strategy of selecting more semantically related articles.

We will do the following steps to answer that question:
1. Compute the TF-IDF matrix to represent the documents as embeddings
2. Compute the cosine similarity between two embeddings to assess how similar two articles are.
3. Verify whether the semantic similarity increases as players progress along their path. 

To do the last step, we use Spearman's rank correlation, which evaluates how well the order of semantic similarity aligns with a strictly increasing sequence. The correlation score ranges from -1 to 1, with 1 indicating a perfect monotonic increase in similarity. We will refer to this score as the semantic_increase_score (SIS).p

For instance computing the TF-IDF matrix will give us the following similarities for the top 5 articles:

<div class="plot">
  <iframe src="assets/plots/similarity_matrix.html" width="100%" height="550px" frameborder="0"></iframe>
</div>

Using this similarity matrix, we can compute how the similarity evolves as players progress along their path

<div class="plot">
  <iframe src="assets/plots/semantic_path_example.html" width="100%" height="550px" frameborder="0"></iframe>
</div>

Then, we can compute the final SIS score using Spearman's rank correlation. For instance, the SIS score for the above path is of **0.738** which indicates that the semantic similarity is generally increasing along the path.


### Link strategy

[Timothee]

Since time is the determining winning factor of the game, we consider a strategy to be to click among the first links of the page. We extract the links order from their position in the files, then we check if this strategy appears to be used by players of the game.

To illustrate how this strategy might pay off, we can take the example of the path in the introduction (Yarralumla -> Lincoln). The path goes through Australia and the United States, while United States appeared at the end of the wikipedia page of Yarralumla. So it is not the shortest path, but Australia appeared at the top of the page of Yarralumla, then United States at the top of Australia (since they are closed allies), which explains why the player solved the game quickly (53 seconds).

Since a significant portion of the clicks are among the top links of the page (which also accounts for the clicks on the side of the wikipedia web page), we can deduce that this strategy is used significantly among players who don't have the time to read through the whole page.

<div class="plot">
  <iframe src="assets/plots/pie_top_clicks.html" width="100%" height="550px" frameborder="0"></iframe>
</div>


We now compare players using this strategy consistently (i.e. making a significant amount of clicks on the top links) are performing better or worse than average. We compare the average completion time of 3 group of paths depending on the proportion of top clicks they have.

<div class="plot">
  <iframe src="assets/plots/link_barplot.html" width="100%" height="550px" frameborder="0"></iframe>
</div>

So clicking on the top links seems to be decreasing completion time. 



### Fast exploration

[Backtrack, Peter]

## Discussing the best strategy

To measure the strengths of each strategies, we will be comparing 2 metrics : success rate (among the paths using these strategies, how many are finished), and average completion time (the average time to finish the path).

<div class="plot">
  <iframe src="assets/plots/barplot_success.html" width="100%" height="550px" frameborder="0"></iframe>
</div>

<div class="plot">
  <iframe src="assets/plots/barplot_times.html" width="100%" height="550px" frameborder="0"></iframe>
</div>

The link strategy appears to have the shortest times while the semantic strategy has the best success rate. The hub strategy underperforms both of these strategies and also the average path, signaling that this strategy might be too naive and be used when players don't have a specific plan in mind.


[TODO Gabriel]

{analyse du shortest path}
{déterminer les stratégies qui correspondent}
<div class="plot">
  <iframe src="assets/plots/spearman_rank_length_graph.html" width="100%" height="620px" frameborder="0"></iframe>
</div>

## Conclusion


TODO
