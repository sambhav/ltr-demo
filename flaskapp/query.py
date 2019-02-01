import json
import logging
import pysolr
import requests
from flaskapp.constants import (
    SOLR_MODEL_STORE_URL,
    SOLR_URI,
    ANNOTATIONS_PATH,
    DEFAULT_RANKER,
)

logger = logging.getLogger(__name__)
RQ_QUERY = "{{!ltr efi.query={} model={} reRankDocs=25}}"
FL_LIST = "features:[features],score,title,wikiTitle,id,description"


class InvalidRankerException(Exception):
    def __init__(self, ranker_name):
        super().__init__(f"Invalid Ranker name:{ranker_name}")


def get_annotated_queries():
    with open(ANNOTATIONS_PATH) as f:
        annotations_data = json.load(f)
        return annotations_data.keys()


def get_rankers(default=True):
    response = requests.get(SOLR_MODEL_STORE_URL)
    models = [model["name"] for model in response.json()["models"]]
    if not default and DEFAULT_RANKER in models:
        models.remove(DEFAULT_RANKER)
    return models


def get_results(query):
    return get_results_for_ranker(query, DEFAULT_RANKER)


def get_results_for_ranker(query, ranker):
    if ranker not in get_rankers():
        raise InvalidRankerException(ranker)
    solr = pysolr.Solr(SOLR_URI)
    params = {}
    params["rq"] = RQ_QUERY.format(query, ranker)
    params["fl"] = FL_LIST
    params["rows"] = 50
    logger.info(query, RQ_QUERY, FL_LIST)
    results = solr.search(query, **params).docs
    return results
