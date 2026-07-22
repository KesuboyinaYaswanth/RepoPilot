import streamlit as st

from modules.clone_repo import clone_repo
from modules.utils import get_repo_info
from modules.loader import load_repository
from modules.chunker import create_chunks
from modules.embeddings import get_embedding_model
from modules.vectordb import *
from modules.retreiver import retrieve_chunks
from modules.llm import *


st.set_page_config(page_title="RepoPilot", page_icon="🤖")

st.title("🤖 RepoPilot")
st.write("Ask questions about any GitHub repository.")

# ------------------------
# Session State
# ------------------------

if "repo_loaded" not in st.session_state:
    st.session_state.repo_loaded = False

# ------------------------
# Repository Section
# ------------------------

repo_url = st.text_input("Repository URL")

if st.button("Load Repository"):

    if not repo_url:
        st.warning("Please enter a repository URL.")
        st.stop()

    try:

        with st.spinner("Cloning repository..."):
            repo_path = clone_repo(repo_url)

        with st.spinner("Loading files..."):
            repo_info = get_repo_info(repo_path)
            files, stats = load_repository(repo_path)

        with st.spinner("Creating chunks..."):
            chunks = create_chunks(files)

        with st.spinner("Creating vector database..."):
            embedding_model = get_embedding_model()
            create_vector_db(chunks, embedding_model)

        st.session_state.repo_loaded = True

        st.success("Repository loaded successfully!")

        st.subheader("Repository Information")
        st.json(repo_info)

        st.subheader("Repository Statistics")
        st.write(f"Files Indexed: {stats['files_indexed']}")
        st.write(f"Folders Scanned: {stats['folders_scanned']}")
        st.write(f"Skipped Files: {stats['skipped_files']}")

        st.subheader("Languages")
        st.json(stats["languages"])

    except Exception as e:
        st.error(str(e))


# ------------------------
# Question Answering
# ------------------------

if st.session_state.repo_loaded:

    st.divider()

    st.header("Ask a Question")

    question = st.text_input("Enter your question")

    if st.button("Ask"):

        if not question:
            st.warning("Please enter a question.")
            st.stop()

        with st.spinner("Searching repository..."):
            chunks = retrieve_chunks(question)

        with st.spinner("Generating answer..."):
            answer = generate_answer(chunks, question)

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Relevant Files")

        files = []

        for chunk in chunks:
            path = chunk["metadata"].get("file_path")

            if path not in files:
                files.append(path)

        for file in files:
            st.write(f"📄 {file}")

        with st.expander("Retrieved Context"):

            for chunk in chunks:

                st.markdown(
                    f"### {chunk['metadata'].get('file_path', 'Unknown')}"
                )

                st.code(chunk["content"][:500])

else:
    st.info("Load a repository to start asking questions.")