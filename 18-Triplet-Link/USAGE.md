# Usage Guide

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   (Note: Dependencies are listed in `pyproject.toml`)

2. Configure Environment:
   Ensure `.env` file exists with `OPENAI_API_KEY`.

## Running the Pipeline

You can run the entire pipeline using the runner script:

```bash
python main.py
```

Or run specific steps:

```bash
# Run only Step 0 (Preprocessing)
python src/pipeline/runner.py --steps 0

# Run Steps 2 and 3
python src/pipeline/runner.py --steps 2 3
```

## Pipeline Steps

1. **Step 0**: Preprocess `extracted_triplets_adj.csv` to `triples_raw.csv`.
2. **Step 2**: Generate entity candidates from Wikidata (`entities_candidates.csv`).
3. **Step 3**: Map relations to Wikidata properties (`relations_mapping.csv`).
4. **Step 4**: Disambiguate and align entities/relations (`alignment_result.csv`).
5. **Step 5**: Generate semantic facts with confidence scores (`facts_semantic.tsv`).
6. **Step 6**: Generate Neo4j import files (`nodes.csv`, `relations.csv`).

## Output

All output files are located in `data/output/`.

## Configuration

Settings are in `src/config.py`.
