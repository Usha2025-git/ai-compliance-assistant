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
    Run the multi-agent pipeline with three-part analysis
    """
    try:
        from .rag import answer_question, get_embeddings, get_llm
        
        # Get similar documents (context retrieval)
        docs = vectorstore.similarity_search(query, k=3)
        context_text = "\n\n".join([d.page_content for d in docs]) if docs else "No documents found"
        
        llm = get_llm()
        
        # 1. Extract Retrieved Context
        retrieved_context = context_text[:500] + "..." if len(context_text) > 500 else context_text
        
        # 2. Generate Risk Analysis
        risk_prompt = f"""Analyze the compliance risk for this question based on the provided documents.

DOCUMENTS:
{context_text}

QUESTION: {query}

Provide a concise risk assessment (2-3 sentences) highlighting potential compliance issues."""
        
        risk_response = llm.invoke(risk_prompt)
        risk_analysis = risk_response.content if hasattr(risk_response, 'content') else str(risk_response)
        
        # 3. Generate Product Manager Recommendations
        pm_prompt = f"""As a compliance officer, provide specific recommendations for a product manager.

DOCUMENTS:
{context_text}

QUESTION: {query}

Provide 3-4 actionable recommendations with specific compliance requirements."""
        
        pm_response = llm.invoke(pm_prompt)
        pm_output = pm_response.content if hasattr(pm_response, 'content') else str(pm_response)
        
        return {
            "retrieved_context": retrieved_context,
            "risk_analysis": risk_analysis,
            "pm_output": pm_output
        }
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback.print_exc()
        return {
            "retrieved_context": f"Error retrieving context: {error_msg}",
            "risk_analysis": f"Unable to analyze risk: {error_msg}",
            "pm_output": f"Unable to generate recommendations: {error_msg}"
        }