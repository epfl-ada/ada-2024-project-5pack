---
title: "The Wikipedia Game: Are We Playing It All Wrong?"
layout: default
---

**Abstract**
In the Wikispeedia game players are tasked to rapidly navigate from one article to another in a simplified Wikipedia network using hyperlinks. Using over 75,000 gameplay paths, we aim to uncover strategies players employ, such as using hub articles and hierarchical thinking. We also investigate how link positioning influences player choices. Combining network analysis with behavioral data, we seek to understand what makes paths challenging and how players’ knowledge organization affects navigation strategies. Finally, we contrast human strategies with optimal paths in the network, and craft some advice for the players.
{: #abstract }

## Introduction

[TODO: Explanation on the website and the data. Mention Stanford's page.]

<div id="wikispeedia-stats">
  <div>Wikispeedia Website</div>
  <div>
    <div>4.5k+ articles</div>
    <div>124k+ hyperlinks</div>
  </div>
</div>

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
The Wikispeedia dataset contains games of Wikispeedia. In this game, a player is given a pair of two articles present on the website, and his goal is to go from the first to the second article by taking hyperlinks on Wikispeedia.

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

[TODO Timothée, Fred, Peter]

{peter + timothee}

{faire plot distribution hub usage ratio}
{gabriel}

## Optimal strategy

[TODO Gabriel]

{analyse du shortest path}
{déterminer les stratégies qui correspondent}

## Conclusion

TODO
