from flaskapp.dataset import Dataset
from flaskapp.query import get_results


def generate_training_data():
    dataset = Dataset()
    data = {}
    for qid, query in enumerate(dataset.get_queries()):
        results = get_results(query)
        docs = []
        for doc in results:
            relevant = int(dataset.is_relevant(query, doc["wikiTitle"]))
            features = {}
            for fvpair in doc["features"].split(","):
                name, value = fvpair.split("=")
                features[name] = float(value)
            docs.append((relevant, features))
        data[qid] = docs
    return data
