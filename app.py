from flask import Flask, request
from src.make_clusters import make_clusters
from src.paper_lookup import paper_lookup

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/get_clusters')
def get_clusters():
    try:
        query = request.args["query"]
    except KeyError:
        return "Error: No query specified. Please specify a query using the 'query' parameter."

    return {"clusters": make_clusters(query, max_results=10)}

@app.route('/get_paper')
def get_paper():
    try:
        paper_id = request.args["paperId"]
    except KeyError:
        return "Error: No paper_id specified. Please specify a paper_id using the 'paperId' parameter."
    return {"paper": paper_lookup(paper_id)}

if __name__ == '__main__':
    app.run(debug=True, port=8000)
