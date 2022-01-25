from make_clusters import *
import numpy as np

def test_load_papers():
    query = "deep learning"
    max_results = 100
    papers = load_papers(query, max_results)
    assert len(papers) == max_results
    assert set(papers[0].keys()) == {"title", "paperId"}


def test_embed_title():
    title = "Deep learning"
    embedding = embed_title(title)
    assert isinstance(embedding, np.ndarray)
    assert embedding.shape == (96,)


def test_learn_model():
    titles = ["Deep learning", "Artificial intelligence", "Machine learning", "yo mama"]
    model = learn_model(titles)
    assert isinstance(model, KMeans)
    assert model.get_params()["n_clusters"] == 4


def test_make_clusters():
    query = "deep learning"
    max_results = 100
    n_clusters = 4
    clusters = make_clusters(query, max_results, n_clusters)
    assert len(clusters) == n_clusters
    assert sum(len(c) for c in clusters) == max_results
