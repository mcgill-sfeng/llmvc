from copy import deepcopy

from graph.controller.state import State, Config
from graph.controller.nodes import setup_node, llm_node, parser_node, runner_node
from graph.graph import get_graph


class ControllerGraphExecutor:
    initial_state = State(
        config=None,
        attempts=0,
        messages=[],
        error="",
        result=""
    )

    def __init__(self):
        self.graph = get_graph(
            setup_node=setup_node,
            llm_node=llm_node,
            parser_node=parser_node,
            runner_node=runner_node,
            state=State
        )

    def execute(self, config: Config, debug: bool | None = None):
        state = deepcopy(ControllerGraphExecutor.initial_state)
        state["config"] = config

        return self.graph.invoke(state, debug=debug)["result"]