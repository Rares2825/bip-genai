import streamlit as st
import os

# Imports for connecting to the "brain" (Backend)
from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="DEW21 Legal Assistant",
    page_icon="⚖️",
    layout="centered"
)

# --- 2. LOAD AI ENGINE (Cached) ---
# @st.cache_resource is CRITICAL. It ensures the model loads only once.
# Without it, the heavy AI model would reload from scratch on every user interaction.
@st.cache_resource
def load_rag_system():
    db_path = "vector_db/"
    
    # Check if the backend team has finished creating the database
    if not os.path.exists(db_path):
        return None
        
    # Load the same embedding settings used in ingest.py
    embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")
    db = Chroma(persist_directory=db_path, embedding_function=embeddings)
    
    # Set the retriever to fetch the top 3 most relevant paragraphs
    retriever = db.as_retriever(search_kwargs={"k": 3})
    
    # Connect to the local Ollama instance (Ensure Ollama is running in the background!)
    # temperature=0.0 prevents hallucinations (forces strict, factual answers)
    llm = Ollama(model="llama3", temperature=0.0) 
    
    # Strict prompt for the AI to follow
    prompt_template = """
    You are an official assistant for DEW21 employees. Your role is to answer questions using ONLY the provided context from the Terms, Conditions, and Regulations.
    If the answer is not contained in the context below, state clearly: "I could not find this information in the official documents."
    Do not invent information. Answer professionally in the language you were asked (English or German).
    
    Official Context: 
    {context}
    
    Question: {question}
    
    Answer:"""
    
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    
    # Assemble the Retrieval-Augmented Generation (RAG) chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    return qa_chain

# --- 3. GRAPHICAL INTERFACE (UI) ---
st.title("⚖️ DEW21 AGB Assistant")
st.markdown("Virtual assistant powered by **GenAI** for rapid querying of internal documents and regulations.")

# Attempt to start the system
qa_system = load_rag_system()

# Graceful degradation if the DB is missing
if qa_system is None:
    st.warning("⏳ The database is not ready yet. Waiting for the Backend team to run `ingest.py` and create the `vector_db/` folder.")
    st.stop() # Stops rendering the rest of the page to prevent errors

# --- 4. CHAT SYSTEM (History) ---
# Initialize the chat memory in Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous messages on the screen
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # If the message is from the AI and has sources, display them
        if "sources" in msg:
            with st.expander("📄 View source documents"):
                for i, doc in enumerate(msg["sources"]):
                    # Extract the filename and page number from metadata
                    source_name = doc.metadata.get('source', 'Unknown Document')
                    page_num = doc.metadata.get('page', 'N/A')
                    st.info(f"**Source {i+1}:** `{source_name}` (Page: {page_num}) \n\n {doc.page_content}")

# --- 5. TEXT INPUT BAR ---
# This is where the user types their question
user_query = st.chat_input("Ask a question about DEW21 regulations...")

if user_query:
    # 1. Display the user's question on the screen
    with st.chat_message("user"):
        st.markdown(user_query)
    
    # Save the question in the chat history
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # 2. The AI thinks and responds
    with st.chat_message("assistant"):
        with st.spinner("Searching through DEW21 legal documents..."):
            try:
                # Send the query to the AI brain
                response = qa_system.invoke({"query": user_query})
                answer = response["result"]
                sources = response["source_documents"]
                
                # Display the generated text
                st.markdown(answer)
                
                # Display the real sources inside an expander
                with st.expander("📄 View source documents"):
                    for i, doc in enumerate(sources):
                        source_name = doc.metadata.get('source', 'Unknown Document')
                        page_num = doc.metadata.get('page', 'N/A')
                        st.info(f"**Source {i+1}:** `{source_name}` (Page: {page_num}) \n\n {doc.page_content}")
                
                # Save the answer and sources to session memory
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer,
                    "sources": sources
                })
                
            except Exception as e:
                st.error(f"An error occurred while generating the response: {e}")