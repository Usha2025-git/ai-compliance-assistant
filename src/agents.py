from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = None

def get_client():
    global client
    if client is None:
        client = OpenAI()
    return client


def run_pipeline(query, vectorstore):
    """
    Run the multi-agent pipeline with three-part analysis
    """
    try:
        # Check API key first
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set. Please set your OpenAI API key.")
        
        # Get similar documents (context retrieval)
        docs = vectorstore.similarity_search(query, k=3)
        context_text = "\n\n".join([d.page_content for d in docs]) if docs else "No documents found"
        
        openai_client = get_client()
        
        # 1. Extract Retrieved Context
        retrieved_context = context_text[:500] + "..." if len(context_text) > 500 else context_text
        
        # 2. Generate Risk Analysis
        risk_prompt = f"""Analyze the compliance risk for this question based on the provided documents.

DOCUMENTS:
{context_text}

QUESTION: {query}

Provide a concise risk assessment (2-3 sentences) highlighting potential compliance issues."""
        
        risk_response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": risk_prompt}],
            temperature=0.7
        )
        risk_analysis = risk_response.choices[0].message.content
        
        # 3. Generate Product Manager Recommendations
        pm_prompt = f"""As a compliance officer, provide specific recommendations for a product manager.

DOCUMENTS:
{context_text}

QUESTION: {query}

Provide 3-4 actionable recommendations with specific compliance requirements."""
        
        pm_response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": pm_prompt}],
            temperature=0.7
        )
        pm_output = pm_response.choices[0].message.content
        
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