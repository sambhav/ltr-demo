import collections
import random
from flask import Flask, request, render_template, abort, Response
from flaskapp.constants import DEFAULT_RANKER
from flaskapp.query import (
    get_results,
    InvalidRankerException,
    get_results_for_ranker,
    get_annotated_queries,
    get_rankers,
)
import json

from flaskapp.dataset import Dataset

app = Flask(__name__)
dataset = Dataset()


@app.route("/", methods=["GET"])
def homepage():
    if "query" not in request.args:
        return render_template("rankers.html")
    else:
        query = request.args.get("query")
        try:
            results = get_results_for_ranker(query, "originalScoreModel")
            for doc in results:
                key = doc["wikiTitle"]
                doc["relevance"] = dataset.get_relevance(query, key)
        except InvalidRankerException:
            return abort(404)
        else:
            return render_template("rankers.html", query=query, results=results)


@app.route("/annotate", methods=["GET"])
def annotate():
    query = request.args.get("query")
    docid = request.args.get("docid")
    rel = int(request.args.get("rel"))
    dataset.annotate(query, docid, rel)
    return json.dumps(True)


@app.route("/stats", methods=["GET"])
def stats():
    metrics = ["P@10", "R@10", "F@10"]
    rankers = {
        "originalScore": [1.0, 1.0, 1.0],
        "originalScore1": [1.0, 1.0, 1.0],
        "originalScore2": [1.0, 1.0, 1.0],
        "originalScore3": [1.0, 1.0, 1.0],
    }
    ranker = request.args.get("ranker", DEFAULT_RANKER)
    results = collections.defaultdict(dict)
    for query in get_annotated_queries():
        results[query]["docs"] = get_results_for_ranker(query, ranker)
        results[query]["metrics"] = {"F@10": 1.0, "R@10": 1.0, "P@10": 1.0}
    return render_template(
        "stats.html", metrics=metrics, rankers=rankers, results=results
    )


@app.route("/ranker", methods=["GET"])
def ranker():
    rankers = get_rankers()
    selected_ranker = request.args.get("ranker", DEFAULT_RANKER)
    if selected_ranker not in rankers:
        return Response("Invalid Ranker"), 404
    results = collections.defaultdict(dict)
    for query in get_annotated_queries():
        results[query]["docs"] = get_results_for_ranker(query, selected_ranker)
        for doc in results[query]["docs"]:
            doc["relevant"] = random.choice([True, False])
        results[query]["metrics"] = {"F@10": "1.0", "R@10": "1.0", "P@10": "1.0"}
    return render_template(
        "ranker-performance.html",
        results=results,
        selected_ranker=selected_ranker,
        rankers=rankers,
    )
