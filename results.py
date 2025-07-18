import importlib.util
import inspect
import json
import os

import pandas as pd

from helpers.show_results import header_from_config, show_stats, show_table

OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
HISTORY_FILE_PATH = os.path.join(OUTPUT_PATH, "history.json")
RESULTS_FILE_PATH = os.path.join(OUTPUT_PATH, "results.csv")


def execute_all_tests(file_path: str) -> tuple[list[int], int]:
    module_name = os.path.splitext(os.path.basename(file_path))[0]

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    functions = list(filter(lambda f: f[1].__module__ == module_name, inspect.getmembers(module, inspect.isfunction)))

    pass_count_arr = [0] * len(functions)

    for i, function in enumerate(functions):
        name, func = function
        try:
            pass_test = func()

            if pass_test:
                pass_count_arr[i] = 1
        except Exception as e:
            print(f"Error running test '{name}': {e}")
            pass

    print(f"Done running tests in {file_path}.", '\n', "Total tests passed:", len(pass_count_arr), "out of", len(functions))
    return pass_count_arr, len(functions)


def run_all_tests():
    with open(HISTORY_FILE_PATH, "r") as f:
        history = json.load(f)

    spreadsheet = []
    results = []

    for model_dir in os.listdir(OUTPUT_PATH):
        model_path = os.path.join(OUTPUT_PATH, model_dir)
        if os.path.isdir(model_path):
            for data_dir in os.listdir(model_path):
                data_path = os.path.join(model_path, data_dir)
                if os.path.isdir(data_path):
                    for run_dir in os.listdir(data_path):
                        run_path = os.path.join(data_path, run_dir, "test.py")
                        run_id = int(run_dir[1:])
                        run_config = history.get(str(run_id), {})[0]

                        if not run_config:
                            print(f"Run ID {run_id} not found in history. Skipping...")
                            continue

                        run_result = execute_all_tests(run_path)

                        run_header = header_from_config(run_config)

                        results.append((
                            run_id,
                            run_header,
                            run_config,
                            run_result[0],
                            run_result[1],
                        ))

                        spreadsheet.append((
                            run_id,
                            run_header,
                            run_config["model_name"],
                            run_config["model_layer_type"],
                            run_result[0].count(1),
                            run_result[1],
                        ))

    df = pd.DataFrame(spreadsheet, columns=[
        "run_id", "run_config", "llm", "modeling_tool", "test_pass", "test_total"
    ])

    df.to_csv(RESULTS_FILE_PATH, index=False)

    print("All tests executed. Results saved to results.csv.")

    show_stats(results)

    show_table(RESULTS_FILE_PATH)

if __name__ == "__main__":
    run_all_tests()