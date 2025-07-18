import os
import ast

from getters import DATA_FOLDER


def get_controller_signature(data: str) -> str:
    controller_file_path = os.path.join(DATA_FOLDER, data, "controller.py")

    if not os.path.exists(controller_file_path):
        raise ValueError(f"Missing controller file at: {controller_file_path}")

    with open(controller_file_path, "r") as file:
        controller_signature = file.read()

    try:
        exec(controller_signature, globals(), {})
    except Exception as e:
        print(f"Warning: Error evaluating controller signature: {e}")

    return controller_signature.strip()


def get_controller_feature_signature(data: str, target_func_name: str = None) -> str:
    controller_file_path = os.path.join(DATA_FOLDER, data, "controller.py")

    if not os.path.exists(controller_file_path):
        raise ValueError(f"Missing controller file at: {controller_file_path}")

    with open(controller_file_path, 'r', encoding='utf-8') as file:
        source = file.read()

    tree = ast.parse(source)
    lines = source.splitlines()
    function_blocks = []

    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name.endswith("Controller"):
            for func in node.body:
                if isinstance(func, ast.FunctionDef):
                    if func.name == "__init__":  # constructor
                        continue

                    if target_func_name is not None and func.name != target_func_name:  # not the target function
                        continue

                    start = func.lineno - 1
                    indent = len(lines[start]) - len(lines[start].lstrip())
                    end = start + 1

                    while end < len(lines):
                        line = lines[end]
                        if line.strip() == "":
                            end += 1
                            continue
                        current_indent = len(line) - len(line.lstrip())
                        if current_indent <= indent:
                            break
                        end += 1

                    function_blocks.append("\n".join(lines[start:end]))

            break

    if not function_blocks:
        raise ValueError(f"Function '{target_func_name}' not found in controller file.")

    return "\n\n".join(function_blocks)
