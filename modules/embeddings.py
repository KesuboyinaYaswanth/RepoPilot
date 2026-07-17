from langchain_ollama import OllamaEmbeddings


def get_embedding_model():
    """
    Returns the Ollama embedding model.
    """

    embedding_model = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    return embedding_model