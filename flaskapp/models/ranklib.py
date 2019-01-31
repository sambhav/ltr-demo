import time
import tempfile
import subprocess
import xml.etree.ElementTree as ET
import json
from flaskapp.training_data_generator import generate_training_data
from flaskapp.dataset import Dataset
from flaskapp.constants import RANKLIB_JAR_PATH


class LambdaMartModel:

    FEATURE_STORE = "_DEFAULT_"

    def __init__(self, num_trees, optimization_metric, k):
        self.name = (
            f"lambdamart-{optimization_metric}@{k}-{num_trees}-{int(time.time())}"
        )
        self.num_trees = str(num_trees)
        self.metric = f"{optimization_metric}@{k}"
        self.features = {}
        _, self.data_output_path = tempfile.mkstemp()
        _, self.model_output_path = tempfile.mkstemp()

    def train(self):
        data = generate_training_data()
        initial_data = []
        for qid in data:
            for doc in data[qid]:
                relevant, features = doc
                if not self.features:
                    self.features = {
                        index: name for index, name in enumerate(features.keys(), 1)
                    }
                feature_string = " ".join(
                    f"{index}:{value}"
                    for index, value in enumerate(features.values(), 1)
                )
                initial_data.append(f"{relevant} qid:{qid} {feature_string}")
        with open(self.data_output_path, "w") as f:
            f.write("\n".join(initial_data))
        self._run_ranklib()

    def _run_ranklib(self):
        subprocess.run(
            [
                "java",
                "-jar",
                RANKLIB_JAR_PATH,
                "-ranker",
                "6",
                "-tree",
                self.num_trees,
                "-train",
                self.data_output_path,
                "-metric2t",
                self.metric,
                "-save",
                self.model_output_path,
                "-silent"
            ]
        )

    def to_json(self):
        with open(self.model_output_path) as f:
            lines = f.readlines()
            lines = list(filter(lambda line: not line.startswith("#"), lines))
            lambda_model = ET.fromstringlist(lines)
        trees = []
        for node in lambda_model:
            t = {
                "weight": str(node.attrib["weight"]),
                "root": self._parse_splits(node[0]),
            }
            trees.append(t)
        model = {
            "class": "org.apache.solr.ltr.model.MultipleAdditiveTreesModel",
            "name": self.name,
            "features": [{"name": feature} for feature in self.features.values()],
            "params": {"trees": trees},
        }
        return json.dumps(model)

    def _parse_splits(self, node):
        obj = {}
        for el in node:
            if el.tag == "feature":
                obj["feature"] = self.features[(int(el.text.strip()))]
            elif el.tag == "threshold":
                obj["threshold"] = str(el.text.strip())
            elif el.tag == "split" and "pos" in el.attrib:
                obj[el.attrib["pos"]] = self._parse_splits(el)
            elif el.tag == "output":
                obj["value"] = str(el.text.strip())
        return obj
