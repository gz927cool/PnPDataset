import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    OUTPUT_DIR = DATA_DIR / "output"
    
    # Input files
    SOURCE_DATA_PATH = DATA_DIR / "merged_index_enrich.csv"
    TRIPLETS_PATH = DATA_DIR / "extracted_triplets_adj.csv"
    
    # Output files
    TRIPLES_RAW_PATH = OUTPUT_DIR / "triples_raw.csv"
    ENTITIES_CANDIDATES_PATH = OUTPUT_DIR / "entities_candidates.csv"
    RELATIONS_MAPPING_PATH = OUTPUT_DIR / "relations_mapping.csv"
    ALIGNMENT_RESULT_PATH = OUTPUT_DIR / "alignment_result.csv"
    FACTS_SEMANTIC_PATH = OUTPUT_DIR / "facts_semantic.tsv"
    NODES_PATH = OUTPUT_DIR / "nodes.csv"
    RELATIONS_PATH = OUTPUT_DIR / "relations.csv"
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
    OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")
    
    # Settings
    WIKIDATA_API_URL = "https://www.wikidata.org/w/api.php"
    USER_AGENT = "KnowledgeGraphBuilder/1.0 (mailto:your_email@example.com)"
    
    # Thresholds
    ENTITY_SCORE_THRESHOLD = 0.7
    RELATION_CONFIDENCE_THRESHOLD = 0.8
    FINAL_CONFIDENCE_THRESHOLD = 0.6
    
    def __init__(self):
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

config = Config()
