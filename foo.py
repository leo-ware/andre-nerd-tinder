import sklearn
import requests
import spacy
import numpy as np
from collections import defaultdict
from sklearn.cluster import KMeans
import random


QUERY = "navier stokes simulation"


def load_abstracts(query, max_results=100):
    url = 'https://api.semanticscholar.org/graph/v1/paper/search'
    params = {'query': query, 'limit': max_results}

    r = requests.get(url, params=params)
    return r

resps = load_abstracts(QUERY, 100)

titles = [resp['title'] for resp in resps.json()['data']]

nlp = spacy.load("en_core_web_sm")
embeddings = np.vstack([nlp(t).vector for t in titles])

# clustering
cluster = KMeans(4)
categories = cluster.fit_predict(embeddings)

# build index
index = defaultdict(set)
for category, item in zip(categories, titles):
    index[category].add(item)

class Swiper:
    def __init__(self, index):
        self.index = index

        self.current_category = random.choice(list(self.index))
        self.current_paper  = None

        self.visited = []

        # ones that you've swiped left on
        self.bad_categories = set()

        self.switch_paper()

    def switch_paper(self):
        # add current paper to visited
        if self.current_paper:
                self.visited.append(self.current_paper)
        
        # select new paper from current category
        candidate_papers = list(self.index[self.current_category] - set(self.visited))
        if candidate_papers:
            new_paper = random.choice(candidate_papers)
            self.visited.append(new_paper)
            self.current_paper = new_paper
        else:
            self.switch_category()
            self.switch_paper()

    def switch_category(self):
        # select new category, excluding bad categories
        candidate_categories = {*index} - self.bad_categories

        if candidate_categories:
            self.current_category = random.choice(list(candidate_categories))
        else:
            # no more categories to visit
            raise StopIteration("exhausted all categories")
        
    def swipe_left(self):
        # add current category to bad categories
        self.bad_categories.add(self.current_category)
        self.switch_category()
        self.switch_paper()
    
    def swipe_right(self):
        self.switch_paper()

    def tinder(self):
        while True:
            print("\nSuggestion:", self.current_paper)

            ans = None
            while ans not in {"y", "n", "exit"}:
                ans = input("Is this a good pick? (y/n/exit)")
            
            try:
                if ans == "y":
                    self.swipe_right()
                elif ans == "n":
                    self.swipe_left()
                else:
                    break
            except StopIteration:
                break
        
        print("\nThanks for using Swiper!")
        
foo = Swiper(index)
foo.tinder()
print(foo.visited)
