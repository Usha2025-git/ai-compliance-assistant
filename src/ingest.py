from pypdf import PdfReader
import os

def load_pdfs(folder_path=None):
    if folder_path is None:
        # Use absolute path relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(os.path.dirname(current_dir), "data")
    
    print(f"  Looking for PDFs in: {folder_path}")
    
    all_text = ""
    pdf_count = 0
    
    # Create data folder if it doesn't exist
    if not os.path.exists(folder_path):
        print(f"  [WARNING] Data folder not found at {folder_path}")
        return ""

    try:
        files = os.listdir(folder_path)
        print(f"  Found {len(files)} files in data folder")
        
        for filename in files:
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(folder_path, filename)
                try:
                    print(f"  Processing: {filename}")
                    reader = PdfReader(pdf_path)
                    page_count = len(reader.pages)
                    
                    for page in reader.pages:
                        text = page.extract_text() or ""
                        all_text += text + "\n"
                    
                    pdf_count += 1
                    print(f"  [OK] Loaded: {filename} ({page_count} pages)")
                except Exception as e:
                    print(f"  [ERROR] Error loading {filename}: {e}")
        
        print(f"  [SUCCESS] Successfully loaded {pdf_count} PDF(s)")
    except Exception as e:
        print(f"  [ERROR] Error reading folder: {e}")

    return all_text

if __name__ == "__main__":
    text = load_pdfs()
    print("Loaded PDF characters:", len(text))

