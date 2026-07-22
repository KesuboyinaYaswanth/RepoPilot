# modules/retriever.py

from modules.embeddings import get_embedding_model
from modules.vectordb import *


def retrieve_chunks(query, k=5):
    """
    Retrieve top-k relevant chunks from FAISS
    """
    # Load embedding model
    embedding_model = get_embedding_model()

    # Load vector database
    vectordb = load_vector_db(embedding_model)

    # Create retriever
    retriever = vectordb.as_retriever(search_kwargs={"k": k})

    # Get relevant documents
    docs = retriever.invoke(query)

    results = []
    for doc in docs:
        results.append({
            "content": doc.page_content,
            "metadata": doc.metadata
        })

    return results