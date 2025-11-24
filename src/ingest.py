from pypdf import PdfReader
import os

def load_pdfs(folder_path=None):
    if folder_path is None:
        # Use absolute path relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(os.path.dirname(current_dir), "data")
    
    all_text = ""
    
    # Create data folder if it doesn't exist
    if not os.path.exists(folder_path):
        print(f"Data folder not found at {folder_path}")
        return ""

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            try:
                reader = PdfReader(pdf_path)
                for page in reader.pages:
                    text = page.extract_text() or ""
                    all_text += text + "\n"
                print(f"Loaded: {filename}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")

    return all_text

if __name__ == "__main__":
    text = load_pdfs()
    print("Loaded PDF characters:", len(text))

