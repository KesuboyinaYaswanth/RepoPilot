import os

from langchain_community.vectorstores import FAISS


VECTOR_DB_PATH = "vector_store"


def create_vector_db(chunks, embedding_model):
    """
    Create a FAISS vector database from document chunks.
    """

    db = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_model
    )

    return db


def save_vector_db(db):
    """
    Save the FAISS index locally.
    """

    os.makedirs(VECTOR_DB_PATH, exist_ok=True)

    db.save_local(VECTOR_DB_PATH)


def load_vector_db(embedding_model):
    """
    Load an existing FAISS index.
    """

    db = FAISS.load_local(
        VECTOR_DB_PATH,
        embedding_model,
        allow_dangerous_deserialization=True
    )

    return db