import os

from getters import DATA_FOLDER


def get_feature_requirement(data: str, feature_name: str) -> str:
    feature_folder_path = os.path.join(DATA_FOLDER, data, "features")
    if not os.path.exists(feature_folder_path):
        raise ValueError(f"Missing feature folder at: {feature_folder_path}")
    if feature_name:
        feature_file_path = os.path.join(feature_folder_path, f"{feature_name}.feature")
        if not os.path.exists(feature_file_path):
            raise ValueError(f"Missing feature file at: {feature_file_path}")

        with open(feature_file_path, "r") as file:
            feature_requirement = file.read()

            return feature_requirement
    else:
        feature_requirement = ""

        for file_name in os.listdir(feature_folder_path):
            if file_name.endswith(".feature"):
                feature_file_path = os.path.join(feature_folder_path, file_name)

                with open(feature_file_path, "r") as file:
                    feature_requirement += file.read() + "\n"

        return feature_requirement
