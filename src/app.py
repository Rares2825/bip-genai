"""
====================================================================
🎨 FRONTEND INSTRUCTIONS: STREAMLIT INTERFACE
====================================================================
Here we build "The simple front-end" requested in the project brief.
The Frontend team works exclusively here. DO NOT write AI logic here,
just import and call the functions from `llm_engine.py`.
"""

import streamlit as st
# TODO 1: Import the functions from llm_engine.py:
# from llm_engine import initialize_rag_system, generate_answer

# TODO 2: Configure the Streamlit page (title, icon using st.set_page_config)
# Add a DEW21 logo or a nice, professional title.

# --- SYSTEM INITIALIZATION ---
# Use the @st.cache_resource decorator above the initialization function
# so the LLM doesn't reload from scratch every time the user clicks a button!

# TODO 3: Call `initialize_rag_system()` and save the result in a variable.

# --- CHAT INTERFACE ---
st.title("⚖️ DEW21 AGB & Regulatory Assistant")
st.write("This prototype answers questions based on internal DEW21 documents.")

# TODO 4: Create a text input bar (st.text_input) for the user's question.
# TODO 5: Create a "Search Answer" button (st.button).

# When the button is clicked:
# TODO 6: Show a loading spinner (st.spinner("Searching through documents...")).
# TODO 7: Call the `generate_answer()` function from llm_engine.py.
# TODO 8: Display the generated answer using st.write() or st.markdown().
# TODO 9: Create an expander (`st.expander("View Sources")`) and display exactly where 
#         the answer came from (so QA can verify and employees can trust the AI).