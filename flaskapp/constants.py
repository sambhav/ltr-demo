from pathlib import Path

DIR_PATH = Path(__file__).parent
DATA_DIR_PATH = DIR_PATH / "data"
RANKERS_PATH = DATA_DIR_PATH / "rankers.json"
ANNOTATIONS_PATH = DATA_DIR_PATH / "annotations.json"
SOLR_URI = "http://localhost:8983/solr/wikipedia"
DEFAULT_RANKER = "originalScoreModel"
