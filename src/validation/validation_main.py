from src.modeling.model_evaluation import compute_error_metrics
import pandas as pd
import lightgbm as lgb
from os.path import join, dirname
from os import getcwd, listdir

def main(data_dir):
    y_train = pd.read_csv(join(data_dir, "y_train.csv")).set_index("Block_Group")
    X_train = pd.read_csv(join(data_dir, "x_train.csv")).set_index("Block_Group")

    y_test = pd.read_csv(join(data_dir, "y_test.csv")).set_index("Block_Group")
    X_test = pd.read_csv(join(data_dir, "x_test.csv")).set_index("Block_Group")

    models = [lgb.basic.Booster(model_file=file) for file in listdir(join(data_dir, "models"))]

    compute_error_metrics(X_train, X_test, y_train, y_test, models)


if __name__ == '__main__':
    main(join(dirname((dirname(getcwd()))), "Data"))