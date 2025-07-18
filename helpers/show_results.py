import os
import pandas as pd
from tabulate import tabulate

from graph.controller.state import Config

OUTPUT_FOLDER = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "output"))


def show_table(csv_path):
    df = pd.read_csv(csv_path)

    df['formatted'] = df.apply(
        lambda row: f"{row['test_pass'] / row['test_total'] * 100:.0f}% ({row['test_pass']}/{row['test_total']})", axis=1
    )

    pivot = df.pivot_table(
        index=['modeling_tool', 'llm'],
        columns='run_config',
        values='formatted',
        aggfunc='first'
    )

    pivot = pivot.reset_index()

    pivot = pivot.reindex(columns=["modeling_tool", "llm",
        "C", "CA", "CG", "CAG", "CFG",
        "CD", "CDA", "CDG", "CDAG", "CDFG",
        "CS", "CSA", "CSG", "CSAG", "CSFG",
        "CDS", "CDSA", "CDSG", "CDSAG", "CDSFG"]
    )

    print("\n\nTable of Results:")
    print(tabulate(pivot, headers='keys', tablefmt='grid', showindex=False))


def show_stats(results):
    stats = {}

    for result in results:
        print(result[2]["data"], result[2]["model_name"], result[1], result[3])
        if result[1] not in stats:
            stats[result[1]] = result[3]
        else:
            for i in range(len(result[3])):
                stats[result[1]][i] += result[3][i]


def header_from_config(config: Config) -> str:
    with_description = config["with_description"]
    with_feature = config["with_feature"]
    with_domain_model = config["with_domain_model"]
    with_model_layer = config["with_model_layer"]
    with_full_model_layer = config["with_full_model_layer"]

    header = "C"
    if with_description:
        header += "D"

    if with_feature:
        header += "S"

    if with_domain_model:
        header += "A"

    if with_model_layer:
        if with_full_model_layer:
            header += "F"

        header += "G"

    return header