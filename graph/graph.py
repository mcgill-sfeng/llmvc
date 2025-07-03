from langgraph.graph import StateGraph, START, END
from functools import partial


def resolve_parser(max_attempt: int, state) -> str:
    if "error" in state and state["error"] and state["error"] != "":
        return "FAIL" if "attempts" in state and state["attempts"] and state[
            "attempts"] < max_attempt else "MAX_ATTEMPTS_REACHED"
    else:
        return "SUCCESS"


def get_graph(setup_node, llm_node, parser_node, runner_node, state, max_attempts=1):
    graph_builder = StateGraph(state)
    graph_builder.add_node("setup", setup_node)
    graph_builder.add_node("llm", llm_node)
    graph_builder.add_node("parser", parser_node)
    graph_builder.add_node("runner", runner_node)

    graph_builder.add_edge(START, "setup")
    graph_builder.add_edge("setup", "llm")
    graph_builder.add_edge("llm", "parser")

    partial_resolve_parser = partial(resolve_parser, max_attempts)

    graph_builder.add_conditional_edges("parser", partial_resolve_parser, {
        "FAIL": "llm",
        "SUCCESS": "runner",
        "MAX_ATTEMPTS_REACHED": END
    })
    graph_builder.add_edge("runner", END)

    return graph_builder.compile()
