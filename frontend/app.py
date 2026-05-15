import sys
sys.path.append(".")

import streamlit as st
from src.retrieval.vector_store import load_vector_store, search
from src.generation.llm import generate_answer

st.set_page_config(
    page_title="Building Energy Code Assistant",
    page_icon="🏢",
    layout="wide",
)

st.title("🏢 Building Energy Code Assistant")
st.markdown("Ask questions about German building energy regulations (GEG), EU directives (EPBD), and KfW subsidies.")

# Load vector store once
@st.cache_resource
def init():
    return load_vector_store()

collection = init()
st.sidebar.success(f"✅ {collection.count()} chunks loaded from 9 PDFs")

# Sidebar settings
st.sidebar.markdown("---")
st.sidebar.subheader("Settings")
n_results = st.sidebar.slider("Number of sources to search", 3, 10, 5)
language = st.sidebar.radio("Answer language", ["Auto (match question)", "English", "Deutsch"])

# Example questions
st.sidebar.markdown("---")
st.sidebar.subheader("Try these questions")
example_questions = [
    "When must new buildings be zero-emission?",
    "What are the U-value requirements for walls?",
    "Welche Förderung gibt es für Wärmepumpen?",
    "What is an Effizienzhaus 40?",
    "Was sind die Anforderungen an den Mindestwärmeschutz?",
]
for q in example_questions:
    if st.sidebar.button(q, key=q):
        st.session_state["query"] = q

# Main input
query = st.text_input(
    "Your question:",
    value=st.session_state.get("query", ""),
    placeholder="e.g. What insulation requirements exist for roof renovation?"
)

if query:
    with st.spinner("🔍 Searching documents and generating answer..."):
        # Search
        results = search(collection, query, n_results=n_results)

        # Generate answer
        answer = generate_answer(query, results)

    # Display answer
    st.markdown("### Answer")
    st.markdown(answer)

    # Display sources
    st.markdown("---")
    st.markdown("### 📄 Sources Used")

    for i, (doc, meta, distance) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    )):
        relevance = max(0, round((1 - distance / 2) * 100))
        with st.expander(
            f"Source {i+1}: {meta['source_file']} — Page {meta['page']} (relevance: {relevance}%)"
        ):
            st.markdown(f"**File:** `{meta['source_file']}`")
            st.markdown(f"**Page:** {meta['page']}")
            st.text(doc[:500])