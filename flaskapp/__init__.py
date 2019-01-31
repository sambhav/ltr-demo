import collections
import random
from flask import (
    Flask,
    request,
    render_template,
    abort,
    Response,
    jsonify,
    url_for,
    redirect,
)
from flaskapp.constants import DEFAULT_RANKER
from flaskapp.query import InvalidRankerException, get_results_for_ranker, get_rankers
from flaskapp.dataset import Dataset
from flaskapp.metrics import evaluate_ranker

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
    return jsonify(True)


@app.route("/stats", methods=["GET"])
def stats():
    rankers = get_rankers()
    metric_names = []
    metrics = {}
    for ranker in rankers:
        metrics[ranker] = evaluate_ranker(ranker, dataset, 10)
        if not metric_names:
            for metric in metrics[ranker]["average"]:
                metric_names.append(metric.name)
    return render_template("stats.html", metric_names=metric_names, metrics=metrics)


@app.route("/ranker", methods=["GET"])
def ranker_home():
    return redirect(url_for("ranker", selected_ranker=DEFAULT_RANKER))


@app.route("/ranker/<selected_ranker>", methods=["GET"])
def ranker(selected_ranker):
    rankers = get_rankers()
    if selected_ranker not in rankers:
        return Response("Invalid Ranker"), 404
    results = collections.defaultdict(dict)
    metrics = evaluate_ranker(selected_ranker, dataset, 10)
    for query in dataset.get_queries():
        results[query]["docs"] = get_results_for_ranker(query, selected_ranker)
        for doc in results[query]["docs"]:
            doc["relevant"] = dataset.get_relevance(query, doc["wikiTitle"])
        results[query]["metrics"] = metrics["queries"][query]
    return render_template(
        "ranker-performance.html",
        results=results,
        selected_ranker=selected_ranker,
        rankers=rankers,
    )
