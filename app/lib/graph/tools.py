from typing import Callable
from langchain.tools import tool

from app.lib.document_loader import load_file_as_document
from app.lib.documents_chunker import get_chunks_from_documents
from app.lib.retriever import Retriever


def make_retriever_tool(retriever: Retriever) -> Callable[..., object]:
    @tool
    def retriever_tool(query: str) -> str:
        """Search and return information from the test file."""
        print("retriever_tool called")
        documents = [load_file_as_document("./test/rule_policy.txt")]
        chunks = get_chunks_from_documents(documents)
        retriever = Retriever(chunks)
        retrieved_docs = retriever.retriever.invoke(query)
        return "\n\n".join([doc.page_content for doc in retrieved_docs])
    
    return retriever_tool