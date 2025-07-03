from typing import TypedDict, Required, Optional, Literal

from langchain_core.messages import BaseMessage

class Config(TypedDict, total=False):
    model_name: Required[str]
    data: Required[str]
    with_description: Required[bool]
    with_feature: Required[bool]
    feature_name: Required[str]
    with_domain_model: Required[bool]
    with_model_layer: Required[bool]
    model_layer_type: Optional[Literal["umple", "ecore"]]
    with_full_model_layer: Required[bool]


class State(TypedDict, total=False):
    config: Required[Config]
    attempts: Required[int]
    messages: Required[list[BaseMessage]]
    error: str
    result: str
