from ingest import load_pdfs
from rag import chunk_text, build_vectorstore, answer_question

# Load PDFs
text = load_pdfs()

# Chunk the text
chunks = chunk_text(text)

# Build vector store
vs = build_vectorstore(chunks)

# Ask questions
while True:
    q = input("Ask a question: ")
    if q.lower() == 'quit' or q.lower() == 'exit':
        break
    print(answer_question(q, vs))