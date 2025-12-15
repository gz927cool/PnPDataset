import csv
import pdfplumber
import os
import glob

csv_dir = r"c:\Users\001\Desktop\list\03-CSV"
pdf_dir = r"c:\Users\001\Desktop\list\01-PDF"
report_file = r"c:\Users\001\Desktop\list\verification_report.txt"

# Mapping from CSV filename to PDF filename(s)
# If not in map, assume same name with .pdf extension
file_mapping = {
    "H.csv": ["H-I-J-K.pdf"],
    "I.csv": ["H-I-J-K.pdf"],
    "J，K.csv": ["H-I-J-K.pdf"],
    "N.csv": ["N-O.pdf"],
    "O.csv": ["N-O.pdf"],
    "P.csv": ["P-Q.pdf"],
    "Q-R.csv": ["P-Q.pdf", "R.pdf"],
}

def normalize_text(text):
    return text.replace('\n', ' ').replace('  ', ' ').lower()

def get_pdf_text(pdf_filename):
    pdf_path = os.path.join(pdf_dir, pdf_filename)
    if not os.path.exists(pdf_path):
        print(f"Warning: PDF not found: {pdf_path}")
        return ""
    
    text_content = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_content += text + "\n"
    except Exception as e:
        print(f"Error reading {pdf_filename}: {e}")
    return normalize_text(text_content)

def verify_all():
    csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))
    
    # Cache PDF content to avoid re-reading
    pdf_cache = {}
    
    with open(report_file, "w", encoding="utf-8") as report:
        report.write("Verification Report\n")
        report.write("===================\n\n")
        
        for csv_file in csv_files:
            csv_filename = os.path.basename(csv_file)
            report.write(f"Processing {csv_filename}...\n")
            print(f"Processing {csv_filename}...")
            
            # Determine corresponding PDF(s)
            if csv_filename in file_mapping:
                pdf_filenames = file_mapping[csv_filename]
            else:
                # Default mapping: A.csv -> A.pdf
                pdf_filename = csv_filename.replace(".csv", ".pdf")
                pdf_filenames = [pdf_filename]
            
            # Get text from all mapped PDFs
            full_pdf_text = ""
            for pdf_name in pdf_filenames:
                if pdf_name not in pdf_cache:
                    print(f"  Reading PDF: {pdf_name}")
                    pdf_cache[pdf_name] = get_pdf_text(pdf_name)
                full_pdf_text += pdf_cache[pdf_name]
            
            # Read CSV entries
            entries = []
            try:
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        entries.append(row)
            except Exception as e:
                report.write(f"  Error reading CSV: {e}\n")
                continue
                
            found_count = 0
            missing_count = 0
            missing_entries = []
            
            for entry in entries:
                main_entry = entry.get('Main Entry', '')
                if not main_entry:
                    continue
                    
                search_term = main_entry.lower().strip()
                search_term = search_term.replace('"', '').replace("'", "")
                
                # Check existence
                # Try exact match first
                if search_term in full_pdf_text:
                    found_count += 1
                else:
                    # Try without commas
                    if search_term.replace(',', '') in full_pdf_text.replace(',', ''):
                        found_count += 1
                    else:
                        missing_count += 1
                        missing_entries.append(main_entry)
            
            report.write(f"  Total Entries: {len(entries)}\n")
            report.write(f"  Found: {found_count}\n")
            report.write(f"  Missing: {missing_count}\n")
            if missing_entries:
                report.write("  Missing Entries (Potential OCR/Format mismatch):\n")
                for missing in missing_entries:
                    report.write(f"    - {missing}\n")
            report.write("\n")
            
    print(f"Verification complete. Report saved to {report_file}")

if __name__ == "__main__":
    verify_all()
