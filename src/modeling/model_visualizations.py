import seaborn as sns
import matplotlib.pyplot as plt
import shap
import pandas as pd
import matplotlib.lines as mlines
from sklearn.metrics import r2_score

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
    fig=plt.figure(figsize=(10, 8))
    plt.title(name, fontsize=22)
    # viz type either 'bar' or None
    shap.summary_plot(shap_values, X_train, plot_type=viz_type, show=False, plot_size=(10, 8))
    return plt




def create_model_bounds_df(bounds_lgb):
    return pd.DataFrame(bounds_lgb).transpose().rename({0: "Lower Bound", 1: "Upper Bound"}, axis=1)


def visualize_predictions(model, x_df, y_df, name):
    fig=plt.figure(figsize=(8, 6))
    plt.plot(model.predict(x_df), y_df, 'p', alpha=0.5)
    plt.ylim(min(y_df-.001), max(y_df) + .001)
    plt.xlim(min(model.predict(x_df) - .001), max(model.predict(x_df)) + .001)
    plt.plot([0,100], [0, 100], c="red")
    plt.title("Actual vs Predicted Percent " + name + " Calls by Block Group")
    plt.xlabel("Predicted Call Category Percent (%)")
    plt.ylabel("True Call Category Percent (%)")
    blue_dot = mlines.Line2D([], [], color='blue', marker='.', linestyle='None',
                          markersize=10, label='Blue point')
    red_line = mlines.Line2D([], [], color='red', marker='_', linestyle='None',
                          markersize=10, label='Red line')
    plt.legend([red_line, blue_dot], ["Perfect Prediction Line", "Block Group"], loc='lower right')
    return plt
