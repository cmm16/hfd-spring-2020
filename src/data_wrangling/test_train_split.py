from sklearn.model_selection import train_test_split
import pandas as pd


def test_train_split(x_df, y_df, test_percent=0.2):
    """
    Splits input data into a train and test set and saves each separately

    Arguments:
         x_df (DataFrame): predictor variables data frame
         y_df (DataFrame): target variables data frame
         test_percent (float): float between 0.0 and 1.0, naturally .2

    Returns:
        Train and test data frames for both predictor and target variables
    """

    train_x, test_x = train_test_split(x_df, test_size=test_percent, random_state=17)
    train_y, test_y = train_test_split(y_df, test_size=test_percent, random_state=17)
    return train_x, test_x, train_y, test_y
