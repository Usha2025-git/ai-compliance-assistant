from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
import os
from dotenv import load_dotenv

load_dotenv()

def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_text(text)

embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

def build_vectorstore(chunks):
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        collection_name="compliance_docs"
    )
    return vectorstore

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-3.5-turbo")

def answer_question(query, vectorstore):
    docs = vectorstore.similarity_search(query, k=3)
    context = "\n\n".join([d.page_content for d in docs])
    
    prompt = f"""
You are a compliance assistant. Answer ONLY using the information below:

{context}

Question: {query}
"""
    
    response = llm.predict(prompt)
    return response