import pandas as pd
from tqdm import tqdm
from difflib import SequenceMatcher
from src.config import config
from src.services.wikidata import wikidata_service

class Step2CandidateGenerator:
    def _calculate_similarity(self, s1, s2):
        return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()

    def run(self):
        print("Step 2: Generating entity candidates...")
        
        # Load raw triplets
        triplets_df = pd.read_csv(config.TRIPLES_RAW_PATH)
        
        # Get unique mentions to minimize API calls
        # Collect (mention, type) pairs if we had types, but we only have raw mentions now.
        # We process subjects and objects.
        mentions = set(triplets_df['subject'].unique()) | set(triplets_df['object'].unique())
        print(f"Found {len(mentions)} unique entity mentions.")
        
        # Search candidates for each mention
        mention_candidates = {}
        
        # Limit for testing/demo purposes if needed, but here we process all
        # For large datasets, might want to process in chunks
        for mention in tqdm(mentions, desc="Searching Wikidata"):
            try:
                results = wikidata_service.search_entity(mention)
                processed_results = []
                for idx, res in enumerate(results):
                    # Calculate score: combination of rank and string similarity
                    rank_score = 1.0 / (idx + 1)  # 1.0, 0.5, 0.33...
                    str_score = self._calculate_similarity(mention, res['label'])
                    
                    # Weighted score
                    final_score = 0.4 * rank_score + 0.6 * str_score
                    
                    processed_results.append({
                        'candidate_qid': res['id'],
                        'candidate_label': res['label'],
                        'description': res['description'],
                        'score': round(final_score, 3)
                    })
                mention_candidates[mention] = processed_results
            except Exception as e:
                print(f"Failed to search for {mention}: {e}")
                mention_candidates[mention] = []
        
        wikidata_service.save()
        
        # Generate output rows
        output_rows = []
        
        for _, row in tqdm(triplets_df.iterrows(), total=len(triplets_df), desc="Generating output"):
            triple_id = row['triple_id']
            
            # Subject
            subj_mention = row['subject']
            for cand in mention_candidates.get(subj_mention, []):
                output_rows.append({
                    'triple_id': triple_id,
                    'role': 'subject',
                    'mention': subj_mention,
                    'normalized_label': subj_mention, # Placeholder
                    'entity_type': '', # Placeholder, would need detailed query
                    'candidate_qid': cand['candidate_qid'],
                    'candidate_label': cand['candidate_label'],
                    'score': cand['score']
                })
            
            # Object
            obj_mention = row['object']
            for cand in mention_candidates.get(obj_mention, []):
                output_rows.append({
                    'triple_id': triple_id,
                    'role': 'object',
                    'mention': obj_mention,
                    'normalized_label': obj_mention, # Placeholder
                    'entity_type': '', # Placeholder
                    'candidate_qid': cand['candidate_qid'],
                    'candidate_label': cand['candidate_label'],
                    'score': cand['score']
                })
                
        # Create DataFrame
        output_df = pd.DataFrame(output_rows)
        
        # Save
        output_df.to_csv(config.ENTITIES_CANDIDATES_PATH, index=False)
        print(f"Step 2 completed. Saved {len(output_df)} candidates to {config.ENTITIES_CANDIDATES_PATH}")

if __name__ == "__main__":
    Step2CandidateGenerator().run()
