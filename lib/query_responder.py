from langgraph.graph import MessagesState
from langchain.chat_models import init_chat_model

from lib.tools.retrieval import retriever_tool

from langchain_core.messages import SystemMessage

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

    Use the retriever tool only when information from the rule policy is required.
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