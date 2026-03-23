"""
====================================================================
🧠 BACKEND INSTRUCTIONS: LLM ENGINE (Ollama + LangChain)
====================================================================
This file connects the user's question, the Vector Database (Chroma), 
and the local Large Language Model (Ollama).

The Backend team works here.
"""

# TODO 1: Import Ollama, Chroma, HuggingFaceEmbeddings, and PromptTemplate from Langchain

DB_PATH = "../vector_db/"

def initialize_rag_system():
    """
    This function loads the LLM and the Database into memory.
    It should only be called once when the app starts.
    """
    # TODO 2: Load ChromaDB using the same embedding model from `ingest.py`.
    # TODO 3: Set up the 'retriever' (configure it to fetch the top 3-4 most relevant chunks).
    
    # TODO 4: Connect to the local Ollama instance (model="llama3" or "mistral").
    # Hint: Set temperature=0.0 to make the answers strict and factual, not creative!
    
    # TODO 5: Create a PromptTemplate (System Prompt).
    # Define how the AI should behave here. E.g., "You are a DEW21 assistant. Only use the context below..."
    
    # TODO 6: Create and return the RetrievalQA chain.
    pass

def generate_answer(qa_chain, question):
    """
    Takes the initialized chain and the user's question, and returns the answer + sources.
    The Frontend team will call this function!
    """
    # TODO 7: Execute qa_chain.invoke({"query": question})
    # TODO 8: Extract the answer text and the source document metadata.
    # Return a dictionary: {"answer": "text...", "sources": ["doc1.pdf - page 2", ...]}
    pass