from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Initialize as None - will be created lazily
_embeddings = None
_client = None


def get_embeddings():
    """Lazy initialization of embeddings using native OpenAI client"""
    global _embeddings
    if _embeddings is None:
        def create_embedding(text):
            """Create embedding using native OpenAI client"""
            client = OpenAI()
            response = client.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            )
            return response.data[0].embedding
        _embeddings = create_embedding
    return _embeddings


class OpenAIEmbeddingFunction:
    """Custom embedding function to use with Chroma"""
    def __call__(self, texts):
        """Create embeddings for a list of texts - deprecated interface"""
        return self.embed_documents(texts)
    
    def embed_documents(self, texts):
        """Create embeddings for a list of texts - Chroma expected method"""
        client = OpenAI()
        embeddings = []
        for text in texts:
            response = client.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            )
            embeddings.append(response.data[0].embedding)
        return embeddings
    
    def embed_query(self, text):
        """Create embedding for a single query"""
        client = OpenAI()
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding


def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_text(text)


def build_vectorstore(chunks):
    try:
        embedding_function = OpenAIEmbeddingFunction()
        vectorstore = Chroma.from_texts(
            texts=chunks,
            embedding=embedding_function,
            collection_name="compliance_docs"
        )
        return vectorstore
    except Exception as e:
        print(f"Error building vectorstore: {e}")
        import traceback
        traceback.print_exc()
        return None


def answer_question(query, vectorstore):
    try:
        if vectorstore is None:
            return "Vector store not initialized. Please ensure PDFs are loaded."
        
        docs = vectorstore.similarity_search(query, k=3)
        
        if not docs or len(docs) == 0:
            return "No relevant compliance documents found for this query. Please upload compliance documents first."
        
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
        
        from openai import OpenAI
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during analysis: {str(e)}"