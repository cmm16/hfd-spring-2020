from os.path import join

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_per_capita_calls_by_block_group(df, title, output_dir, with_out_hobby):
    df["total_cals"] = df[
        ["fire", "health", "injuries_external", "mental_illness", "motor", "other"]
    ].sum(1)
    df["call_per_cap"] = df["total_cals"] / df["TotalPop"]
    sns.set(rc={"figure.figsize": (13, 8)})
    if with_out_hobby:
        new_df = df.copy()
        new_df = new_df[new_df["Block_Group"] != 482019800001.0]
        sns_plot = sns.swarmplot(new_df["call_per_cap"])

    else:
        sns_plot = sns.swarmplot(df["call_per_cap"])
    sns_plot.set_title(title)
    sns_plot.figure.savefig(join(output_dir, title))
    sns_plot.figure.clf()


def air_create_airport_bar_charts(counts, output_dir):
    calls = ["fire", "health", "injuries_external", "mental_illness", "motor", "other"]
    h = counts[counts["Block_Group"] == 482019800001]
    h = h[calls].values.reshape(-1)
    # print(h.columns)
    b = counts[counts["Block_Group"] == 482019801001]
    b = b[calls].values.reshape(-1)
    # print(b.columns)
    c = counts.drop([1482, 1483])
    c = c[calls].mean(axis=0).values
    # print(c2)
    a = pd.DataFrame([h, b, c], columns=calls, index=["hobby", "iah", "not-airport"])
    a.to_csv(join(output_dir, "airport_proportions.csv"))
    callLabels = [
        "Health (internal)",
        "External Injuries",
        "Mental Illness",
        "Motor",
        "Fire",
        "Other",
    ]
    fig = plt.figure(figsize=(20, 15))
    ax = fig.add_subplot(111)
    portions = a[calls].apply(lambda row: row / row.sum(), axis=1)
    portions.head()
    portions.plot(
        ax=ax,
        kind="bar",
        stacked=True,
        rot=0,
        color=["coral", "red", "yellow", "darkorange", "firebrick", "gold"],
    )
    plt.title("Call Distribution", fontsize=20)
    plt.ylabel("Proportion of Calls", fontsize=18)
    plt.yticks(fontsize=15)
    plt.xlabel("Block Group Type", fontsize=18)
    plt.legend(prop={"size": 20}, labels=callLabels)
    plt.xticks(ticks=range(0, 3), labels=["Hobby", "IAH", "Not-Airport"], fontsize=15)

    plt.savefig(join(output_dir, "airport_distributions.png"))


def run_airports_eda(output_dir, df):
    plot_per_capita_calls_by_block_group(
        df, "Swarm Plot of Calls per Capita by Block Group", output_dir, False
    )
    plot_per_capita_calls_by_block_group(
        df,
        "Swarm Plot of Calls per Capita by Block Group without Bush",
        output_dir,
        True,
    )
    air_create_airport_bar_charts(df, output_dir)
