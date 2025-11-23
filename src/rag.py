from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import Chroma
import os
from dotenv import load_dotenv
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

load_dotenv()

# Initialize embeddings
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
# Initialize LLM
llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))

def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_text(text)

def build_vectorstore(chunks):
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        collection_name="compliance_docs"
    )
    return vectorstore

def answer_question(query, vectorstore):
    # Retrieve relevant chunks
    docs = vectorstore.similarity_search(query, k=3)
    
    # Combine retrieved text
    context = "\n\n".join([d.page_content for d in docs])
    
    # Ask LLM to answer
    prompt = f"""
You are a compliance assistant. Answer ONLY using the information below:

{context}

Question: {query}
"""
    response = llm.invoke(prompt)  # ← CHANGED THIS LINE
    return response