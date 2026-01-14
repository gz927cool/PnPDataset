import pandas as pd
import numpy as np
from src.config import config

class Step5FactGenerator:
    def run(self):
        print("Step 5: Generating Semantic Facts...")
        
        # Load inputs
        alignment_df = pd.read_csv(config.ALIGNMENT_RESULT_PATH)
        triplets_df = pd.read_csv(config.TRIPLES_RAW_PATH)
        candidates_df = pd.read_csv(config.ENTITIES_CANDIDATES_PATH)
        relations_df = pd.read_csv(config.RELATIONS_MAPPING_PATH)
        
        # Merge data to get confidence scores
        # 1. Join alignment with triplets for raw confidence
        facts = alignment_df.merge(triplets_df[['triple_id', 'confidence']], on='triple_id', how='left', suffixes=('', '_raw'))
        
        # 2. Get Subject Score
        # We need to lookup score from candidates_df based on triple_id, role=subject, candidate_qid=subject_qid
        # Optimize: create lookup dict
        cand_lookup = candidates_df.set_index(['triple_id', 'role', 'candidate_qid'])['score'].to_dict()
        
        # 3. Get Object Score
        # Same lookup
        
        # 4. Get Relation Score
        rel_lookup = relations_df.set_index(['triple_id', 'mapped_property'])['confidence'].to_dict()
        
        fact_rows = []
        for idx, row in facts.iterrows():
            if pd.isna(row['subject_qid']) or pd.isna(row['object_qid']) or pd.isna(row['relation_pid']):
                continue
                
            raw_conf = row['confidence']
            
            subj_score = cand_lookup.get((row['triple_id'], 'subject', row['subject_qid']), 0.5)
            obj_score = cand_lookup.get((row['triple_id'], 'object', row['object_qid']), 0.5)
            rel_score = rel_lookup.get((row['triple_id'], row['relation_pid']), 0.5)
            
            # Geometric mean
            final_conf = np.power(raw_conf * subj_score * obj_score * rel_score, 1/4)
            
            fact_rows.append({
                'fact_id': f"F{idx:05d}",
                'subject_uri': f"wd:{row['subject_qid']}",
                'predicate_uri': f"wdt:{row['relation_pid']}",
                'object_uri': f"wd:{row['object_qid']}",
                'source_triple': row['triple_id'],
                'confidence': round(final_conf, 3)
            })
            
        facts_df = pd.DataFrame(fact_rows)
        facts_df.to_csv(config.FACTS_SEMANTIC_PATH, sep='\t', index=False)
        print(f"Step 5 completed. Generated {len(facts_df)} facts.")

if __name__ == "__main__":
    Step5FactGenerator().run()
