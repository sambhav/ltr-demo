from flask import Flask, request, render_template, abort
from flaskapp.query import get_results, InvalidRankerException

app = Flask(__name__)


@app.route("/", methods=["GET"])
def homepage():
    if "query" not in request.args:
        return render_template("rankers.html")
    else:
        query = request.args.get("query")
        try:
            results = get_results(query)
        except InvalidRankerException:
            return abort(404)
        else:
            return render_template("rankers.html", query=query, results=results)


@app.route("/compare", methods=["GET"])
def compare():
    metrics = ["P@10", "R@10", "F@10"]
    rankers = {
        "originalScore": [1.0, 1.0, 1.0],
        "originalScore1": [1.0, 1.0, 1.0],
        "originalScore2": [1.0, 1.0, 1.0],
        "originalScore3": [1.0, 1.0, 1.0],
    }
    return render_template("compare.html", metrics=metrics, rankers=rankers)
