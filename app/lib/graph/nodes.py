from pydantic import BaseModel, Field
from langgraph.graph import MessagesState
from langchain.chat_models import init_chat_model


from langchain_core.messages import SystemMessage



class ScoreAndCitation(BaseModel):
    """Grade documents using a binary score for relevance check."""

    compliance_score: str = Field(
        description="Relevance score: 'yes' if claim is compliant with policy, or 'no' if not compliant."
    )

    citation: str = Field(
        description="The chunk of the rule policy used to determine that the claim is not compliant. If claim is compliant with rule policy, this should be left blank."
    )
    


def produce_final_answer(state: MessagesState):
    response_model = init_chat_model(
        model="gemini-3.1-flash-lite", 
        model_provider="google_genai",
        temperature=0
    )

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






def make_respond_or_call_policy_retriever(retriever_tool):
    response_model = init_chat_model(
        model="gemini-3.1-flash-lite", 
        model_provider="google_genai",
        temperature=0
    )

    def respond_or_call_policy_retriever(state: MessagesState):
        """Call the model to generate a response based on the current state. Given
        the question, it will decide to retrieve using the policy retriever tool, or simply respond to the user.
        """

        SYSTEM_PROMPT = """
        You are an insurance policy assistant.

        Use the retriever tool only wwhen information from the rule policy is required.
        If you already have enough information, answer directly.
        """

        print("LLM node 1 entered")
        response = response_model.bind_tools([retriever_tool]).invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                *state["messages"]
            ]
        )
        return {"messages": [response]}

    # I have no idea how I would have done this by myself. I know I need to provide an interface for making calls to the LLM, but I don't know how you provide it with the necessary tools. We'll do it in the other git branch.

    return respond_or_call_policy_retriever