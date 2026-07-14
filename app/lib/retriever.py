from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

class Retriever():
    def __init__(self, chunks):
        vectorstore = InMemoryVectorStore.from_documents(
            documents=chunks,
            embedding=GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
        )

        self.retriever = vectorstore.as_retriever()

#  I could make this without a framework by simply using a dict attribute 'vector_store' to map from the embedding to the original text.
#  In __init__, I could make the manual API call to OpenAI's embedding model.