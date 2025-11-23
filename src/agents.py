from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-3.5-turbo")

def run_pipeline(query, vectorstore):
    # Agent 1: Retriever
    docs = vectorstore.similarity_search(query, k=3)
    context = "\n\n".join([d.page_content for d in docs])
    
    # Agent 2: Risk Analysis
    risk_prompt = f"""
Based on this compliance context:
{context}

Question: {query}

Provide a risk assessment (HIGH/MEDIUM/LOW) and explain why.
"""
    risk_analysis = llm.predict(risk_prompt)
    
    # Agent 3: PM Output
    pm_prompt = f"""
Based on this compliance context:
{context}

Risk Analysis:
{risk_analysis}

Question: {query}

Create:
1. User story (As a... I want... So that...)
2. Acceptance criteria (3 bullet points)
3. Product recommendation
"""
    pm_output = llm.predict(pm_prompt)
    
    return {
        "retrieved_context": context,
        "risk_analysis": risk_analysis,
        "pm_output": pm_output
    }