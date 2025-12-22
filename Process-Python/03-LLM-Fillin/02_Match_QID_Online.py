import pandas as pd
import requests
import time
import os
import urllib.parse
from difflib import SequenceMatcher

# Paths
base_dir = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin"
input_file = os.path.join(base_dir, "02-LLM_Fillin_Merged_Split.csv")
output_file = os.path.join(base_dir, "03-LLM_Fillin_With_QID.csv")

# Wikidata API
API_URL = "https://www.wikidata.org/w/api.php"
# Add User-Agent to comply with Wikidata policy
HEADERS = {
    "User-Agent": "PnPDatasetBot/1.0 (https://github.com/PnPDataset/PnPDataset; myemail@example.com) python-requests/2.32.3"
}

def search_wikidata(query, limit=5):
    """Search Wikidata for entities matching the query."""
    if not query or not isinstance(query, str) or len(query.strip()) < 2:
        return []
        
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "language": "en",
        "type": "item",
        "search": query,
        "limit": limit
    }
    
    try:
        response = requests.get(API_URL, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("search", [])
    except Exception as e:
        print(f"Error searching for '{query}': {e}")
        return []

def get_entity_details(qid):
    """Get details for a specific QID."""
    params = {
        "action": "wbgetentities",
        "format": "json",
        "ids": qid,
        "props": "labels|descriptions|claims",
        "languages": "en"
    }
    
    try:
        response = requests.get(API_URL, params=params, headers=HEADERS, timeout=10)
        data = response.json()
        return data.get("entities", {}).get(qid, {})
    except Exception as e:
        print(f"Error getting details for '{qid}': {e}")
        return {}

def similarity(a, b):
    return SequenceMatcher(None, str(a).lower(), str(b).lower()).ratio()

def match_row(row):
    """
    Attempt to match a row to a Wikidata item.
    Returns: (qid, label, description, score, method)
    """
    formal_name = row.get("英文正式名称 (Formal Name)", "")
    original_name = row.get("原始名称 (CSV)", "")
    desc_en = row.get("Description_EN", "")
    desc_cn = row.get("Description_CN", "")
    entity_type = row.get("实体类型", "")
    
    # Strategy Refinement:
    # 1. Search by Formal Name
    # 2. Search by Original Name (if different)
    # 3. Search by combination of Name + Entity Type
    # 4. Search by Name + Context (Creator/Location) - NEW
    # 5. Name Permutations (e.g. "Name, Surname" -> "Surname Name") - NEW
    
    queries = []
    
    # Clean names
    clean_formal = formal_name.strip()
    
    queries.append((clean_formal, "Formal Name"))
    
    if original_name and original_name != formal_name:
        queries.append((original_name, "Original Name"))
    
    # Contextual Queries
    if entity_type == "人名":
        queries.append((f"{clean_formal} painter", "Name + Painter"))
        queries.append((f"{clean_formal} artist", "Name + Artist"))
        queries.append((f"{clean_formal} architect", "Name + Architect"))
    elif entity_type == "作品":
        queries.append((f"{clean_formal} painting", "Name + Painting"))
        
        # Try to extract "By Author" from description
        if desc_en and isinstance(desc_en, str):
            # Look for "by [Name]" pattern
            import re
            match = re.search(r'\b(by|attributed to)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})', desc_en)
            if match:
                author = match.group(2)
                queries.append((f"{clean_formal} {author}", "Name + Extracted Author"))
                
    elif entity_type == "机构":
        queries.append((f"{clean_formal} academy", "Name + Academy"))
        queries.append((f"{clean_formal} museum", "Name + Museum"))

    # Name Permutation: "Last, First" -> "First Last"
    if "," in clean_formal:
        parts = clean_formal.split(",")
        if len(parts) == 2:
            swapped = f"{parts[1].strip()} {parts[0].strip()}"
            queries.append((swapped, "Swapped Name"))
            
    # Parentheses removal: "Name (Context)" -> "Name"
    if "(" in clean_formal:
        base_name = clean_formal.split("(")[0].strip()
        if len(base_name) > 3:
             queries.append((base_name, "Name without Parens"))
             
    # Stopword removal for Artworks
    if clean_formal.lower().startswith("the "):
        queries.append((clean_formal[4:], "Name without 'The'"))

    all_candidates = []
    seen_ids = set()
    
    for q, q_type in queries:
        results = search_wikidata(q, limit=5)
        for res in results:
            if res['id'] not in seen_ids:
                res['query_type'] = q_type
                all_candidates.append(res)
                seen_ids.add(res['id'])
        time.sleep(0.2)
        
    if not all_candidates:
        return None, None, None, 0, "No Match"
        
    # Evaluate Candidates
    best_score = 0
    best_match = None
    
    for cand in all_candidates:
        score = 0
        cand_label = cand.get("label", "")
        cand_desc = cand.get("description", "")
        cand_id = cand.get("id", "")
        
        # 1. Name Similarity (Base)
        name_sim = max(similarity(formal_name, cand_label), similarity(original_name, cand_label))
        score += name_sim * 0.5
        
        # 2. Description/Context Matching
        cand_text = (str(cand_label) + " " + str(cand_desc)).lower()
        
        # Positive Keywords from our Description
        if desc_en and isinstance(desc_en, str):
            # Extract potential keywords (capitalized words, years)
            # Simple approach: just check word overlap
            my_words = set([w for w in desc_en.lower().split() if len(w) > 3])
            overlap = sum(1 for w in my_words if w in cand_text)
            score += min(overlap * 0.1, 0.4) # Max 0.4 bonus
            
        # 3. Entity Type Validation (Negative penalties)
        # Relaxed: Only penalize strong contradictions
        is_human = "human" in cand_desc.lower() or "painter" in cand_desc.lower() or "born" in cand_desc.lower()
        is_work = "painting" in cand_desc.lower() or "canvas" in cand_desc.lower()
        
        # 4. Exact Match Bonus
        if name_sim > 0.9:
            score += 0.3
        elif name_sim > 0.8:
            score += 0.2
            
        # 5. Partial Match Bonus (e.g. "Church of X" matching "X")
        if len(formal_name) > 5 and formal_name in cand_label:
            score += 0.2
            
        if score > best_score:
            best_score = score
            best_match = (cand_id, cand_label, cand_desc, score, f"Relaxed Match ({cand.get('query_type')})")

    # Relaxed Threshold
    if best_score > 0.35:
        return best_match
             
    return None, None, None, 0, "Low Confidence"

def main():
    # Force use of the output file as the base to continue work
    if os.path.exists(output_file):
        print(f"Loading existing results from {output_file}...")
        df = pd.read_csv(output_file)
    else:
        print(f"Reading {input_file}...")
        try:
            df = pd.read_csv(input_file, encoding='utf-8-sig')
        except:
            df = pd.read_csv(input_file, encoding='gbk')
            
    # Add columns if not exist
    new_cols = ['Matched_QID', 'Matched_Label', 'Matched_Desc', 'Match_Score', 'Match_Method']
    for col in new_cols:
        if col not in df.columns:
            df[col] = None

    print(f"Total rows: {len(df)}")
    
    save_interval = 10
    
    for index, row in df.iterrows():
        # Skip if already matched (and not empty)
        # Check if QID exists and looks valid
        current_qid = str(row.get('Matched_QID', ''))
        if current_qid.startswith('Q') and pd.notna(row.get('Matched_QID')):
            continue
            
        print(f"Processing {index+1}/{len(df)}: {row.get('英文正式名称 (Formal Name)', 'Unknown')}")
        
        qid, label, desc, score, method = match_row(row)
        
        if qid:
            print(f"  -> Match: {qid} ({label}) - Score: {score:.2f}")
            df.at[index, 'Matched_QID'] = qid
            df.at[index, 'Matched_Label'] = label
            df.at[index, 'Matched_Desc'] = desc
            df.at[index, 'Match_Score'] = score
            df.at[index, 'Match_Method'] = method
        else:
            print("  -> No match found.")
            df.at[index, 'Match_Method'] = "Failed (Relaxed)"
            
        time.sleep(0.3) # Slightly faster
        
        if (index + 1) % save_interval == 0:
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"Saved progress to {output_file}")

    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print("Done.")

if __name__ == "__main__":
    main()
