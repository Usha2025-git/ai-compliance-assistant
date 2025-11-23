from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Lazy initialization - do NOT instantiate at module load
_llm = None

def get_llm():
    global _llm
    if _llm is None:
        _llm = ChatOpenAI(model="gpt-3.5-turbo")
    return _llm


def run_pipeline(query, vectorstore):
    """
    Run the multi-agent pipeline
    """
    from .rag import answer_question
    
    llm = get_llm()
    
    # Your agent logic here
    result = answer_question(query, vectorstore)
    
    return {
        "retrieved_context": "...",
        "risk_analysis": "...",
        "pm_output": result
    }