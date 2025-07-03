import os

from getters import DATA_FOLDER


def get_description(data: str) -> str:
    data_path = os.path.join(DATA_FOLDER, data) if data else None

    if not data_path or not os.path.exists(data_path):
        raise ValueError(f"Missing data folder at: {data_path}")

    # description
    description_file_path = os.path.join(data_path, "description.txt")

    if not os.path.exists(description_file_path):
        raise ValueError(f"Missing description file at: {description_file_path}")

    with open(description_file_path, "r") as file:
        description = file.read()

    return description