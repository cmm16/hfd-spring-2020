from sklearn.model_selection import train_test_split
import pandas as pd


def test_train_split(input_data_path, save_path):
    df = pd.read_csv(input_data_path)
    train, test = train_test_split(df, test_size=0.2)
    train.to_csv(save_path + "_train")
    test.to_csv(save_path + "_test")
