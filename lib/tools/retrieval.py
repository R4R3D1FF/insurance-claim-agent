from functools import lru_cache

from langchain.tools import tool

from lib.document_loader import load_file_as_document
from lib.documents_chunker import get_chunks_from_documents
from lib.retriever import Retriever

@lru_cache(maxsize=1)
def get_retriever():
    documents = [load_file_as_document("./test/rule_policy.txt")]
    chunks = get_chunks_from_documents(documents)

    return Retriever(chunks)

@tool
def retriever_tool(query: str) -> str:
    """Search and return information from the test file."""
    print("retriever_tool called")
    retriever = get_retriever()
    retrieved_docs = retriever.retriever.invoke(query)
    return "\n\n".join([doc.page_content for doc in retrieved_docs])

