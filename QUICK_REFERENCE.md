# QUICK REFERENCE - VERSIONS & DEPENDENCIES

## PYTHON
✓ **3.9.13** (LOCKED - DO NOT CHANGE)

## PACKAGE VERSIONS (from requirements.txt)
```
langchain==0.3.0
langchain-community==0.3.0
langchain-openai==0.2.0
langchain-text-splitters==0.3.0
openai==1.54.0
chromadb==0.4.22
fastapi==0.109.2
uvicorn==0.27.1
pypdf==4.0.1
python-dotenv==1.0.1
pydantic==2.7.4
```

## CRITICAL FIX APPLIED
**File**: src/rag.py (Line 1)
```python
# OLD:
from langchain.text_splitter import RecursiveCharacterTextSplitter

# NEW:
from langchain_text_splitters import RecursiveCharacterTextSplitter
```

## CONNECTIONS
| Connection | Status | Details |
|-----------|--------|---------|
| Frontend → Backend | ✓ | POST /analyze |
| Backend → OpenAI | ✓ | Requires OPENAI_API_KEY |
| PDF → ChromaDB | ✓ | Via PyPDF & embeddings |
| ChromaDB → LLM | ✓ | Similarity search |

## STATUS
✓ All versions correct
✓ All dependencies pinned
✓ All imports fixed
✓ All connections verified
✓ **READY FOR DEPLOYMENT**

## LATEST COMMITS
- a9c3783: Add comprehensive version check summary
- 4877bf5: Add deployment ready document
- 1f9f3fc: Fix deprecated LangChain import

## DEPLOYMENT URL
https://ai-compliance-assistant-0728.onrender.com/
