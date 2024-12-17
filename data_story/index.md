---
title: "The Wikipedia Game: Are We Playing It All Wrong?"
layout: default
---

**Abstract**
In the Wikispeedia game players are tasked to rapidly navigate from one article to another in a simplified Wikipedia network using hyperlinks. Using over 75,000 gameplay paths, we aim to uncover strategies players employ, such as using hub articles and hierarchical thinking. We also investigate how link positioning influences player choices. Combining network analysis with behavioral data, we seek to understand what makes paths challenging and how players’ knowledge organization affects navigation strategies. Finally, we contrast human strategies with optimal paths in the network, and craft some advice for the players.
{: #abstract }

## Introduction

This research is based on a dataset collected in the context of [Wikispeedia](https://dlab.epfl.ch/wikispeedia/play/){:target="_blank"}, a game where players are tasked to reach one article from another only using hyperlinks on a subset of Wikipedia. A quick analysis shows that humans are not optimal, as they usually take paths longers than the shortest paths, as they visit on average **x2.4** more articles than needed. This leads us to study the specificities of human navigation patterns in Wikipedia, and understand what the most efficient strategies are for browsing the Wikipedia network.

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
              <th>HITS Score</th>
          </tr>
      </thead>
      <tbody>
          <tr><td>United States, North America</td><td>0.0546, 0.0266</td></tr>
          <tr><td>Europe</td><td>0.0302</td></tr>
          <tr><td>Earth</td><td>0.0210</td></tr>
          <tr><td>United Kingdom, England</td><td>0.0177, 0.0163</td></tr>
          <tr><td>English language</td><td>0.0171</td></tr>
          <tr><td>World War II</td><td>0.0145</td></tr>
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

[plot of distribution of page rank among the top articles]

We perfomed an analysis on all the finished paths to determine how different players use the hubs. We observe that, many players do not tend to use hubs as defined above, while the rest of the players exhibit a normal distribution around 0.5 in the hub usage ratio for their paths.

[plot of the distribution of hub usage ratio and show clearly the two modes]

### Semantic navigationm

[Frederic]

### Link strategy

[Timothee]

### Fast exploration

[Backtrack, Peter]

## Optimal strategy

[TODO Gabriel]

{analyse du shortest path}
{déterminer les stratégies qui correspondent}

## Conclusion

TODO
