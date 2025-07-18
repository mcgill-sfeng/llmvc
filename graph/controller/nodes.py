import re

from langchain_core.messages import ChatMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek

from getters import get_controller_prompt
from graph.controller.state import State

PYTHON_CODE_BLOCK_PATTERN = re.compile(r"```python\s+([\s\S]*?)\s+```", re.DOTALL)

def setup_node(state: State) -> State:
    config = state["config"]

    controller_prompt = get_controller_prompt(
        data=config["data"],
        with_description=config["with_description"],
        with_feature=config["with_feature"],
        feature_name=config["feature_name"],
        with_domain_model=config["with_domain_model"],
        with_model_layer=config["with_model_layer"],
        model_layer_type=config["model_layer_type"],
        with_full_model_layer=config["with_full_model_layer"],
    )

    state["messages"].append(SystemMessage(content=controller_prompt))

    return state


def llm_node(state: State) -> State:
    messages = state["messages"]
    model_name = state["config"]["model_name"]

    if len(messages) == 0:
        state["error"] = "No messages to process"
        return state

    if model_name.startswith("gpt"):
        llm = ChatOpenAI(model=model_name, temperature=0.01)
    elif model_name.startswith("deepseek"):
        llm = ChatDeepSeek(model=model_name, temperature=0.01, max_retries=3, timeout=60)
    else:
        raise ValueError(f"Unsupported model name: {model_name}")

    try:
        response = llm.invoke(messages)

        state["messages"].append(response)
        state["error"] = ""

    except Exception as e:
        state["error"] = str(e)

    state["attempts"] += 1
    return state


def parser_node(state: State) -> State:
    messages = state["messages"]

    if len(messages) == 0 or not isinstance(messages[-1], AIMessage):
        state["error"] = "No messages to process"
        return state

    match = PYTHON_CODE_BLOCK_PATTERN.search(messages[-1].content)

    if not match:
        state["result"] = messages[-1].content
        return state

    result = match.group(1).strip()

    state["error"] = ""
    state["result"] = result

    return state


def runner_node(state: State) -> State:

    if state["error"]:
        print("Warning:", state["error"])

    return state