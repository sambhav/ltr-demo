import requests
from flaskapp.constants import SOLR_MODEL_STORE_URL


def upload_model(name, model_json):
    response = requests.post(
        SOLR_MODEL_STORE_URL,
        data=model_json,
        headers={"content-type": "application/json"},
    )
    if response.status_code != 200:
        raise Exception(
            f"Unable to upload model to Solr. Status code: {response.status_code}"
        )
