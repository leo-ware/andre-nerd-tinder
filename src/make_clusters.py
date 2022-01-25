import requests
import numpy as np
import spacy
from sklearn.cluster import KMeans

from src.paper_lookup import paper_lookup

nlp = spacy.load("en_core_web_sm")

def embed_title(title):
    return nlp(title).vector

def load_papers(query, max_results=100):
    url = 'https://api.semanticscholar.org/graph/v1/paper/search'
    params = {'query': query, 'limit': max_results, 'fields': 'paperId,title,abstract,authors'}
    r = requests.get(url, params=params)

    if r.status_code == 200:
        data = r.json()["data"]
        cache_vals = {p['paperId']: p for p in data}
        paper_lookup.save(cache_vals)
        return data
    else:
        raise Exception('Error: {}'.format(r.status_code))

def learn_model(titles, n_clusters=4):
    embeddings = np.vstack([embed_title(t) for t in titles])
    model = KMeans(n_clusters)
    model.fit(embeddings)
    return model

def make_clusters(query, max_results=100, n_clusters=4):
    papers = load_papers(query, max_results)
    titles = [p["title"] for p in papers]
    model = learn_model(titles, n_clusters)
    clusters = [[] for _ in range(n_clusters)]

    for paper in papers:
        embedding = embed_title(paper["title"])
        cluster = model.predict(embedding.reshape(1, -1))[0]
        clusters[cluster].append(paper["paperId"])

    return clusters
