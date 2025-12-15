import pdfplumber

pdf_path = r"c:\Users\001\Desktop\list\01-PDF\A.pdf"

try:
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}")
        if len(pdf.pages) > 0:
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            with open("pdf_content.txt", "w", encoding="utf-8") as f:
                f.write(text)
            print("Text written to pdf_content.txt")
except Exception as e:
    print(f"Error: {e}")
