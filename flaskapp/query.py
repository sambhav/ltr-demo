import json
import logging
import pysolr
from flaskapp.constants import RANKERS_PATH, SOLR_URI

logger = logging.getLogger(__name__)
RQ_QUERY = "{{!ltr efi.query={} model={}}}"
FL_LIST = "features:[features],score,title,wikiTitle,id"


class InvalidRankerException(Exception):
    pass


def get_rankers():
    with open(RANKERS_PATH) as f:
        rankers_data = json.load(f)
        return list(rankers_data.keys())


def get_results(query):
    results = {}
    for ranker in get_rankers():
        results[ranker] = get_results_for_ranker(query, ranker)
    return results


def get_results_for_ranker(query, ranker):
    if ranker not in get_rankers():
        raise InvalidRankerException()
    solr = pysolr.Solr(SOLR_URI)
    params = {}
    params["rq"] = RQ_QUERY.format(query, ranker)
    params["fl"] = FL_LIST
    logger.info(query, RQ_QUERY, FL_LIST)
    results = solr.search(query, **params)
    return results
