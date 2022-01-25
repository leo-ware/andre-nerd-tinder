from flask import request
import requests
from src.cache import Cache


def _lookup(paperId):
    resp = requests.get(f"https://api.semanticscholar.org/graph/v1/paper/{paperId}?fields=title,abstract,authors")
    return resp.json()

paper_lookup = Cache(_lookup, maxsize=1e5)
