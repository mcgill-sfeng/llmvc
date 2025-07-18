import re

MODEL_LAYER_IMPORT = "from model_layer import"
TEST_MODULE_PATTERN = re.compile(r"TEST_MODULE\s*=\s*['\"]([^'\"]+)['\"]", re.MULTILINE)


def path_to_package(path: str, root: str) -> str:
    parts = path.replace("\\", "/").split("/")

    try:
        root_index = parts.index(root)
    except ValueError:
        raise ValueError(f"Root directory '{root}' not found in path: {path}")

    return ".".join(parts[root_index:])


def replace_model_layer_import(code: str, package: str) -> str:
    return code.replace(MODEL_LAYER_IMPORT, f"from {package} import")


def replace_controller_file_import(code: str, replacement: str) -> str:
    match = TEST_MODULE_PATTERN.search(code)
    if not match:
        raise ValueError("MODEL_MODULE assignment not found.")

    old_module = match.group(1)

    return code.replace(old_module, replacement)
