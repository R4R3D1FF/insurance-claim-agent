from typing import Literal, Optional

from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

from app.lib.graph.nodes import ScoreAndCitation, produce_final_answer, make_respond_or_call_policy_retriever

class InsuranceState(MessagesState):
    analysis: Optional[ScoreAndCitation]

def create_graph(retriever_tool):
    workflow = StateGraph(InsuranceState)

    workflow.add_node(make_respond_or_call_policy_retriever(retriever_tool))
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

    return graph