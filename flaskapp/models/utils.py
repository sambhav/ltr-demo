from urllib.parse import urljoin
import requests
from flaskapp.constants import SOLR_MODEL_STORE_URL, DEFAULT_RANKER
from flaskapp.query import get_rankers


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


def delete_model(name):
    if name == DEFAULT_RANKER:
        raise Exception("Unable to delete default model")
    response = requests.delete(urljoin(SOLR_MODEL_STORE_URL, name))
    if response.status_code != 200:
        raise Exception(f"Unable to delete model. Status code: {response.status_code}")


def delete_all_models():
    for model in get_rankers():
        if model == DEFAULT_RANKER:
            continue
        delete_model(model)
