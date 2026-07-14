from dataclasses import dataclass

from pydantic import BaseModel, Field

from app.lib.document_loader import load_file_as_document
from app.lib.documents_chunker import get_chunks_from_documents
from app.lib.graph.tools import make_retriever_tool
from app.lib.graph.workflow import create_graph
from app.lib.retriever import Retriever
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

@dataclass
class AdjunctatorResult:
    chunk: str
    citation: str


class Reflection(BaseModel):
    compliant: bool = Field(
        description="Boolean indicating whether claim is compliant with rule policy."
    )
    confidence: float = Field(
        description="Confidence between 0.0 and 1.0 that the compliance analysis is correct."
    )
    reasoning: str = Field(
        description="Brief explanation for the confidence score."
    )

class PolicyChecker:
    def __init__(self, policy_file_path):
        self.policy_file_path = policy_file_path
        documents = [load_file_as_document(policy_file_path)]
        chunks = get_chunks_from_documents(documents)
        self.retriever = Retriever(chunks)
        retriever_tool = make_retriever_tool(self.retriever)
        self.graph = create_graph(retriever_tool)

    def run_agentic_rag(self, chunk) -> None:
        state = self.graph.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": chunk,
                    }
                ]
            },
            version="v3",
        )

        analysis = state["analysis"]

        return analysis
        
        # print("stream.messages", stream.messages)
        # for message in stream.messages:
        #     print("message.text", message.text)
        #     for token in message.text:
        #         print(token, end="", flush=True)
        

    def loop_over_claim_chunks(self, claim_file_path: str):
        non_compliant_claims: list[AdjunctatorResult] = []

        documents = [load_file_as_document(claim_file_path)]
        chunks = get_chunks_from_documents(documents)

        

        compliance = True
        for chunk in chunks:
            analysis = self.run_agentic_rag(chunk.page_content)
            if analysis.compliance_score == 'no':
                non_compliant_claims.append(
                    AdjunctatorResult(
                        chunk=chunk,
                        citation=analysis.citation
                    )
                )
                print("This claim is not compliant according to the following statements in policy.")
                print(analysis.citation)
                print("The part of the claim that violated the above part is as follows")
                print(chunk)
                compliance = False

        if compliance:
            print("This claim is compliant.")

        return non_compliant_claims

    def check_validity(self, claim_file_path: str):
        reflector_model = init_chat_model(
            model="gemini-3.1-flash-lite",
            model_provider="google_genai",
            temperature=0,
        )

        results = self.loop_over_claim_chunks(claim_file_path)
        if len(results) == 0:
            return Reflection(
                compliant=False
            )
            
        report = "\n\n".join(
            f"""
    Claim chunk:
    {r.chunk.page_content}

    Policy citation:
    {r.citation}
    """.strip()
            for r in results
        )

        response = reflector_model.with_structured_output(Reflection).invoke(
            [
                SystemMessage(
                    content="""
    You are an expert insurance claims auditor.

    You are reviewing the output of an insurance policy compliance agent.

    Do NOT determine compliance again.

    Instead, estimate how likely it is that the compliance agent's conclusion is correct.

    Consider:
    - Whether each cited policy clause clearly supports the conclusion.
    - Whether the claim evidence is sufficient.
    - Whether there are ambiguities or missing information.
    - Whether any cited policy clauses appear unrelated.

    Return:
    - confidence: a number between 0.0 and 1.0
    - reasoning: a concise explanation
    """
                ),
                HumanMessage(content=report),
            ]
        )

        return response

    