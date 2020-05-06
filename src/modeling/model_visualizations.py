from os.path import join

import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import shap


def visualize_model_features(name, model, X_train, viz_type):
    """ Create SHAP value feature importance or heatmap for given model

    Arguments:
        name (str): Name of plot
        model (Instance of a trained tree based model): model to visualize
        X_train (DataFrame): data frame with same predictor variables as those used to train model
        viz_type: bar or None, bar will give absolute SHAP values plot, None will give heat map of SHAP values

    Returns:
        instance of the plot
    """
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_train)
    fig = plt.figure(figsize=(10, 8))
    plt.title(name, fontsize=22)
    # viz type either 'bar' or None
    shap.summary_plot(
        shap_values, X_train, plot_type=viz_type, show=False, plot_size=(10, 8)
    )
    return plt


def create_model_bounds_df(bounds_lgb):
    """ Create data frame to show off model hyper-parameter bounds """
    return (
        pd.DataFrame(bounds_lgb)
        .transpose()
        .rename({0: "Lower Bound", 1: "Upper Bound"}, axis=1)
    )


def visualize_predictions(model, x_df, y_df, name):
    """ Creates plot of the true vs predicted values for a given target

    Arguments:
        name (str): Name of plot
        model (Instance of a trained tree based model): model to visualize
        x_df (DataFrame): data frame with same predictor variables as those used to train model
        y_df (DAtaFrame): target variable

    Returns:
        instance of the plot
    """
    fig = plt.figure(figsize=(8, 6))
    preds = []
    for s_model in model:
        preds.append(s_model.predict(x_df))
    plt.plot(np.mean(preds, 0), y_df, "p", alpha=0.5)

    plt.ylim(min(y_df - 0.001), max(y_df) + 0.001)
    plt.xlim(min(np.mean(preds, 0) - 0.001), max(np.mean(preds, 0) + 0.001))
    plt.plot([0, 100], [0, 100], c="red")
    plt.title("Actual vs Predicted Percent " + name + " Calls by Block Group")
    plt.xlabel("Predicted Call Category Percent (%)")
    plt.ylabel("True Call Category Percent (%)")
    blue_dot = mlines.Line2D(
        [],
        [],
        color="blue",
        marker=".",
        linestyle="None",
        markersize=10,
        label="Blue point",
    )
    red_line = mlines.Line2D(
        [],
        [],
        color="red",
        marker="_",
        linestyle="None",
        markersize=10,
        label="Red line",
    )
    plt.legend(
        [red_line, blue_dot],
        ["Perfect Prediction Line", "Block Group"],
        loc="lower right",
    )
    return plt


def create_params_table(optimal_params_df, name):
    """ Create data frame to show off models optimal hyper-parameters """
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=[name] + list(optimal_params_df.columns),
                    fill_color="paleturquoise",
                    align="left",
                ),
                cells=dict(
                    values=[optimal_params_df.index]
                    + [col for col in optimal_params_df.transpose().values],
                    fill_color="lavender",
                    align="left",
                ),
            )
        ]
    )
    return fig


def run_model_visuals(model_viz_path, col, model, X_train, y_train, X_test, y_test):
    """ Runs and saves all model visuals """
    visualize_model_features(
        col + " Feature Importance", model[0], X_train, "bar"
    ).savefig(join(model_viz_path, col + " abs"))
    visualize_model_features(
        col + " Feature Importance", model[0], X_train, None
    ).savefig(join(model_viz_path, col + " heat"))
    visualize_predictions(model, X_train, y_train, "Train " + col[7:]).savefig(
        join(model_viz_path, col + "train imp")
    )
    visualize_predictions(model, X_test, y_test[col], "Test " + col[7:]).savefig(
        join(model_viz_path, col + "test imp")
    )


def visualize_targets(y_data):
    """
    Creates visuals that show the univariate and bivariate relationships of the variables

    Arguments:
        y_data (DataFrame):
    """
    sns.pairplot(data=y_data)
    for col in y_data.columns:
        # add titles
        sns.swarmplot(col, data=y_data)
        plt.show()
