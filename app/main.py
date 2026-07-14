# from pathlib import Path

# from app.lib.claim_loop import reflect_and_give_final_answer
# from app.lib.document_loader import load_file_as_document
# from app.lib.documents_chunker import get_chunks_from_documents
# from app.lib.workflow import run_agentic_rag, show_graph
# # from langchain.chat_models import init_chat_model


# def main():
#     # show_graph()

#     # reflect_and_give_final_answer()

    


# if __name__ == "__main__":
#     main()

from fastapi import FastAPI
from app.routers.agent import agent_router

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello"}

app.include_router(agent_router)