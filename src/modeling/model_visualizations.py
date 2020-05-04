import seaborn as sns
import matplotlib.pyplot as plt
import shap
import pandas as pd


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


def visualize_model_features(name, model, X_train, viz_type):
    """

    """
    # add title
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_train)
    plt.title(name, fontsize=22)
    # viz type either 'bar' or None
    shap.summary_plot(shap_values, X_train, plot_type=viz_type)


def create_model_bounds_df(bounds_lgb):
    return pd.DataFrame(bounds_lgb).transpose().rename({0: "Lower Bound", 1: "Upper Bound"}, axis=1)
