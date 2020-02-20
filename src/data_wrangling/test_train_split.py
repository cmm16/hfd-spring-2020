from sklearn.model_selection import train_test_split
import pandas as pd


def test_train_split(input_data_path, train_save_path, test_save_path, test_percent=.2):
    """
    Splits input data into a train and test set and saves each separately

    Arguments:
         input_data_path (str): String path to input data
         save_path (str): String path to desired save location
         test_percent (float): float between 0.0 and 1.0, naturally .2
    """

    df = pd.read_csv(input_data_path)
    train, test = train_test_split(df, test_size=test_percent, random_state=17)

    train.to_csv(train_save_path)
    test.to_csv(test_save_path)
