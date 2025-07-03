import ast
import os
from typing import Literal

from getters import ASSETS_FOLDER, DATA_FOLDER


def _format_arguments(args: ast.arguments) -> str:
    parts = []

    for arg in args.posonlyargs:
        part = arg.arg
        if arg.annotation:
            part += f": {ast.unparse(arg.annotation)}"
        parts.append(part)

    if args.posonlyargs:
        parts.append("/")

    for arg in args.args:
        part = arg.arg
        if arg.annotation:
            part += f": {ast.unparse(arg.annotation)}"
        parts.append(part)

    if args.vararg:
        part = f"*{args.vararg.arg}"
        if args.vararg.annotation:
            part += f": {ast.unparse(args.vararg.annotation)}"
        parts.append(part)
    elif args.kwonlyargs:
        parts.append("*")

    for arg in args.kwonlyargs:
        part = arg.arg
        if arg.annotation:
            part += f": {ast.unparse(arg.annotation)}"
        parts.append(part)

    if args.kwarg:
        part = f"**{args.kwarg.arg}"
        if args.kwarg.annotation:
            part += f": {ast.unparse(args.kwarg.annotation)}"
        parts.append(part)

    return ", ".join(parts)


def get_model_layer_signature(
        data: str,
        model_layer_type: Literal["umple", "ecore"],
        filenames: list[str] | None,
) -> str:
    result = ""

    assets_model_folder_path = os.path.join(ASSETS_FOLDER, data, "model")

    if not os.path.exists(assets_model_folder_path):
        raise ValueError(f"Missing model folder at: {assets_model_folder_path}")

    model_inner_folder_path = os.path.join(assets_model_folder_path, model_layer_type)

    if not os.path.exists(model_inner_folder_path):
        raise ValueError(f"Missing model inner folder at: {model_inner_folder_path}")

    if filenames is None or len(filenames) == 0:
        filenames = []

        for file_name in os.listdir(model_inner_folder_path):
            if file_name.endswith(".py"):
                filenames.append(file_name[:-3])

    for filename in filenames:
        class_result = ""

        filename = os.path.join(model_inner_folder_path, f"{filename}.py")

        with open(filename, "r", encoding="utf-8") as file:
            tree = ast.parse(file.read(), filename=filename)

            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.FunctionDef):
                    signature = f"def {node.name}({_format_arguments(node.args)})"
                    signature += f" -> {ast.unparse(node.returns)}:" if node.returns else ":"

                    docstring = ast.get_docstring(node, clean=True)
                    if docstring:
                        docstring = f'    """\n    {docstring}\n    """'
                        class_result += f"{signature}\n{docstring}\n"
                    else:
                        class_result += f"{signature}\n\n"

                elif isinstance(node, ast.ClassDef):
                    class_signature = f"class {node.name}:"
                    class_result += f"{class_signature}\n"

                    docstring = ast.get_docstring(node, clean=True)
                    if docstring:
                        docstring = f'    """\n    {docstring}\n    """'
                        class_result += f"{docstring}\n"

                    for child in ast.iter_child_nodes(node):
                        if isinstance(child, ast.FunctionDef):
                            signature = f"def {child.name}({_format_arguments(child.args)})"
                            signature += f" -> {ast.unparse(child.returns)}:" if child.returns else ":"

                            docstring = ast.get_docstring(child, clean=True)
                            if docstring:
                                docstring = f'        """\n    {docstring}\n    """'
                                class_result += f"    {signature}\n{docstring}\n"
                            else:
                                class_result += f"    {signature}\n\n"

        result += class_result + "\n"

    return result.strip() + "\n"


def get_model_layer(
        data: str,
        model_layer_type: Literal["umple", "ecore"],
        filenames: list[str] | None,
) -> str:
    result = ""

    assets_model_folder_path = os.path.join(ASSETS_FOLDER, data, "model")

    if not os.path.exists(assets_model_folder_path):
        raise ValueError(f"Missing model folder at: {assets_model_folder_path}")

    model_inner_folder_path = os.path.join(assets_model_folder_path, model_layer_type)

    if not os.path.exists(model_inner_folder_path):
        raise ValueError(f"Missing model inner folder at: {model_inner_folder_path}")

    if filenames is None or len(filenames) == 0:
        filenames = []

        for file_name in os.listdir(model_inner_folder_path):
            if file_name.endswith(".py"):
                filenames.append(file_name[:-3])

    for filename in filenames:
        filename = os.path.join(model_inner_folder_path, f"{filename}.py")

        with open(filename, "r", encoding="utf-8") as file:
            result += file.read() + "\n"

    return result.strip() + "\n"


def get_domain_model(data: str, model_layer_type: Literal["umple", "ecore"]) -> str:
    if model_layer_type == "umple":
        domain_model_file_name = "model.ump"
    elif model_layer_type == "ecore":
        domain_model_file_name = "model.emf"
    else:
        raise ValueError(f"Unsupported model layer type: {model_layer_type}")

    domain_model_file_path = os.path.join(DATA_FOLDER, data, domain_model_file_name)

    if not os.path.exists(domain_model_file_path):
        raise ValueError(f"Missing domain model file at: {domain_model_file_path}")

    with open(domain_model_file_path, "r") as file:
        domain_model = file.read()

    return domain_model