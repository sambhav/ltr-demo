from pathlib import Path

DIR_PATH = Path(__file__).parent
DATA_DIR_PATH = DIR_PATH / "data"
RANKERS_PATH = DATA_DIR_PATH / "rankers.json"
SOLR_URI = "http://solr:8983/solr/wikipedia"
