import pandas as pd
from src.config import config

class Step6GraphBuilder:
    def run(self):
        print("Step 6: Building Graph Ingestion Files...")
        
        facts_df = pd.read_csv(config.FACTS_SEMANTIC_PATH, sep='\t')
        candidates_df = pd.read_csv(config.ENTITIES_CANDIDATES_PATH)
        
        # Build Nodes
        # We need label and type for each QID. 
        # We can look up from candidates_df (take the first occurrence or best score)
        
        # Prepare lookup
        # Sort candidates by score to get best metadata
        candidates_sorted = candidates_df.sort_values('score', ascending=False)
        qid_meta = {}
        for _, row in candidates_sorted.iterrows():
            qid = row['candidate_qid']
            if qid not in qid_meta:
                qid_meta[qid] = {
                    'label': row['candidate_label'],
                    'entity_type': row['entity_type'] if pd.notna(row['entity_type']) else 'Thing'
                }
        
        nodes = {}
        node_counter = 1
        
        def get_node_id(qid):
            nonlocal node_counter
            if qid not in nodes:
                meta = qid_meta.get(qid, {'label': qid, 'entity_type': 'Unknown'})
                nodes[qid] = {
                    'id': node_counter,
                    'qid': qid,
                    'name': meta['label'],
                    'label': 'Entity', # Neo4j label, could be more specific
                    'entity_type': meta['entity_type'],
                    'source': 'wikidata'
                }
                node_counter += 1
            return nodes[qid]['id']
            
        relations = []
        
        for _, row in facts_df.iterrows():
            subj_qid = row['subject_uri'].replace('wd:', '')
            obj_qid = row['object_uri'].replace('wd:', '')
            pred_pid = row['predicate_uri'].replace('wdt:', '')
            
            s_id = get_node_id(subj_qid)
            o_id = get_node_id(obj_qid)
            
            relations.append({
                'start_id': s_id,
                'relation': pred_pid,
                'end_id': o_id,
                'fact_id': row['fact_id'],
                'source_triple': row['source_triple'],
                'confidence': row['confidence']
            })
            
        # Output Nodes
        nodes_df = pd.DataFrame(list(nodes.values()))
        nodes_df.to_csv(config.NODES_PATH, index=False)
        
        # Output Relations
        relations_df = pd.DataFrame(relations)
        relations_df.to_csv(config.RELATIONS_PATH, index=False)
        
        print(f"Step 6 completed. Generated {len(nodes_df)} nodes and {len(relations_df)} relations.")

if __name__ == "__main__":
    Step6GraphBuilder().run()
