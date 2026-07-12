from dataclasses import dataclass

from pydantic import BaseModel, Field

from lib.document_loader import load_file_as_document
from lib.documents_chunker import get_chunks_from_documents
from lib.workflow import run_agentic_rag

from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model

@dataclass
class AdjunctatorResult:
    chunk: str
    citation: str

class Reflection(BaseModel):
    confidence: float = Field(
        description="Confidence between 0.0 and 1.0 that the compliance analysis is correct."
    )
    reasoning: str = Field(
        description="Brief explanation for the confidence score."
    )

def loop_over_claim_chunks():
    non_compliant_claims: list[AdjunctatorResult] = []

    documents = [load_file_as_document("test/insurance_claim.txt")]
    chunks = get_chunks_from_documents(documents)

    

    compliance = True
    for chunk in chunks:
        analysis = run_agentic_rag(chunk.page_content)
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

reflector_model = init_chat_model(
    model="gemini-3.1-flash-lite",
    model_provider="google_genai",
    temperature=0,
)


def reflect_and_give_final_answer():
    results = loop_over_claim_chunks()
    if len(results) == 0:
        print("The claim is compliant.")
        return
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

    print("\n========== FINAL RESULT ==========")
    print("Decision: NOT COMPLIANT")
    print(f"Confidence: {response.confidence:.2%}")
    print(f"Reasoning: {response.reasoning}")

    return response