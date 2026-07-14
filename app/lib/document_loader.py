from langchain_core.documents import Document

def load_file_as_document(path: str) -> Document:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
        return [Document(page_content=text, metadata={"source": path})]
# I guess without a framework I wouldn't need to convert this text to a Document object.
