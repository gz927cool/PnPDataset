import pandas as pd
from tqdm import tqdm
from src.config import config
from src.services.llm import llm_service
import json
import os

class Step3RelationMapper:
    # Predefined mapping (partial)
    RELATION_MAPPING = {
        "is_located_in": {"id": "P131", "label": "located in the administrative territorial entity", "confidence": 0.95},
        "founded_by": {"id": "P112", "label": "founded by", "confidence": 0.98},
        "has_member": {"id": "P527", "label": "has part", "confidence": 0.9},
        "has_role_of": {"id": "P39", "label": "position held", "confidence": 0.85},
        "has_identity": {"id": "P106", "label": "occupation", "confidence": 0.8}, # Example
    }

    def _get_mapping_from_llm(self, relation, context_samples):
        prompt = f"""
        You are a Knowledge Graph Expert. Map the following relation from a text extraction to the most likely Wikidata property.
        
        Relation: "{relation}"
        Context samples:
        {context_samples}
        
        Provide the output in JSON format:
        {{
            "property_id": "Pxxx",
            "label": "property label",
            "confidence": 0.0 to 1.0,
            "reasoning": "explanation"
        }}
        """
        try:
            response = llm_service.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            # Clean markdown code blocks if present
            content = response.replace("```json", "").replace("```", "").strip()
            return json.loads(content)
        except Exception as e:
            print(f"LLM mapping failed for {relation}: {e}")
            raise # Re-raise to handle in the loop

    def run(self):
        print("Step 3: Mapping relations...")
        
        triplets_df = pd.read_csv(config.TRIPLES_RAW_PATH)
        unique_relations = triplets_df['relation'].unique()
        print(f"Found {len(unique_relations)} unique relations.")
        
        # Load existing mappings if available (Resume capability)
        # Fix: We should load UNIQUE mappings per raw_relation, not per triplet
        existing_mappings = {}
        if os.path.exists(config.RELATIONS_MAPPING_PATH):
            try:
                existing_df = pd.read_csv(config.RELATIONS_MAPPING_PATH)
                # Group by raw_relation to handle potential 1-to-many mappings
                # And de-duplicate: we only need to know "is_located_in -> P131" once, not for every triplet
                unique_existing = existing_df.drop_duplicates(subset=['raw_relation', 'mapped_property'])
                for rel, group in unique_existing.groupby('raw_relation'):
                    existing_mappings[rel] = group.to_dict('records')
                print(f"Loaded {len(existing_mappings)} unique relation mappings types.")
            except Exception as e:
                print(f"Error loading existing mappings: {e}")
        
        relation_map_result = existing_mappings.copy()
        newly_processed_count = 0
        failed_count = 0
        
        for relation in tqdm(unique_relations, desc="Mapping relations"):
            # Skip if already mapped
            if relation in relation_map_result:
                continue
                
            if relation in self.RELATION_MAPPING:
                mapping = self.RELATION_MAPPING[relation]
                relation_map_result[relation] = [{
                    "raw_relation": relation, # Ensure field consistency
                    "mapped_property": mapping["id"],
                    "property_label": mapping["label"],
                    "property_uri": "wdt:" + mapping["id"],
                    "confidence": mapping["confidence"]
                }]
                newly_processed_count += 1
            else:
                # Get a few samples for context
                samples = triplets_df[triplets_df['relation'] == relation].head(3)
                context_str = ""
                for _, row in samples.iterrows():
                    context_str += f"- {row['subject']} -> {row['object']} (Context: {row['source_sentence'][:50]}...)\n"
                
                try:
                    llm_res = self._get_mapping_from_llm(relation, context_str)
                    if llm_res:
                         relation_map_result[relation] = [{
                            "raw_relation": relation,
                            "mapped_property": llm_res.get("property_id"),
                            "property_label": llm_res.get("label"),
                            "property_uri": "wdt:" + llm_res.get("property_id", ""),
                            "confidence": llm_res.get("confidence", 0.5)
                        }]
                         newly_processed_count += 1
                except Exception as e:
                    print(f"Skipping relation '{relation}' due to error. Will retry next time.")
                    failed_count += 1
                    # Do NOT add empty list or fallback, so it remains unmapped

        # Generate output (Full rewrite to ensure consistency)
        output_rows = []
        
        # We need to output rows for ALL triplets, but based on the mappings we have.
        # However, the relations_mapping.csv format (as per design) lists mappings per triple_id?
        # Wait, the design doc says:
        # "triple_id, raw_relation, mapped_property..."
        # So we need to expand the mappings to all triples.
        
        # Let's re-read the doc or previous implementation.
        # Previous implementation:
        # for _, row in triplets_df.iterrows(): ... output_rows.append(...)
        
        # So we iterate all triplets, and if we have a mapping for the relation, we write it.
        # If we don't have a mapping (because it failed), we don't write it (or write partially?)
        # The downstream steps depend on this file.
        # If we skip rows here, Step 4 might miss them.
        # But if we don't have a mapping, we can't do much.
        # Let's skip rows for failed relations.
        
        for _, row in tqdm(triplets_df.iterrows(), total=len(triplets_df), desc="Generating output"):
            triple_id = row['triple_id']
            rel = row['relation']
            
            mappings = relation_map_result.get(rel, [])
            for m in mappings:
                # Ensure we have all fields
                output_rows.append({
                    'triple_id': triple_id,
                    'raw_relation': rel,
                    'mapped_property': m.get('mapped_property'),
                    'property_label': m.get('property_label'),
                    'property_uri': m.get('property_uri'),
                    'confidence': m.get('confidence')
                })
                
        output_df = pd.DataFrame(output_rows)
        output_df.to_csv(config.RELATIONS_MAPPING_PATH, index=False)
        print(f"Step 3 completed. Processed {newly_processed_count} new, {failed_count} failed. Total mappings: {len(output_df)} rows saved to {config.RELATIONS_MAPPING_PATH}")

if __name__ == "__main__":
    Step3RelationMapper().run()
