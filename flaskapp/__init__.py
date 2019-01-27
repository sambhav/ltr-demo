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
    return render_template("compare.html")
