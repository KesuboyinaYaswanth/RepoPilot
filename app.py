import streamlit as st
from modules.clone_repo import *
from modules.utils import *

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
        except Exception as e:
            st.error(f"Error cloning repository: {e}")
    else:
        st.warning("Please enter a valid repository URL.")

