import json
import requests
from flaskapp.constants import MODEL_UPLOAD_URL, RANKERS_PATH


def upload_model(name, model_json):
    response = requests.post(
        MODEL_UPLOAD_URL, data=model_json, headers={"content-type": "application/json"}
    )
    if response.status_code != 200:
        raise Exception(
            f"Unable to upload model to Solr. Status code: {response.status_code}"
        )
    models = []
    with open(RANKERS_PATH) as f:
        models = json.load(f)
        models.append(name)
    with open(RANKERS_PATH, "w") as f:
        json.dump(models, f, indent=2)
