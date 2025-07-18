# llmvc: Code for Paper "Towards Domain Model Assisted LLM Code Generation"

## Requirements

- Python 3.12+
- pip 25.0+
- `pip install -r requirements.txt`
- You must have valid `OPENAI_API_KEY` and `DEEPSEEK_API_KEY` set in your environment variables to run the generation experiments.

## Code Structure
- `static/`: static resources.
  - `static/data/`: dataset used in the experiments.
  - `static/prompts/`: prompt templates used in the experiments.
- `assets/`: pre-processed assets from the static resources.
  - `static/<dataset_name>/model`: generated model layer codes from domain models.
  - `static/<dataset_name>/test`: reference (ideal) controller implementation and test cases.
- `output/`: our results from running the code. Delete this folder if you want to re-run the generation.
- `main.py`: run code generation experiments.
- `results.py`: display results from the experiments.

The rest are utility scripts supporting the operations above.

## Usage

### Install the requirements
   ```bash
   pip install -r requirements.txt
   ```
   
### Run the code generation experiments
1. Make sure to clear the `output/` folder.
2. Make sure you have valid `OPENAI_API_KEY` and `DEEPSEEK_API_KEY` set in your environment variables.
   - If you only have `OPENAI_API_KEY`, go into `main.py` and comment out line 99: `"deepseek-chat"`.
3. Run the main script:
   
  ```bash
   python main.py
   ```
   
### Display experiment results (either from our experiments or your own)
   ```bash
   python results.py
   ```