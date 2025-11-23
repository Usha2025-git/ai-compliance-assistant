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
    try:
        from .rag import answer_question
        
        llm = get_llm()
        
        # Your agent logic here
        result = answer_question(query, vectorstore)
        
        return {
            "retrieved_context": "Context retrieved from compliance documents",
            "risk_analysis": "Risk analysis based on query and documents",
            "pm_output": result if isinstance(result, str) else str(result)
        }
    except Exception as e:
        return {
            "retrieved_context": f"Error: {str(e)}",
            "risk_analysis": "Unable to analyze - check backend logs",
            "pm_output": f"Error occurred: {str(e)}"
        }