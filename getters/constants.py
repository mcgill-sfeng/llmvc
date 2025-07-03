import os
from enum import Enum


class PromptParams(Enum):
    DESCRIPTION = "description"
    CONTROLLER_SIGNATURE = "controller_signature"
    FEATURE_NAME = "feature_name"
    FEATURE_REQUIREMENT = "feature_requirement"
    ALL_FEATURE_REQUIREMENTS = "all_feature_requirements"
    DOMAIN_MODEL = "domain_model"
    UMPLE_MODEL_LAYER = "umple_model_layer"
    ECORE_MODEL_LAYER = "ecore_model_layer"
    FULL_MODEL_LAYER = "full_model_layer"
    MODEL_LAYER_SIGNATURE = "model_layer_signature"

ASSETS_FOLDER = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "assets"))


STATIC_FOLDER = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "static"))
DATA_FOLDER = os.path.join(STATIC_FOLDER, "data")
PROMPT_FOLDER = os.path.join(STATIC_FOLDER, "prompts")
CONTROLLER_PROMPT_FOLDER = os.path.join(PROMPT_FOLDER, "controller")
MODEL_PROMPT_FOLDER = os.path.join(PROMPT_FOLDER, "model")
TEST_PROMPT_FOLDER = os.path.join(PROMPT_FOLDER, "test")