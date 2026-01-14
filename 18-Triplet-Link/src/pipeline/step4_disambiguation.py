import pandas as pd
import json
import os
from tqdm import tqdm
from src.config import config
from src.services.llm import llm_service

class Step4Aligner:
    def _construct_prompt(self, sentence, subj_cands, obj_cands, rel_cands, triplet):
        subj_str = "\n".join([f"- {c['candidate_label']} ({c.get('description','')}) [ID: {c['candidate_qid']}]" for c in subj_cands])
        obj_str = "\n".join([f"- {c['candidate_label']} ({c.get('description','')}) [ID: {c['candidate_qid']}]" for c in obj_cands])
        rel_str = "\n".join([f"- {c['property_label']} [ID: {c['mapped_property']}]" for c in rel_cands])
        
        return f"""
        You are a Knowledge Graph Construction Agent.
        Your task is to identify the correct Wikidata entities and predicates for a given triplet extracted from text.

        Input Text: "{sentence}"
        Extracted Triplet: ({triplet['subject']}, {triplet['relation']}, {triplet['object']})

        Candidate Sets:
        1. Subject Candidates:
        {subj_str}
        2. Relation Candidates:
        {rel_str}
        3. Object Candidates:
        {obj_str}

        Instructions:
        1. Analyze the semantic context of the Input Text.
        2. Evaluate which candidate combination makes the most logical sense.
        3. Select the BEST combination. If no valid candidate exists for a role, return null for that role.

        Output Format (JSON):
        {{
          "rationale": "reasoning...",
          "decision": {{
            "subject": "Qxxxx" or null,
            "relation": "Pxxxx" or null,
            "object": "Qxxxx" or null
          }},
          "confidence": 0.0 to 1.0
        }}
        """

    def run(self):
        print("Step 4: Disambiguation and Alignment...")
        
        # Load data
        triplets_df = pd.read_csv(config.TRIPLES_RAW_PATH)
        candidates_df = pd.read_csv(config.ENTITIES_CANDIDATES_PATH)
        relations_df = pd.read_csv(config.RELATIONS_MAPPING_PATH)
        
        # Indexing for fast lookup
        candidates_grp = candidates_df.groupby(['triple_id', 'role'])
        relations_grp = relations_df.groupby('triple_id')
        
        # Load existing results (Resume capability)
        existing_results = []
        processed_ids = set()
        
        if os.path.exists(config.ALIGNMENT_RESULT_PATH):
            try:
                existing_df = pd.read_csv(config.ALIGNMENT_RESULT_PATH)
                existing_results = existing_df.to_dict('records')
                # We consider a record processed if it exists and status is NOT 'error'
                # AND note does not contain "Agent skipped" (legacy fallback)
                valid_mask = (existing_df['alignment_status'] != 'error') & \
                             (~existing_df['notes'].astype(str).str.contains("Agent skipped", na=False))
                processed_ids = set(existing_df[valid_mask]['triple_id'])
                print(f"Loaded {len(existing_results)} existing alignment results. {len(processed_ids)} are valid/completed.")
            except Exception as e:
                print(f"Error loading existing results: {e}")

        # Map existing results by triple_id for easy update (in case we retry errors)
        # Actually, simpler to just rebuild the list: keep valid ones, re-process others
        final_results_map = {r['triple_id']: r for r in existing_results if r['triple_id'] in processed_ids}
        
        newly_processed = 0
        errors = 0
        
        for _, row in tqdm(triplets_df.iterrows(), total=len(triplets_df), desc="Aligning"):
            triple_id = row['triple_id']
            
            if triple_id in processed_ids:
                continue
            
            # Get candidates
            subj_cands = candidates_grp.get_group((triple_id, 'subject')).to_dict('records') if (triple_id, 'subject') in candidates_grp.groups else []
            obj_cands = candidates_grp.get_group((triple_id, 'object')).to_dict('records') if (triple_id, 'object') in candidates_grp.groups else []
            rel_cands = relations_grp.get_group(triple_id).to_dict('records') if triple_id in relations_grp.groups else []
            
            # Tier 1: Fast Pass
            decision = {}
            status = "pending"
            note = ""
            validator = "auto"
            
            # Helper to pick best
            def pick_best(cands, key_id):
                if not cands: return None
                sorted_cands = sorted(cands, key=lambda x: x.get('score', 0) if 'score' in x else x.get('confidence', 0), reverse=True)
                best = sorted_cands[0]
                score = best.get('score', 0) if 'score' in best else best.get('confidence', 0)
                return best[key_id] if score > config.ENTITY_SCORE_THRESHOLD else None

            subj_qid = pick_best(subj_cands, 'candidate_qid')
            obj_qid = pick_best(obj_cands, 'candidate_qid')
            rel_pid = pick_best(rel_cands, 'mapped_property')
            
            if subj_qid and obj_qid and rel_pid:
                status = "accepted"
                note = "Fast pass accepted"
                decision = {"subject": subj_qid, "object": obj_qid, "relation": rel_pid}
            else:
                # Tier 2: Agent
                try:
                    # Construct Prompt
                    prompt = self._construct_prompt(row['source_sentence'], subj_cands, obj_cands, rel_cands, row)
                    
                    # Call LLM
                    response = llm_service.chat_completion(
                        messages=[{"role": "user", "content": prompt}],
                        response_format={"type": "json_object"}
                    )
                    
                    # Parse
                    content = response.replace("```json", "").replace("```", "").strip()
                    parsed = json.loads(content)
                    
                    decision_data = parsed.get("decision", {})
                    decision = {
                        "subject": decision_data.get("subject"),
                        "object": decision_data.get("object"),
                        "relation": decision_data.get("relation")
                    }
                    
                    conf = parsed.get("confidence", 0.5)
                    note = parsed.get("rationale", "")
                    
                    if conf > config.FINAL_CONFIDENCE_THRESHOLD:
                        status = "accepted"
                    elif conf > 0.3:
                        status = "low_confidence"
                    else:
                        status = "rejected"
                        
                    validator = "agent"
                    
                except Exception as e:
                    # Error handling: Record as error, do not fallback
                    status = "error"
                    note = f"Agent failed: {str(e)}"
                    errors += 1
                    decision = {"subject": None, "object": None, "relation": None}

            # Clean newlines from note to ensure CSV integrity (one line per record)
            if note:
                note = note.replace('\n', ' ').replace('\r', ' ')

            # Update/Add result
            final_results_map[triple_id] = {
                'triple_id': triple_id,
                'subject_qid': decision.get('subject'),
                'relation_pid': decision.get('relation'),
                'object_qid': decision.get('object'),
                'alignment_status': status,
                'validator': validator,
                'validated_at': pd.Timestamp.now().isoformat(),
                'notes': note
            }
            newly_processed += 1
            
        # Convert map back to list and save
        # Sort by triple_id for consistency
        final_results = sorted(list(final_results_map.values()), key=lambda x: x['triple_id'])
        
        pd.DataFrame(final_results).to_csv(config.ALIGNMENT_RESULT_PATH, index=False)
        print(f"Step 4 completed. Processed {newly_processed} items ({errors} errors). Total results: {len(final_results)}")

if __name__ == "__main__":
    Step4Aligner().run()
