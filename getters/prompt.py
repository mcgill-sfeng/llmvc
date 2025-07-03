import os
import json
from copy import copy
from typing import Literal

from getters import (
    PromptParams,
    CONTROLLER_PROMPT_FOLDER,
    MODEL_PROMPT_FOLDER,
    get_feature_requirement,
    get_controller_signature,
    get_controller_feature_signature,
    get_description,
    get_model_layer,
    get_model_layer_signature,
    get_domain_model,
)

CONTROLLER_PROMPT_DEFAULT_PARAMS = {
    PromptParams.CONTROLLER_SIGNATURE.value,
}

MODEL_PROMPT_DEFAULT_PARAMS = {
    PromptParams.DESCRIPTION.value,
}


def _get_prompt_template(folder_path: str, params: set[str]) -> str:
    map_file_path = os.path.join(CONTROLLER_PROMPT_FOLDER, "map.json")

    if not os.path.exists(map_file_path):
        raise ValueError(f"Missing map file at {map_file_path}")

    with open(map_file_path, "r") as file:
        map_data = json.load(file)

    prompt_files = [
        file_name for file_name, file_params in map_data.items()
        if set(file_params) == params and len(file_params) == len(params)
    ]
    if len(prompt_files) != 1:
        raise ValueError(f"Expected one prompt file matching the selected params {params}, but found {len(prompt_files)}")

    prompt_file = prompt_files[0]
    prompt_path = os.path.join(folder_path, f"{prompt_file}.txt")

    if not os.path.exists(prompt_path):
        raise ValueError(f"Missing prompt file at {prompt_path}")

    with open(prompt_path, "r") as file:
        prompt_template = file.read()

    return prompt_template


def _get_controller_prompt_template(
    with_description: bool,
    with_feature: bool,
    with_feature_name: bool,
    with_domain_model: bool,
    with_model_layer: bool,
    model_layer_type: Literal["umple", "ecore"],
    with_full_model_layer: bool,
) -> str:
    params = copy(CONTROLLER_PROMPT_DEFAULT_PARAMS)

    if with_description:
        params.add(PromptParams.DESCRIPTION.value)

    if with_feature:
        if with_feature_name:
            params.add(PromptParams.FEATURE_NAME.value)
            params.add(PromptParams.FEATURE_REQUIREMENT.value)
        else:
            params.add(PromptParams.ALL_FEATURE_REQUIREMENTS.value)

    if with_domain_model:
        params.add(PromptParams.DOMAIN_MODEL.value)

    if with_model_layer:
        if with_full_model_layer:
            params.add(PromptParams.FULL_MODEL_LAYER.value)
        else:
            params.add(PromptParams.MODEL_LAYER_SIGNATURE.value)

    if model_layer_type == "umple":
        params.add(PromptParams.UMPLE_MODEL_LAYER.value)
    elif model_layer_type == "ecore":
        params.add(PromptParams.ECORE_MODEL_LAYER.value)
    else:
        raise ValueError(f"Unknown model layer type: {model_layer_type}.")

    return _get_prompt_template(CONTROLLER_PROMPT_FOLDER, params)


def _get_model_prompt_template(
    with_domain_model: bool,
    with_controller_signature: bool,
    with_feature: bool,
    with_all_features: bool,
) -> str:
    if not with_feature:
        assert not with_all_features, "with_all_features can only be used with with_feature=True"

    params = copy(MODEL_PROMPT_DEFAULT_PARAMS)

    if with_domain_model:
        params.add(PromptParams.DOMAIN_MODEL.value)

    if with_controller_signature:
        params.add(PromptParams.CONTROLLER_SIGNATURE.value)

    if with_feature:
        params.add(PromptParams.FEATURE_NAME.value)

        if with_all_features:
            params.add(PromptParams.ALL_FEATURE_REQUIREMENTS.value)
        else:
            params.add(PromptParams.FEATURE_REQUIREMENT.value)

    return _get_prompt_template(MODEL_PROMPT_FOLDER, params)


def get_controller_prompt(
        data: str,
        with_description: bool = False,
        with_feature: bool = False,
        feature_name: str = None,
        with_domain_model: bool = False,
        with_model_layer: bool = False,
        model_layer_type: Literal["umple", "ecore"] = None,
        with_full_model_layer: bool = False,
        model_layer_classnames: list[str] = None,
) -> str:
    """
    Gets the formatted prompt to generate controller implementations.

    :param data: The name of the dataset, e.g. "BTMS".
    :param feature_name: The name of the feature to be implemented, e.g. "create_driver". Must correspond to one of the feature files within the dataset. Leave empty or None for passing all features together.
    :param with_domain_model: Whether to include the domain model in the prompt.
    :param with_model_layer: Whether to include a model layer description in the prompt.
    :param model_layer_type: When with_model_layer=True, use model_layer_type to specify the type of model layer to be included in the prompt.
    :param with_full_model_layer: When with_model_layer=True, use full_model_layer=True to include the full implementation details of the model layer, and use full_model_layer=False to include only the model layer signature.
    :param model_layer_classnames: When with_model_layer=True, use model_layer_classnames to specify the class names of the model layer to be included in the prompt. If None, all classes in the model layer will be included.
    :return: The formatted prompt.
    """
    if not with_feature:
        assert not feature_name, "feature_name can only be used with with_feature=True"

    if not with_model_layer:
        assert not with_full_model_layer, "with_full_model_layer can only be used with with_model_layer=True"
        assert not model_layer_classnames, "model_layer_classnames can only be used with with_model_layer=True"

    assert model_layer_type is not None, "model_layer_type must be specified"

    controller_signature = get_controller_signature(data)
    controller_feature_signature = get_controller_feature_signature(data, feature_name)

    if with_description:
        description = get_description(data)
    else:
        description = None

    if with_feature:
        feature_requirement = get_feature_requirement(data, feature_name)
    else:
        feature_requirement = None

    # domain_model
    if with_domain_model:
        domain_model = get_domain_model(data, model_layer_type)
    else:
        domain_model = None

    # model_layer
    if with_model_layer:
        if with_full_model_layer:
            model_layer = get_model_layer(data, model_layer_type, model_layer_classnames)
        else:
            model_layer = get_model_layer_signature(data, model_layer_type, model_layer_classnames)
    else:
        model_layer = None


    prompt_template = _get_controller_prompt_template(
        with_description=with_description,
        with_feature=with_feature,
        with_feature_name=feature_name is not None,
        with_domain_model=with_domain_model,
        with_model_layer=with_model_layer,
        model_layer_type=model_layer_type,
        with_full_model_layer=with_full_model_layer,
    )

    return prompt_template.format(
        description=description,
        feature_name=feature_name,
        feature_requirement=feature_requirement,
        controller_signature=controller_signature,
        controller_feature_signature=controller_feature_signature,
        domain_model=domain_model,
        model_layer=model_layer,
    )