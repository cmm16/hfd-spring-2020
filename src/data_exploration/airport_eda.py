import seaborn as sns
from os.path import join


def plot_per_capita_calls_by_block_group(df, title, output_dir, with_out_hobby):
    df["total_cals"] = df[["fire",
"health",
'injuries_external',
'mental_illness',
'motor',
'other']].sum(1)
    df["call_per_cap"] = df["total_cals"] / df["TotalPop"]
    sns.set(rc={"figure.figsize":(13,8)})
    if with_out_hobby:
        new_df = df.copy()
        new_df = new_df[new_df["Block_Group"] != 482019800001.0]
        sns_plot = sns.swarmplot(new_df["call_per_cap"])

    else:
        sns_plot = sns.swarmplot(df["call_per_cap"])
    sns_plot.set_title(title)
    sns_plot.figure.savefig(join(output_dir, title))
    sns_plot.figure.clf()

