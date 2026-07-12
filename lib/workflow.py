from typing import Literal, Optional

from langgraph.graph import START, END, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

from lib.answer_producer import ScoreAndCitation, produce_final_answer
from lib.query_responder import respond_or_call_policy_retriever
from lib.tools.retrieval import retriever_tool

class InsuranceState(MessagesState):
    analysis: Optional[ScoreAndCitation]

workflow = StateGraph(InsuranceState)

workflow.add_node(respond_or_call_policy_retriever)
workflow.add_node("retrieve", ToolNode([retriever_tool]))
workflow.add_node(produce_final_answer)

workflow.add_edge(START, "respond_or_call_policy_retriever")

def retrieve_or_end_decider(state: MessagesState) -> Literal["retrieve", "__end__"]:
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "retrieve"
    return END

workflow.add_edge("respond_or_call_policy_retriever", "retrieve")
workflow.add_edge("retrieve", "produce_final_answer")
# workflow.add_conditional_edge("generate_query_or_respond", END)
workflow.add_edge("produce_final_answer", END)

graph = workflow.compile()

def show_graph():
    png = graph.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(png)

def run_agentic_rag(chunk) -> None:
    state = graph.invoke(
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