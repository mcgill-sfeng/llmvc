import os
import json
import shutil
import uuid
from concurrent.futures import ProcessPoolExecutor
from itertools import product

from tqdm import tqdm

from graph.controller.graph_executor import ControllerGraphExecutor
from graph.controller.state import Config
from helpers.postprocess import path_to_package, replace_model_layer_import, replace_controller_file_import


ASSET_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "assets"))
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/data")
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def _sanitize_model_name(model_name: str) -> str:
    return model_name.lower().replace("-", "_").replace(".", "_").replace(" ", "_").replace("/", "_").replace("\\", "_")


def run_config(run_id: int, config: Config):
    result = ControllerGraphExecutor().execute(config=config, debug=False)

    output_file = os.path.join(OUTPUT_PATH,
                               f"{_sanitize_model_name(config["model_name"])}\\{config["data"]}\\{f"_{run_id}"}\\{"controller" if config["feature_name"] is None else config["feature_name"]}.py")

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result)


def run_config_with_random_id(config: Config) -> tuple[int, Config]:
    run_id = uuid.uuid4().int
    run_config(run_id, config)
    print("Done with run ID:", run_id, "for config:", config)
    return run_id, config


def run_postprocess(runs: list[tuple[int, Config]]):
    run_history_file = os.path.join(OUTPUT_PATH, f"history.json")

    if not os.path.exists(run_history_file):
        with open(run_history_file, "w") as f:
            json.dump({}, f, indent=4)

    with open(run_history_file, "r") as f:
        run_history = json.load(f)

    for run_id, config in runs:
        run_history[run_id] = [config]

        run_output_path = os.path.join(OUTPUT_PATH,
                                       f"{_sanitize_model_name(config['model_name'])}\\{config['data']}\\{f'_{run_id}'}")
        run_output_file = os.path.join(run_output_path,
                                       f"{'controller' if config['feature_name'] is None else config['feature_name']}.py")

        if not os.path.exists(run_output_file):
            raise FileNotFoundError(run_output_file)

        run_output_package = path_to_package(run_output_path, "output")
        model_layer_path = os.path.join(ASSET_PATH, config["data"])
        model_layer_package = path_to_package(os.path.join(model_layer_path, "model", str(config["model_layer_type"])),
                                              "assets")
        test_file_path = os.path.join(model_layer_path, "test", str(config["model_layer_type"]), "test.py")
        output_test_file_path = os.path.join(run_output_path, "test.py")

        with open(run_output_file, "r", encoding="utf-8") as f:
            run_output_content = f.read()

        replaced_output_content = replace_model_layer_import(run_output_content, model_layer_package)

        with open(run_output_file, "w", encoding="utf-8") as f:
            f.write(replaced_output_content)

        shutil.copyfile(test_file_path, output_test_file_path)

        with open(output_test_file_path, "r", encoding="utf-8") as f:
            test_content = f.read()

        replaced_test_content = replace_controller_file_import(test_content, run_output_package)

        with open(output_test_file_path, "w", encoding="utf-8") as f:
            f.write(replaced_test_content)

    with open(run_history_file, "w") as f:
        json.dump(run_history, f, indent=4)


if __name__ == "__main__":
    model_names = [
        "gpt-4o-mini",
        "gpt-4o",
        "gpt-4.1-nano",
        "gpt-4.1",
        "deepseek-chat"
    ]

    model_layer_types = [
        "umple",
        "ecore"
    ]
    partial_configs_nl = [
        {
            "with_description": False,
            "with_feature": False,
        },
        {
            "with_description": True,
            "with_feature": False,
        },
        {
            "with_description": False,
            "with_feature": True,
        },
        {
            "with_description": True,
            "with_feature": True,
        }
    ]

    partial_configs_st = [
        {
            "with_domain_model": False,
            "with_model_layer": False,
            "with_full_model_layer": False,
        },
        {
            "with_domain_model": True,
            "with_model_layer": False,
            "with_full_model_layer": False,
        },
        {
            "with_domain_model": False,
            "with_model_layer": True,
            "with_full_model_layer": False,
        },
        {
            "with_domain_model": True,
            "with_model_layer": True,
            "with_full_model_layer": False,
        },
        {
            "with_domain_model": False,
            "with_model_layer": True,
            "with_full_model_layer": True,
        }
    ]

    p = product(model_names, model_layer_types, partial_configs_nl, partial_configs_st)

    configs = [Config(
        model_name=model_name,
        data="BTMS",
        with_description=partial_config_nl["with_description"],
        with_feature=partial_config_nl["with_feature"],
        feature_name=None,
        with_domain_model=partial_config_st["with_domain_model"],
        with_model_layer=partial_config_st["with_model_layer"],
        model_layer_type=model_layer_type,
        with_full_model_layer=partial_config_st["with_full_model_layer"]
    ) for model_name, model_layer_type, partial_config_nl, partial_config_st in p]

    with ProcessPoolExecutor() as executor:
        runs = list(tqdm(executor.map(run_config_with_random_id, configs), total=len(configs)))

    print("Running post-processing...")
    run_postprocess(runs)
