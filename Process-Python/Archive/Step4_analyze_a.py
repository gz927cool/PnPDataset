import csv
import pdfplumber
import difflib
import re

csv_path = r"c:\Users\001\Desktop\list\03-CSV\A.csv"
pdf_path = r"c:\Users\001\Desktop\list\01-PDF\A.pdf"

def normalize(text):
    # Remove multiple spaces, newlines, and make lower case
    return re.sub(r'\s+', ' ', text).lower().strip()

def get_pdf_text(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        # Replace unprintable characters with ?
        print(text.encode('gbk', errors='replace').decode('gbk'))

def analyze_a():
    safe_print("Analyzing A.csv vs A.pdf details...")
    
    # 1. Get Data
    pdf_raw_text = get_pdf_text(pdf_path)
    pdf_norm_text = normalize(pdf_raw_text)
    
    csv_entries = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Main Entry']:
                csv_entries.append(row['Main Entry'])

    # 2. Analyze
    found_exact = 0
    found_fuzzy = 0
    not_found = []
    
    safe_print(f"\nTotal CSV Entries: {len(csv_entries)}")
    
    for entry in csv_entries:
        norm_entry = normalize(entry)
        # Remove quotes for search
        clean_entry = norm_entry.replace('"', '').replace("'", "")
        
        if clean_entry in pdf_norm_text:
            found_exact += 1
        else:
            # Fuzzy check 1: All words present in order (allowing garbage in between)
            words = clean_entry.split()
            if len(words) > 1:
                pattern = ".*".join([re.escape(w) for w in words])
                # Limit the distance between words to avoid false positives across pages
                # e.g. .{0,50} instead of .*
                pattern_tight = ".{0,50}".join([re.escape(w) for w in words])
                
                match = re.search(pattern_tight, pdf_norm_text)
                if match:
                    found_fuzzy += 1
                    span = match.span()
                    start = max(0, span[0] - 10)
                    end = min(len(pdf_norm_text), span[1] + 10)
                    found_text = pdf_norm_text[start:end]
                    safe_print(f"[Fuzzy Match] '{entry}' found as: '...{found_text}...'")
                    continue
            
            not_found.append(entry)

    safe_print(f"\nExact Matches: {found_exact}")
    safe_print(f"Fuzzy/Partial Matches: {found_fuzzy}")
    safe_print(f"Missing: {len(not_found)}")
    
    safe_print("\n--- Detailed Missing Items Analysis ---")
    for item in not_found:
        safe_print(f"MISSING: {item}")
        first_word = item.split()[0].lower().replace('"', '').replace("'", "")
        if len(first_word) > 3:
            # Find occurrences of the first word in PDF
            start_indices = [m.start() for m in re.finditer(re.escape(first_word), pdf_norm_text)]
            if start_indices:
                candidates = []
                for idx in start_indices:
                    # Grab a chunk of text of similar length
                    chunk = pdf_norm_text[idx : idx + len(item) + 20]
                    ratio = difflib.SequenceMatcher(None, normalize(item), chunk).ratio()
                    if ratio > 0.4: 
                        candidates.append((ratio, chunk))
                
                if candidates:
                    candidates.sort(key=lambda x: x[0], reverse=True)
                    best = candidates[0]
                    safe_print(f"  -> Potential OCR candidate found: '...{best[1]}...' (Similarity: {best[0]:.2f})")
                else:
                    safe_print("  -> No close text candidate found starting with first word.")
            else:
                safe_print(f"  -> First word '{first_word}' not found in text.")

if __name__ == "__main__":
    analyze_a()
