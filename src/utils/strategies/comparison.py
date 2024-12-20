from src.utils.strategies.semantic_strategy import semantic_increase_score

from src.utils.metrics import pagerank
from src.utils.strategies.link_strategy import get_click_positions, get_probability_link

import pandas as pd


def build_comparison_df(graph_data, all_links_dict, top_hubs = 200, threshold_semantic = 0.8, threshold_link = 0.8):
    graph_pagerank = pagerank(graph_data['graph'])
    article_gen_score = graph_pagerank.set_index('Article')['Generality_score']
    sorted_scores = article_gen_score.sort_values(ascending=False)
    score_threshold = sorted_scores.iloc[top_hubs]

    article_gen_score = graph_pagerank.set_index('Article')['Generality_score']
    
    # Remove < from path (but keep the articles that the person attempted to go to)
    graph_data['paths_finished']['path'] = graph_data['paths_finished']['path'].apply(lambda x: [u for u in x if u != '<'])
    graph_data['paths_unfinished']['path'] = graph_data['paths_finished']['path'].apply(lambda x: [u for u in x if u != '<'])
    
    
    
    fin_list = []
    
    for _, row in graph_data['paths_finished'].iterrows():
        
        path = row['path']
        time = row['duration_in_seconds']
        click_positions = get_click_positions(pd.DataFrame({'path': [path]}))
        prob = get_probability_link(click_positions)
        semantic, pval = semantic_increase_score(path, row['target'])
        max_gen = article_gen_score.loc[path].max()
        if len(path) < 4 or semantic < 0 or len(path) > 100:
            continue #A path too short, too long, or that progressively gets further from target doesn't make sense and will be ignored
        fin_list.append({
            'source': row['source'],
            'target': row['target'],
            'path': path,
            'time': time,
            'finished': True,
            'link_percentage': prob, 
            'num_clicks': len(path),
            'top_link_usage': prob > threshold_link,
            'semantic' : semantic > threshold_semantic,
            'max_generality' : max_gen > score_threshold
    
        })
    
    finished = pd.DataFrame(fin_list)
    
    unfin_list = []
    for _, row in graph_data['paths_unfinished'].iterrows():
        path = row['path']
        time = row['duration_in_seconds']
        click_positions = get_click_positions(pd.DataFrame({'path': [path]}))
        prob = get_probability_link(click_positions)
        semantic, pval = semantic_increase_score(path, row['target'])
        max_gen = article_gen_score.loc[path].max()
    
        if len(path) < 4 or semantic < 0 or len(path) > 100:
            continue #A path too short, too long, or that progressively gets further from target doesn't make sense and will be ignored
        unfin_list.append({
            'source': row['source'],
            'target': row['target'],
            'path': path,
            'time': time,
            'finished': False,
            'num_clicks': len(path),
            'top_link_usage': prob > threshold_link,
            'semantic' : semantic > threshold_semantic,
            'max_generality' : max_gen > score_threshold
        })
    
    unfinished = pd.DataFrame(unfin_list)

    return finished, unfinished

