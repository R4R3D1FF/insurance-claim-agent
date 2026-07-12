from pathlib import Path

from lib.claim_loop import reflect_and_give_final_answer
from lib.document_loader import load_file_as_document
from lib.documents_chunker import get_chunks_from_documents
from lib.workflow import run_agentic_rag, show_graph
# from langchain.chat_models import init_chat_model


def main():
    # response_model = init_chat_model(
    #     model="gemini-3-flash-preview", 
    #     model_provider="google_genai",
    #     temperature=0
    # )
    # for chunk in response_model.stream(
    #     "Say hello."
    # ):
    #     print(repr(chunk))
    show_graph()

    # claimText = Path("test/insurance_claim.txt").read_text()
    reflect_and_give_final_answer()

    


if __name__ == "__main__":
    main()
