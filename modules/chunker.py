from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def create_chunks(loaded_files):
    """
    Convert loaded files into LangChain Documents and split them into chunks.
    """

    documents = []

    # Convert dictionaries into Documents
    for file in loaded_files:

        document = Document(
            page_content=file["content"],
            metadata={
                "path": file["path"],
                "relative_path": file["relative_path"],
                "filename": file["filename"],
                "extension": file["extension"],
                "language": file["language"],
                "size": file["size"],
                "lines": file["lines"]
            }
        )

        documents.append(document)

    # Create text splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    # Split documents into chunks
    chunks = splitter.split_documents(documents)

    # Add unique chunk IDs
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i

    return chunks