import os
import shutil
from os import getcwd, mkdir
from os.path import join, dirname

import pandas as pd

from src.modeling.mapping import run_map_maker
from src.modeling.model_evaluation import compute_error_metrics
from src.modeling.model_object import LGBModel
from src.modeling.model_visualizations import (
    run_model_visuals,
    create_params_table,
)


def main(data_dir):
    # read in train and test data
    y_train_all = pd.read_csv(join(data_dir, "y_train.csv")).set_index("Block_Group")
    X_train = pd.read_csv(join(data_dir, "x_train.csv")).set_index("Block_Group")

    X_test = pd.read_csv(join(data_dir, "x_test.csv")).set_index("Block_Group")
    y_test = pd.read_csv(join(data_dir, "y_test.csv")).set_index("Block_Group")

    # set models visualizations save path
    model_viz_path = join(dirname(data_dir), "model_viz")
    # create new model viz foler
    if not os.path.exists(model_viz_path):
        mkdir(model_viz_path)
    else:
        shutil.rmtree(model_viz_path)  # Removes all the subdirectories!
        mkdir(model_viz_path)

    # specify hyper-parameter bounds
    bounds_lgb = {
        "feature_fraction": (0.3, 1),
        "lambda_l1": (0.0, 70.0),
        "lambda_l2": (0.0, 70.0),
        "learning_rate": (0.001, 1),
        "max_depth": (2, 7),
        "min_data_in_leaf": (5, 30),
        "min_gain_to_split": (0, 1),
        "min_sum_hessian_in_leaf": (0.01, 1),
        "num_leaves": (10, 50),
    }

    # create hyper-param bounds df and visualize it
    bounds_df = (
        pd.DataFrame(bounds_lgb)
            .transpose()
            .rename({0: "Lower Bound", 1: "Upper Bound"}, axis=1)
    )
    fig = create_params_table(bounds_df, "Hyperparameter")
    # could not find way to properly save so it is instead shown with out stopping processing
    fig.show()

    optimal_params_list = []

    models = []
    for col in y_train_all.columns:
        # y_train points towards current target call category
        y_train = y_train_all[col]

        # create instance of LGBModel, optimize it, then train
        model_pipeline = LGBModel(X_train, y_train, bounds_lgb)
        optimal_params = model_pipeline.optimize()
        optimal_params_list.append(optimal_params)
        model = model_pipeline.train(optimal_params)
        # model.save_model(join(join(data_dir, "models"), col + " model.txt"))
        models.append(model)

        # create and save model visuals
        run_model_visuals(model_viz_path, col, model, X_train, y_train, X_test, y_test)

    # save optimal params and visualize them
    optimal_params_df = pd.DataFrame(optimal_params_list, index=y_train_all.columns)
    optimal_params_df.to_csv(join(data_dir, "optimal_params.csv"))
    fig = create_params_table(optimal_params_df, "Model")
    fig.show()

    # compute and visualize train and test error metrics
    error_metrics_df, all_predictions_df = compute_error_metrics(
        X_train, X_test, y_train_all, y_test, models
    )
    fig = create_params_table(error_metrics_df, "Model")
    fig.show()
    all_predictions_df.to_csv(join(data_dir, "model_predictions.csv"))

    run_map_maker(model_viz_path, all_predictions_df, bg_filepath, fd_filepath)


if __name__ == "__main__":
    main(join(dirname((dirname(getcwd()))), "Data"))
