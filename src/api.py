from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from .ingest import load_pdfs
from .rag import chunk_text, build_vectorstore
from .agents import run_pipeline

# -------- SETUP ONLY ONCE -------- #

vectorstore = None
initialization_error = None

try:
    print("=" * 60)
    print("INITIALIZING AI COMPLIANCE ASSISTANT")
    print("=" * 60)
    
    print("Loading PDFs...")
    text_data = load_pdfs()
    print(f"[SUCCESS] Loaded {len(text_data)} characters from PDFs")

    if text_data and len(text_data) > 100:  # Must have meaningful content
        print("Chunking text...")
        chunks = chunk_text(text_data)
        print(f"[SUCCESS] Created {len(chunks)} chunks")

        print("Building vector database...")
        vectorstore = build_vectorstore(chunks)
        print(f"[SUCCESS] Vector database ready! Loaded {len(chunks)} chunks")
    else:
        print("[WARNING] No PDF content found - vectorstore will be empty")
        initialization_error = "No PDFs loaded"
except Exception as e:
    print(f"[ERROR] Error during initialization: {e}")
    import traceback
    traceback.print_exc()
    initialization_error = str(e)

print("=" * 60)

# -------- FASTAPI APP -------- #

app = FastAPI(title="AI Compliance Assistant", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def root():
    """Serve frontend HTML"""
    frontend_path = os.path.join(os.path.dirname(__file__), 'frontend', 'index.html')
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"message": "Frontend not found"}

@app.get("/health")
def health():
    """Health check endpoint"""
    return {
        "status": "ok" if vectorstore is not None else "error",
        "vectorstore_ready": vectorstore is not None,
        "initialization_error": initialization_error,
        "message": "Vectorstore ready and documents loaded" if vectorstore is not None else f"Vectorstore not initialized: {initialization_error}"
    }

@app.post("/analyze")
def analyze(request: QueryRequest):
    """
    Takes a 'query' and runs the multi-agent pipeline.
    """
    if vectorstore is None:
        return {
            "error": "Vector store not initialized",
            "details": initialization_error or "PDFs not loaded on startup. Check if data/ folder exists with PDF files.",
            "retrieved_context": "ERROR: No documents available",
            "risk_analysis": "ERROR: Cannot analyze - no compliance documents loaded",
            "pm_output": "ERROR: Please ensure PDF files are in the data/ folder and the vectorstore initialized successfully"
        }
    
    result = run_pipeline(request.query, vectorstore)
    return result