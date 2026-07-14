from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# How would I do this without a framework? Ok, it's some algorithm

def get_chunks_from_documents(documents: list[Document]):
    docs_list = [item for sublist in documents for item in sublist]
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=50,
        chunk_overlap=10,
    )

    return text_splitter.split_documents(docs_list)