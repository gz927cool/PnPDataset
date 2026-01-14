import pandas as pd
from src.config import config

class Step0Preprocessor:
    def run(self, limit=None):
        print(f"Step 0: Preprocessing data... (Limit: {limit})")
        
        # Load data
        triplets_df = pd.read_csv(config.TRIPLETS_PATH)
        if limit:
            triplets_df = triplets_df.head(limit)
        source_df = pd.read_csv(config.SOURCE_DATA_PATH)
        
        # Create a dictionary for fast lookup of source documents
        # Assuming 'index' column in source_df matches 'Row_Index' in triplets_df
        source_df.set_index('index', inplace=True)
        source_dict = source_df.to_dict('index')
        
        processed_rows = []
        
        for _, row in triplets_df.iterrows():
            row_index = row['Row_Index']
            triple_index = row['Index']
            
            # Generate unique triple_id
            triple_id = f"T_{row_index}_{triple_index}"
            
            # Get source info
            source_info = source_dict.get(row_index, {})
            
            # Construct source sentence/context
            # Concatenate relevant fields to form a context
            parts = [
                str(source_info.get('Index_Main Entry', '')),
                str(source_info.get('Index_Location', '')),
                str(source_info.get('Index_Sub-entry', '')),
                str(source_info.get('Index_Detail', '')),
                str(source_info.get('Index_Page Numbers', ''))
            ]
            # Filter out 'nan' and empty strings
            valid_parts = [p for p in parts if p and p.lower() != 'nan']
            source_sentence = ". ".join(valid_parts)
            
            # Create new row
            new_row = {
                'triple_id': triple_id,
                'subject': row['主体 (Subject)'],
                'relation': row['谓词 (Predicate)'],
                'object': row['客体 (Object)'],
                'source_doc': row_index,
                'source_sentence': source_sentence,
                'confidence': 1.0  # Default confidence
            }
            processed_rows.append(new_row)
            
        # Create DataFrame
        output_df = pd.DataFrame(processed_rows)
        
        # Save to CSV
        output_df.to_csv(config.TRIPLES_RAW_PATH, index=False)
        print(f"Step 0 completed. Saved {len(output_df)} rows to {config.TRIPLES_RAW_PATH}")

if __name__ == "__main__":
    Step0Preprocessor().run()
