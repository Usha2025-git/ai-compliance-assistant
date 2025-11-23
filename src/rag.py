from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.vectorstores import Chroma
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Initialize as None - will be created lazily
_embeddings = None
_llm = None


def get_embeddings():
    """Lazy initialization of embeddings"""
    global _embeddings
    if _embeddings is None:
        _embeddings = OpenAIEmbeddings()  # No api_key parameter needed
    return _embeddings


def get_llm():
    """Lazy initialization of LLM"""
    global _llm
    if _llm is None:
        _llm = OpenAI()  # No api_key parameter needed
    return _llm


def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_text(text)


def build_vectorstore(chunks):
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=get_embeddings(),  # ✅ Call function instead
        collection_name="compliance_docs"
    )
    return vectorstore


def answer_question(query, vectorstore):
    docs = vectorstore.similarity_search(query, k=3)
    context = "\n\n".join([d.page_content for d in docs])
    
    prompt = f"""
You are a compliance assistant. Answer ONLY using the information below:

{context}

Question: {query}
"""
    
    llm = get_llm()  # ✅ Call function instead
    response = llm(prompt)
    return response