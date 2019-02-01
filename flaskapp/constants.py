from pathlib import Path

DIR_PATH = Path(__file__).parent
DATA_DIR_PATH = DIR_PATH / "data"
ANNOTATIONS_PATH = DATA_DIR_PATH / "annotations.json"
SOLR_URI = "http://localhost:8983/solr/wikipedia"
SOLR_MODEL_STORE_URL = "http://localhost:8983/solr/wikipedia/schema/model-store/"
DEFAULT_RANKER = "originalScoreModel"
RANKLIB_JAR_PATH = DIR_PATH / "bin" / "ranklib.jar"
