import json
import logging
import pysolr
from flaskapp.constants import RANKERS_PATH, SOLR_URI, ANNOTATIONS_PATH, DEFAULT_RANKER

logger = logging.getLogger(__name__)
RQ_QUERY = "{{!ltr efi.query={} model={}}}"
FL_LIST = "features:[features],score,title,wikiTitle,id,description"


class InvalidRankerException(Exception):
    def __init__(self, ranker_name):
        super().__init__(f"Invalid Ranker name:{ranker_name}")


def get_annotated_queries():
    with open(ANNOTATIONS_PATH) as f:
        annotations_data = json.load(f)
        return annotations_data.keys()


def get_rankers():
    with open(RANKERS_PATH) as f:
        rankers_data = json.load(f)
        return list(rankers_data.keys())


def get_results(query):
    return get_results_for_ranker(query, DEFAULT_RANKER)


def get_results_for_ranker(query, ranker):
    if ranker not in get_rankers():
        raise InvalidRankerException(ranker)
    solr = pysolr.Solr(SOLR_URI)
    params = {}
    params["rq"] = RQ_QUERY.format(query, ranker)
    params["fl"] = FL_LIST
    logger.info(query, RQ_QUERY, FL_LIST)
    results = solr.search(query, **params).docs
    return results
