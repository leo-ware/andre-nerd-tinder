from flask import Flask, request
from make_clusters import make_clusters

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

    return {"clusters": make_clusters(query)}

if __name__ == '__main__':
    app.run(debug=True, port=8000)
