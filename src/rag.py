from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import Chroma
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
    try:
        docs = vectorstore.similarity_search(query, k=3)
        
        if not docs:
            return "No relevant compliance documents found for this query."
        
        context = "\n\n".join([d.page_content for d in docs])
        
        prompt = f"""You are a compliance assistant. Analyze the following query based on the compliance documents provided.

COMPLIANCE CONTEXT:
{context}

USER QUERY: {query}

Please provide:
1. A direct answer to the question
2. Relevant compliance rules or requirements found
3. Risk assessment
4. Recommendations

Keep your response concise and actionable."""
        
        llm = get_llm()
        response = llm(prompt)
        return response if response else "Analysis completed but no specific guidance available."
    except Exception as e:
        return f"Error during analysis: {str(e)}"