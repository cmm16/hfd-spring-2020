from src.modeling.model_object import LGBModel
from src.modeling.model_visualizations import visualize_model_features, visualize_predictions
import pandas as pd
from os.path import join, dirname
from os import getcwd, mkdir
import os
import shutil


def main(data_dir):
    y_train_all = pd.read_csv(join(data_dir, "y_train.csv")).set_index("Block_Group")
    X_train = pd.read_csv(join(data_dir, "x_train.csv")).set_index("Block_Group")

    bounds_lgb = {
        'feature_fraction': (0.3, 1),
        'lambda_l1': (0., 70.),
        'lambda_l2': (0., 70.),
        'learning_rate': (0.001, 1),
        'max_depth': (2, 7),
        'min_data_in_leaf': (5, 30),
        'min_gain_to_split': (0, 1),
        'min_sum_hessian_in_leaf': (0.01, 1),
        'num_leaves': (10, 50)
    }
    optimal_params_list = []

    if not os.path.exists(join(data_dir, "models")):
        mkdir(join(data_dir, "models"))
    else:
        shutil.rmtree(join(data_dir, "models"))  # Removes all the subdirectories!
        mkdir(join(data_dir, "models"))

    if not os.path.exists(join(data_dir, "model_viz")):
        mkdir(join(data_dir, "model_viz"))
    else:
        shutil.rmtree(join(data_dir, "model_viz"))  # Removes all the subdirectories!
        mkdir(join(data_dir, "model_viz"))
    model_viz_path = join(data_dir, "model_viz")

    for col in y_train_all.columns:
        y_train = y_train_all[col]
        model_pipeline = LGBModel(X_train, y_train, bounds_lgb)
        optimal_params = model_pipeline.optimize()
        optimal_params_list.append(optimal_params)

        model = model_pipeline.train(optimal_params)
        model.save_model(join(join(data_dir, "models"), col + " model.txt"))

        visualize_model_features(col + " Feature Importance", model, X_train, 'bar').savefig(join(model_viz_path, col + " abs"))
        visualize_model_features(col + " Feature Importance", model, X_train, None).savefig(join(model_viz_path, col + " heat"))
        visualize_predictions(model, X_train, y_train, col).savefig(join(model_viz_path, col + " imp"))

    pd.DataFrame(optimal_params_list, index=y_train_all.columns).to_csv(join(data_dir, "optimal_params.csv"))


if __name__ == '__main__':
    main(join(dirname((dirname(getcwd()))), "Data"))