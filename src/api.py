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

try:
    print("Loading PDFs...")
    text_data = load_pdfs()

    print("Chunking text...")
    chunks = chunk_text(text_data)

    print("Building vector database...")
    vectorstore = build_vectorstore(chunks)
    print("Vector database ready!")
except Exception as e:
    print(f"Error during initialization: {e}")
    import traceback
    traceback.print_exc()

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
        "status": "ok",
        "vectorstore_ready": vectorstore is not None
    }

@app.post("/analyze")
def analyze(request: QueryRequest):
    """
    Takes a 'query' and runs the multi-agent pipeline.
    """
    if vectorstore is None:
        return {"error": "Vector store not initialized"}
    
    result = run_pipeline(request.query, vectorstore)
    return result