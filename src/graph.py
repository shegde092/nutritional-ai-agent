from langgraph.graph import StateGraph, START, END
from src.state import AgentState
from src.agents import extraction_agent_node, formatting_agent_node


def get_nutrition_graph():
    """
    Builds and compiles the dual-agent LangGraph workflow.
    
    Workflow Sequence:
    START -> Extraction Agent Node -> Formatting Agent Node -> END
    
    Returns:
        Compiled LangGraph StateGraph instance.
    """
    workflow = StateGraph(AgentState)

    # Register graph nodes
    workflow.add_node("extraction", extraction_agent_node)
    workflow.add_node("formatting", formatting_agent_node)

    # Establish execution control flow
    workflow.add_edge(START, "extraction")
    workflow.add_edge("extraction", "formatting")
    workflow.add_edge("formatting", END)

    return workflow.compile()
