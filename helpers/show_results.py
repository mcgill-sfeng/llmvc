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

    print("\n\nTable of Results:")
    print(tabulate(pivot.reset_index(), headers='keys', tablefmt='grid', showindex=False))


def show_stats(results):
    stats = {}

    for result in results:
        print(result[2]["data"], result[2]["model_name"], result[1], result[3])
        if result[1] not in stats:
            stats[result[1]] = result[3]
        else:
            for i in range(len(result[3])):
                stats[result[1]][i] += result[3][i]

    no_d_s = [0] * len(results[0][3])
    yes_d_s = [0] * len(results[0][3])
    no_a_f_g = [0] * len(results[0][3])
    yes_a_f_g = [0] * len(results[0][3])
    ds_afg = [0] * len(results[0][3])

    for key, value in stats.items():
        if not any(c in key for c in ["d", "s"]):
            for i in range(len(value)):
                no_d_s[i] += value[i]
        else:
            for i in range(len(value)):
                yes_d_s[i] += value[i]

        if not any(c in key for c in ["a", "f", "g"]):
            for i in range(len(value)):
                no_a_f_g[i] += value[i]
        else:
            for i in range(len(value)):
                yes_a_f_g[i] += value[i]

        if any(c in key for c in ["d", "s"]) and any(c in key for c in ["a", "f", "g"]):
            for i in range(len(value)):
                ds_afg[i] += value[i]

    print("\n\nStats:")

    for key, value in stats.items():
        print(f"{key}: {value}")

    print("\n\nAggregated Stats:")
    print("no_d_s = ", no_d_s)
    print("yes_d_s = ", yes_d_s)
    print("no_a_f_g = ", no_a_f_g)
    print("yes_a_f_g = ", yes_a_f_g)
    print("ds_afg = ", ds_afg)


def header_from_config(config: Config) -> str:
    with_description = config["with_description"]
    with_feature = config["with_feature"]
    with_domain_model = config["with_domain_model"]
    with_model_layer = config["with_model_layer"]
    with_full_model_layer = config["with_full_model_layer"]

    header = "c"
    if with_description:
        header += "d"

    if with_feature:
        header += "s"

    if with_domain_model:
        header += "a"

    if with_model_layer:
        if with_full_model_layer:
            header += "f"
        else:
            header += "g"

    return header