import networkx as nx
import pandas as pd
import numpy as np

def pagerank(graph):
    #Pagerank algorithm using the graph of articles (without weights)
    pagerank_scores = nx.pagerank(graph, alpha=0.85)
    graph_pagerank = pd.DataFrame(list(pagerank_scores.items()), columns=['Article', 'Pagerank'])
    #Normalizing
    graph_pagerank['Generality_score'] = (graph_pagerank['Pagerank'] - graph_pagerank['Pagerank'].min()) / (graph_pagerank['Pagerank'].max()-graph_pagerank['Pagerank'].min())
    return graph_pagerank


def average_path(NUMBER_OF_BINS, paths):
    scores_bins = [[] for _ in range(NUMBER_OF_BINS+1)]

    #We have bins for every steps then add the scores that fall in that bin
    #For ex. if the path is of length 5 we will add step 1 to 1st bin, step 2 to 3rd, etc...
    for _, path in paths.iterrows():
        #This is the previously computed path of generality scores (for each step)
        generality_scores = path['Generality_score']
        bins = np.linspace(0, 1, len(generality_scores))

        for fraction, score in zip(bins, generality_scores):
            bin_index = int(fraction * NUMBER_OF_BINS) #Find bin where this falls
            scores_bins[bin_index].append(score)

    scores = [np.mean(scores) for scores in scores_bins]

    percent = [(100*i / NUMBER_OF_BINS) for i in range(NUMBER_OF_BINS+1)]

    return scores, percent