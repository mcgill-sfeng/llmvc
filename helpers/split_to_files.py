import os
import re


PARENT_FOLDER = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

def split_generated_file(input_file: str):
    # Read the entire content of the file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match each file section
    pattern = r"# %% NEW FILE ([\w\d_]+) BEGINS HERE %%\n"

    # Find all file headers and their positions
    matches = list(re.finditer(pattern, content))

    target_folder = os.path.join(PARENT_FOLDER, "assets/BTMS/model/umple")

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for i, match in enumerate(matches):
        filename = os.path.join(target_folder, f"{match.group(1)}.py")

        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        file_content = content[start:end].lstrip('\n')  # Strip leading newlines
        file_content = file_content.replace(".remove(", ".pop(")  # fix dict deletion error

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(file_content)

        print(f"Written: {filename}")


if __name__ == '__main__':
    model_path = os.path.join(PARENT_FOLDER, "BTMS_generated_umple.py.template")

    split_generated_file(model_path)
