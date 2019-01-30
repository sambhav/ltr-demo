from functools import partial
from collections import namedtuple

from flaskapp.query import get_results_for_ranker

class Metric:

    def __init__(self, name, value):
        self.name = name
        self._value = None
        self.value = value
    
    def __repr__(self):
        return f"{self.name}: {self.value}"

    def __add__(self, other):
        return Metric(self.name, self.value + other.value)

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = round(value, 2)

class MetricsCalculator:
    def __init__(self, dataset, query, results, k=-1):
        self.dataset = dataset
        self.query = query
        self.is_relevant = partial(dataset.is_relevant, query)
        if k > 0:
            results = results[:k]
        self.results = results
        self.k = k

    @property
    def relevant_doc_count(self):
        if not self.dataset or not self.results:
            return 0
        return sum(map(lambda doc: self.is_relevant(doc['wikiTitle']), self.results))

    @property
    def precision(self):
        name = f"PRECISION@{self.k}"
        if not self.results:
            value = 0
        else:
            value = self.relevant_doc_count / len(self.results)
        return Metric(name, value)

    @property
    def recall(self):
        name = f"RECALL@{self.k}"
        total_relevant_docs = self.dataset.get_relevant_docs(self.query)
        if not total_relevant_docs:
            value = 0
        else:
            value = self.relevant_doc_count / total_relevant_docs
        return Metric(name, value)

    @property
    def fscore(self):
        name = f"F-SCORE@{self.k}"
        sum_ = self.recall.value + self.precision.value
        if not sum_:
            value = 0
        else:
            value = (2 * self.recall.value * self.precision.value) / sum_
        return Metric(name, value)

    def get_all_metrics(self):
        return [self.fscore, self.precision, self.recall]


def evaluate_ranker(ranker, dataset, k):
    evaluation = {"average": [], "queries": {}}
    query_evaluations = evaluation["queries"]
    get_results = partial(get_results_for_ranker, ranker=ranker)
    avg_metrics = MetricsCalculator(dataset, "", [], k=k).get_all_metrics()
    queries = dataset.get_queries()
    num_queries = len(queries)
    for query in queries:
        results = get_results(query)
        metrics = MetricsCalculator(
            dataset, query, results, k=k
        ).get_all_metrics()
        query_evaluations[query] = metrics
        for i, metric in enumerate(metrics):
            avg_metrics[i] += metric
    evaluation['average'] = avg_metrics
    for metric in avg_metrics:
        metric.value /= num_queries
    return evaluation
