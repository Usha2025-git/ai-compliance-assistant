from pypdf import PdfReader
import os

def load_pdfs(folder_path=None):
    if folder_path is None:
        # Try multiple possible paths for flexibility
        possible_paths = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"),  # Parent/data
            os.path.join(os.getcwd(), "data"),  # Current working dir
            "/data",  # Root level
            "./data",  # Relative
        ]
        
        # Find first path that exists
        folder_path = None
        for path in possible_paths:
            abs_path = os.path.abspath(path)
            print(f"  Checking: {abs_path}")
            if os.path.exists(abs_path):
                folder_path = abs_path
                print(f"  Found data folder at: {folder_path}")
                break
        
        if folder_path is None:
            print(f"  [ERROR] No data folder found in any expected location")
            print(f"  Searched: {possible_paths}")
            return ""
    
    print(f"  Using data folder: {folder_path}")
    
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

