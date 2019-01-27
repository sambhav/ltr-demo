from flask import request, render_template, abort
from flaskapp import app
from flaskapp.query import get_results, InvalidRankerException


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
