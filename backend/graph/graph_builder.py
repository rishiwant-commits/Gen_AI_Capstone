from langgraph.graph import StateGraph, END

from backend.core.state import FarmState
from backend.graph.nodes import get_nodes
from backend.graph.edges import risk_router


def build_graph(model, scaler, columns):
    graph = StateGraph(FarmState)

    nodes = get_nodes(model, scaler, columns)

    graph.add_node("preprocess", nodes["preprocess"])
    graph.add_node("predict", nodes["predict"])
    graph.add_node("issue", nodes["issue"])
    graph.add_node("risk", nodes["risk"])
    graph.add_node("recommend", nodes["recommend"])
    graph.add_node("explain", nodes["explain"])
    graph.add_node("rag", nodes["rag"])
    graph.add_node("advisory", nodes["advisory"])

    graph.set_entry_point("preprocess")

    graph.add_edge("preprocess", "predict")
    graph.add_edge("predict", "issue")
    graph.add_edge("issue", "risk")
    graph.add_edge("risk", "recommend")
    graph.add_edge("recommend", "explain")

    graph.add_conditional_edges(
        "explain",
        risk_router,
        {
            "skip_advisory": END,
            "do_advisory": "rag"
        }
    )

    graph.add_edge("rag", "advisory")
    graph.add_edge("advisory", END)

    return graph.compile()
