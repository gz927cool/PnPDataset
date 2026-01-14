# Knowledge Graph Construction Pipeline Implementation Plan

## 1. Project Initialization

* [x] Analyze requirements and existing files.

* [ ] Create directory structure (`src/`, `tests/`, `data/output/`).

* [ ] Configure `pyproject.toml` with dependencies (`pandas`, `requests`, `openai`, `pydantic`, `tenacity`, `python-dotenv`).

## 2. Pipeline Implementation

### Step 0: Data Preprocessing

* [ ] Implement `Step0Preprocessor` to process `extracted_triplets_adj.csv`.

* [ ] Generate `data/output/triples_raw.csv` with required fields.

### Step 2: Entity Standardization & Candidates

* [ ] Implement `WikidataService` to search entities via Wikidata API.

* [ ] Implement `Step2CandidateGenerator` to generate `entities_candidates.csv`.

* [ ] Implement caching to avoid redundant API calls.

### Step 3: Relation Semantic Mapping

* [ ] Implement `Step3RelationMapper` with rule-based and LLM-based mapping.

* [ ] Generate `relations_mapping.csv`.

### Step 4: Agentic Disambiguation

* [ ] Implement `DisambiguationAgent` using OpenAI API and Langchain.

* [ ] Implement `Step4Aligner` to process candidates and generate `alignment_result.csv`.

### Step 5: Semantic Fact Generation

* [ ] Implement `Step5FactGenerator` to produce `facts_semantic.tsv`.

### Step 6: Graph Ingestion Preparation

* [ ] Implement `Step6GraphBuilder` to generate `nodes.csv` and `relations.csv` for Neo4j.

## 3. Orchestration & Testing

* [ ] Create `main.py` or `run_pipeline.py` to execute steps sequentially.

* [ ] Add unit tests for key components (API wrappers, data transformation).

* [ ] Verify output against requirements.

