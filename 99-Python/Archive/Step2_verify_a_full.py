import csv
import pdfplumber
import os

csv_path = r"c:\Users\001\Desktop\list\03-CSV\A.csv"
pdf_path = r"c:\Users\001\Desktop\list\01-PDF\A.pdf"

def normalize_text(text):
    return text.replace('\n', ' ').replace('  ', ' ').lower()

def verify_file(csv_file, pdf_file):
    print(f"Verifying {os.path.basename(csv_file)} against {os.path.basename(pdf_file)}...")
    
    # Read CSV
    entries = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append(row)
            
    # Read PDF
    pdf_text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pdf_text += text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return

    pdf_text_lower = normalize_text(pdf_text)
    
    found_count = 0
    missing_count = 0
    
    print(f"Checking {len(entries)} entries...")
    
    for entry in entries:
        main_entry = entry['Main Entry']
        # Simple check: is the main entry string in the PDF text?
        # We might need to be careful about partial matches, but for verification, exact string search (case insensitive) is a good start.
        
        # Clean up entry for search
        search_term = main_entry.lower().strip()
        if search_term in pdf_text_lower:
            found_count += 1
        else:
            missing_count += 1
            print(f"MISSING: '{main_entry}'")

    print(f"Summary: Found {found_count}, Missing {missing_count}")

if __name__ == "__main__":
    verify_file(csv_path, pdf_path)
