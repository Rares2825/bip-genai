"""
====================================================================
⚙️ BACKEND INSTRUCTIONS: DATA INGESTION (vector_db)
====================================================================
The goal of this script is to take the PDF documents from the `data/` folder,
split them into smaller chunks, convert them into embeddings, 
and save them into a local ChromaDB vector database.

The Backend team needs to complete the code below.
"""

import os
# TODO 1: Import PyPDFDirectoryLoader from langchain_community.document_loaders
# TODO 2: Import RecursiveCharacterTextSplitter from langchain.text_splitter
# TODO 3: Import HuggingFaceEmbeddings from langchain_community.embeddings
# TODO 4: Import Chroma from langchain_community.vectorstores

DATA_PATH = "../data/"     # This is where the DEW21 PDFs are stored
DB_PATH = "../vector_db/"  # This is where the database will be saved

def create_vector_db():
    print("1. Loading documents...")
    # TODO 5: Use PyPDFDirectoryLoader to read all PDFs from DATA_PATH.
    
    print("2. Splitting text (Chunking)...")
    # TODO 6: Set up RecursiveCharacterTextSplitter. 
    # Hint: For legal documents (AGBs), try chunk_size=1000 and chunk_overlap=200.
    # If it cuts sentences poorly, adjust these numbers!
    
    print("3. Generating Embeddings and Saving to ChromaDB...")
    # TODO 7: Initialize the "paraphrase-multilingual-MiniLM-L12-v2" model (great for Ger/Eng).
    # TODO 8: Save the document chunks into Chroma using persist_directory=DB_PATH.
    
    print("✅ Vector database successfully created!")

if __name__ == "__main__":
    # Run this script from the terminal: python src/ingest.py
    # create_vector_db() # Uncomment this after writing the code
    pass