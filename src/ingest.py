import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Atentie: Presupunem ca rulezi scriptul din radacina proiectului!
DATA_PATH = "data/"
DB_PATH = "vector_db/"

def create_vector_db():
    print("📂 1. Cautam documente PDF in folderul data/...")
    # Verificam daca folderul exista
    if not os.path.exists(DATA_PATH):
        print(f"❌ Eroare: Nu gasesc folderul {DATA_PATH}. Creeaza-l si pune PDF-uri in el.")
        return

    loader = PyPDFDirectoryLoader(DATA_PATH)
    documents = loader.load()
    
    if not documents:
        print("❌ Eroare: Folderul data/ este gol. Pune PDF-urile DEW21 acolo.")
        return

    print(f"✅ Am gasit si incarcat {len(documents)} pagini de PDF.")

    print("✂️ 2. Incepem taierea textului (Chunking)...")
    # Tăiem textul în bucăți de 1000 de caractere. 
    # Lăsăm un 'overlap' (suprapunere) de 200 de caractere ca să nu tăiem o lege la jumătate și să pierdem contextul.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""] # Incearca sa taie la sfarsit de paragraf/propozitie
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Am impartit documentele in {len(chunks)} bucati de text (chunks).")

    print("🧠 3. Descarcam modelul multilingv si cream baza de date ChromaDB...")
    # Acest model este perfect pentru Germana si Engleza. Se va descarca automat (are cam 400MB).
    embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")
    
    # Cream baza de date si o salvam pe disk
    db = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=DB_PATH
    )
    db.persist() # Salvam fortat fisierele
    print(f"🚀 GATA! Baza de date a fost salvata cu succes in folderul '{DB_PATH}'!")

if __name__ == "__main__":
    create_vector_db()