import streamlit as st
from modules.clone_repo import *
from modules.utils import *
from modules.loader import *
from modules.constants import *
from modules.chunker import *
from modules.vectordb import *
from modules.embeddings import *

st.set_page_config(page_title="GitHub Repository Assistant")

st.title("📂 GitHub Repository Assistant")

repo_url = st.text_input("Repository URL")
if st.button("Clone Repository"):
    if repo_url:

        try:
            repo_path = clone_repo(repo_url)
            repo_info = get_repo_info(repo_path)
            st.success("Repository cloned successfully!")
            st.write("Repository Information:")
            st.json(repo_info)
            files, stats = load_repository(repo_path)
            chunks = create_chunks(files)
            st.write(f"Total Chunks Created: {len(chunks)}")
            vector_db = create_vector_db(chunks, get_embedding_model())

            st.success("Vector database created successfully!")

            st.success("Repository Loaded Successfully!")

            st.write("### Repository Statistics")

            st.write(f"Files Indexed: {stats['files_indexed']}")

            st.write(f"Folders Scanned: {stats['folders_scanned']}")

            st.write(f"Skipped Files: {stats['skipped_files']}")

            st.write("### Languages")

            st.json(stats["languages"])
        except Exception as e:
            st.error(f"Error cloning repository: {e}")
    else:
        st.warning("Please enter a valid repository URL.")


