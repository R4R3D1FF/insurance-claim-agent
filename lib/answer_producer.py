from langgraph.graph import MessagesState
from langchain.chat_models import init_chat_model

from langchain_core.messages import AIMessage, SystemMessage
from pydantic import BaseModel, Field

from lib.tools.retrieval import retriever_tool

response_model = init_chat_model(
    model="gemini-3.1-flash-lite", 
    model_provider="google_genai",
    temperature=0
)

class ScoreAndCitation(BaseModel):
    """Grade documents using a binary score for relevance check."""

    compliance_score: str = Field(
        description="Relevance score: 'yes' if claim is compliant with policy, or 'no' if not compliant."
    )

    citation: str = Field(
        description="The chunk of the rule policy used to determine that the claim is not compliant. If claim is compliant with rule policy, this should be left blank."
    )
    


def produce_final_answer(state: MessagesState):
    """Simply generate a response based on the results of the tool call
    """
    print("Second LLM node entered")
    response = response_model.with_structured_output(ScoreAndCitation).invoke(
        [
            SystemMessage(content="Based on the embeddings found in the above tool call, check if any of them is violated by the information found in the chunk in the original user message. Also cite evidence."),
            *state["messages"]
        ]
    )
    # return {"messages": [response]}

    return {
        "analysis": response
    }

    if response.compliance_score == "yes":
        return { "messages": [ AIMessage( content=f"""Compliance: {response.compliance_score} Citation: {response.citation} """ ) ] }
    
    elif response.compliance_score == "no":
        return { "messages":  [ AIMessage( content=f"""Compliance: {response.compliance_score} """ ) ]}
