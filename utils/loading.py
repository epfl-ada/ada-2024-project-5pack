from functools import cache
from lxml.html import parse
from urllib.parse import unquote

import os
import numpy as np
import pandas as pd

PATHS_AND_GRAPH_FOLDER = "data/wikispeedia_paths-and-graph"
WP_SOURCE_DATA_FOLDER = "data/wpcd/wp"

def extract_links(page_path):
    doc = parse(page_path).getroot()
    
    return [
        (a.text_content(), href.split("/")[-1].split(".htm")[0], unquote(href.split("/")[-1].split(".htm")[0])) 
        for a in doc.cssselect('a') 
        if (href := a.get('href'))
    ]

def extract_articles_data():
    articles_data = {}
    for root, _, files in os.walk(WP_SOURCE_DATA_FOLDER):
        for file in files:
            if file.endswith(".htm"):
                article_name = file.split(".")[0]
                article_links = extract_links(os.path.join(root, file))
                
                articles_data[article_name] = {
                    "links": article_links
                }
    
    articles_data = pd.DataFrame.from_dict(articles_data, orient="index")

    return articles_data

def load_data_from_file(file_path):
    columns = None
    data = []
    with open(file_path) as file:
        while line := file.readline():
            line = line.rstrip()
            if line.startswith("# FORMAT:") and not columns:
                data_str = line.split("# FORMAT:   ")[1] if line.startswith("# FORMAT:   ") else "value"
                columns = data_str.split("   ")
            elif line.startswith("# FORMAT:"):
                raise RuntimeError()
            elif len(line) > 0 and not line.startswith("#"):
                data_line = line.split("	")
                assert len(data_line) == len(columns)
                data.append(data_line)
    
    df = pd.DataFrame(data, columns=columns)
    
    return df

@cache
def load_paths_and_graph():
    if not os.path.isdir(PATHS_AND_GRAPH_FOLDER):
        raise ValueError("The data is not setup correctly, please follow the instructions in `data/README.md`.")
    
    paths_and_graph = {}

    print("loading raw data from tsv files...")
    with os.scandir(PATHS_AND_GRAPH_FOLDER) as it:
        for entry in it:
            if (entry.name.endswith(".tsv") or entry.name.endswith(".txt")) and entry.is_file():
                key = entry.name.split(".")[0]
                paths_and_graph[key] = load_data_from_file(entry.path)

    print("formatting data...")
    paths_and_graph["articles"]["article_decoded"] = paths_and_graph["articles"]["article"].apply(unquote)

    paths_and_graph["categories"]["article_decoded"] = paths_and_graph["categories"]["article"].apply(unquote)

    paths_and_graph["links"]["linkSource_decoded"] = paths_and_graph["links"]["linkSource"].apply(unquote)
    paths_and_graph["links"]["linkTarget_decoded"] = paths_and_graph["links"]["linkTarget"].apply(unquote)
    
    paths_and_graph["shortest-path-distance-matrix"] = np.array(list(map(
            lambda s: np.array(list(map(lambda e: np.NaN if e == "_" else int(e), list(s)))),
            paths_and_graph["shortest-path-distance-matrix"].value.values
        ))
    )
    
    print("extracting additional information from source code...")
    articles_data = extract_articles_data()
    paths_and_graph["articles"] = paths_and_graph["articles"].merge(articles_data, left_on="article", right_index=True)
    paths_and_graph["articles"]["num_links"] = paths_and_graph["articles"]["links"].apply(lambda l: len(l))

    return paths_and_graph