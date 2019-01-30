import json
import time
import numpy as np
from flaskapp.training_data_generator import generate_training_data


class LinearModel:
    def __init__(self):
        self.weights = {}

    def train(self):
        training_data = generate_training_data()
        relevance = []
        features = []
        feature_names = []
        for docs in training_data.values():
            for doc in docs:
                relevance.append(doc[0])
                features.append(list(doc[1].values()))
                if not feature_names:
                    feature_names.extend(doc[1].keys())
        relevance = np.array(relevance)
        features = np.array(features)
        # Linear fitting of feature value to relevance and then extracting the weights
        weights = np.polyfit(relevance, features, 1)[0].tolist()
        for feature_name, weight in zip(feature_names, weights):
            self.weights[feature_name] = weight

    def to_json(self):
        model = {
            "class": "org.apache.solr.ltr.model.LinearModel",
            "name": f"linear-model-{int(time.time())}",
            "features": [{"name": feature} for feature in self.weights],
            "params": {"weights": self.weights},
        }
        return json.dumps(model)
