from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7
)

def run_pipeline(query, vectorstore):
    """
    Multi-agent pipeline:
    1. Retriever Agent - gets relevant docs
    2. Risk Agent - analyzes compliance risk
    3. PM Agent - generates product recommendations
    """
    
    # AGENT 1: Retriever Agent
    docs = vectorstore.similarity_search(query, k=3)
    retrieved_context = "\n\n".join([d.page_content for d in docs])
    
    # AGENT 2: Risk Assessment Agent
    risk_prompt = f"""
You are a compliance risk analyst. Based on the following context, analyze the risk level.

Context:
{retrieved_context}

Question: {query}

Provide:
1. Risk Level (Low/Medium/High)
2. Key compliance concerns
3. Recommended actions

Keep it concise.
"""
    risk_analysis = llm.invoke(risk_prompt).content
    
    # AGENT 3: PM Output Agent
    pm_prompt = f"""
You are a Product Manager. Based on this compliance analysis, create:

Context: {retrieved_context}

Risk Analysis: {risk_analysis}

Question: {query}

Provide:
1. User Story (As a [user], I want [goal], so that [benefit])
2. Acceptance Criteria (3 bullet points)
3. Product Recommendation

Keep it professional and concise.
"""
    pm_output = llm.invoke(pm_prompt).content
    
    # Return structured response
    return {
        "retrieved_context": retrieved_context,
        "risk_analysis": risk_analysis,
        "pm_output": pm_output
    }