import csv
import pdfplumber
import re
import os

csv_path = r"c:\Users\001\Desktop\list\03-CSV\A.csv"
md_path = r"c:\Users\001\Desktop\list\02-LIST\A.md"
pdf_path = r"c:\Users\001\Desktop\list\01-PDF\A.pdf"

def normalize(text):
    if not text: return ""
    return re.sub(r'\s+', ' ', text).strip()

def get_pdf_text(path):
    text = ""
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def parse_md_table(path):
    rows = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        headers = []
        for line in lines:
            line = line.strip()
            if not line: continue
            if line.startswith('|') and '---' in line: continue # Separator
            
            # Split by pipe
            parts = [p.strip() for p in line.split('|')]
            # Remove empty first and last elements if they exist (due to leading/trailing pipes)
            if len(parts) > 0 and parts[0] == '': parts.pop(0)
            if len(parts) > 0 and parts[-1] == '': parts.pop(-1)
            
            if not headers:
                headers = parts
            else:
                row_dict = {}
                for i, h in enumerate(headers):
                    if i < len(parts):
                        row_dict[h] = parts[i]
                    else:
                        row_dict[h] = ""
                rows.append(row_dict)
    except Exception as e:
        print(f"Error reading MD: {e}")
    return rows

def compare_row(csv_row, md_rows, pdf_text_lower):
    errors = []
    
    # 1. Compare with MD
    # Find corresponding row in MD. Since we are iterating CSV, we assume 1-to-1 mapping order usually.
    # But let's try to find by content to be safe, or just use index if they are sorted same.
    # Given the file names, they are likely generated from each other. Let's try index matching first.
    
    # Actually, let's just look for an exact match in MD rows.
    md_match = None
    for md_row in md_rows:
        # Compare key fields
        if (normalize(md_row.get('Main Entry')) == normalize(csv_row.get('Main Entry')) and
            normalize(md_row.get('Sub-entry')) == normalize(csv_row.get('Sub-entry'))):
            md_match = md_row
            break
    
    if not md_match:
        errors.append("MD: 条目在 Markdown 文件中未找到 (Entry not found in MD)")
    else:
        # Compare details
        csv_loc = normalize(csv_row.get('Location'))
        md_loc = normalize(md_match.get('Location'))
        if csv_loc != md_loc:
            errors.append(f"MD: 地点不匹配 (Location mismatch) CSV='{csv_loc}' vs MD='{md_loc}'")
            
        csv_pages = normalize(csv_row.get('Page Numbers'))
        md_pages = normalize(md_match.get('Page Numbers'))
        # Normalize page numbers (remove spaces)
        if csv_pages.replace(' ', '') != md_pages.replace(' ', ''):
             errors.append(f"MD: 页码不匹配 (Page mismatch) CSV='{csv_pages}' vs MD='{md_pages}'")

    # 2. Compare with PDF (Validity)
    main_entry = csv_row.get('Main Entry', '')
    if main_entry:
        # Simple check
        clean_entry = main_entry.lower().replace('"', '').replace("'", "")
        # Remove comma for looser check
        clean_entry_no_comma = clean_entry.replace(',', '')
        
        if clean_entry in pdf_text_lower:
            pass # Found
        elif clean_entry_no_comma in pdf_text_lower.replace(',', ''):
            pass # Found without comma
        else:
            # Fuzzy check logic from before
            words = clean_entry.split()
            if len(words) > 1:
                pattern = ".*".join([re.escape(w) for w in words])
                if re.search(pattern, pdf_text_lower):
                    pass # Found fuzzy
                else:
                     errors.append("PDF: PDF中未找到该条目 (Entry not found in PDF - Potential OCR error)")
            else:
                errors.append("PDF: PDF中未找到该条目 (Entry not found in PDF)")

    return errors

def analyze_all():
    print("Loading files...")
    csv_rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            csv_rows.append(row)
            
    md_rows = parse_md_table(md_path)
    pdf_text = get_pdf_text(pdf_path)
    pdf_text_lower = normalize(pdf_text).lower()
    
    print(f"CSV Rows: {len(csv_rows)}")
    print(f"MD Rows: {len(md_rows)}")
    
    print("\n--- Analysis Report (CSV as Subject) ---")
    print("| Row | Main Entry | Errors/Discrepancies |")
    print("| :--- | :--- | :--- |")
    
    for i, row in enumerate(csv_rows):
        errors = compare_row(row, md_rows, pdf_text_lower)
        if errors:
            entry_display = row.get('Main Entry', '')
            if row.get('Sub-entry'):
                entry_display += f" ({row.get('Sub-entry')})"
            
            error_str = "<br>".join(errors)
            print(f"| {i+1} | {entry_display} | {error_str} |")

if __name__ == "__main__":
    analyze_all()
