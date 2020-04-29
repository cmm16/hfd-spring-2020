import seaborn as sns
import matplotlib.pyplot as plt
import shap


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

