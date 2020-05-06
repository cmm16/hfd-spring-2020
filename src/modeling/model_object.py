import warnings

import numpy as np
from sklearn.metrics import r2_score
from sklearn.model_selection import KFold

warnings.simplefilter("ignore", category=FutureWarning)

from bayes_opt import BayesianOptimization
import lightgbm as lgb


class LGBModel:
    """
    LGBModel can train and optimize the hyper-parameters of a light gradient boosting model

    Arguments:
        x_train (DataFrame): All predictor variables
        y_train (DataFrame): Single target variable
        param_boundaries (Dict(Str: Tup(Int, Int))): Dictionary mapping hyper-parameter string names to tuple of values
    """
    def __init__(self, x_train, y_train, param_boundaries):
        self.param_boundaries = param_boundaries
        self.x_train = x_train
        self.y_train = y_train
        self.optimal_params = None

    def optimize(self):
        """ optimizes the lgbm hyper-params using baysain optimization"""
        LGB_BO = BayesianOptimization(
            self.lgb_bayesian, self.param_boundaries, random_state=7, verbose=0
        )
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            LGB_BO.maximize(init_points=10, n_iter=10, acq="ucb")

        return LGB_BO.max["params"]

    def train(self, params):
        """
        Trains lgbm model given hyper-params

        Arguments:
            params (Dict (Str: float)): A dictionary mapping hyper-param name to value

        Returns:
            The trained model
        """
        models = []
        KFolds = KFold(n_splits=5, shuffle=True, random_state=9).split(
            self.x_train, self.y_train
        )
        formated_params = format_params(params)
        for fold in KFolds:
            lgb_train, lgb_valid, fold_val_x, fold_val_y = self.generate_lgb_fold_data(
                fold
            )
            # lgb_train = lgb.Dataset(self.x_train, self.y_train, free_raw_data=False, params={'verbose': -1})
            num_rounds = 5000
            clf = lgb.train(
                formated_params,
                lgb_train,
                num_rounds,
                valid_sets=[lgb_valid],
                verbose_eval=False,
                early_stopping_rounds=50,
            )
            # val_preds = clf.predict(fold_val_x, num_iterations=clf.best_iteration)
            models.append(clf)
        return models

    def lgb_bayesian(
        self,
        num_leaves,
        min_data_in_leaf,
        learning_rate,
        min_sum_hessian_in_leaf,
        feature_fraction,
        lambda_l1,
        lambda_l2,
        min_gain_to_split,
        max_depth,
    ):
        """ Bayesian optimization function to optimize parameters over given bounds for given data """
        params = {
            "feature_fraction": feature_fraction,
            "lambda_l1": lambda_l1,
            "lambda_l2": lambda_l2,
            "learning_rate": learning_rate,
            "max_depth": max_depth,
            "min_data_in_leaf": min_data_in_leaf,
            "min_gain_to_split": min_gain_to_split,
            "min_sum_hessian_in_leaf": min_sum_hessian_in_leaf,
            "num_leaves": num_leaves,
            "bagging_fraction": 0.8,
            "bagging_freq": 6,
            "save_binary": True,
            "seed": 7,
            "feature_fraction_seed": 7,
            "bagging_seed": 7,
            "drop_seed": 7,
            "data_random_seed": 7,
            "objective": "regression",
            "boosting_type": "gbdt",
            "verbose": -1,
            "metric": {"l2"},
            "is_unbalance": True,
            "boost_from_average": True,
            "n_jobs": -1,
        }
        formated_params = format_params(params)
        KFolds = KFold(n_splits=5, shuffle=True, random_state=9).split(
            self.x_train, self.y_train
        )

        lgb_train, lgb_valid, fold_val_x, fold_val_y = self.generate_lgb_fold_data(
            list(KFolds)[0]
        )

        num_rounds = 5000
        clf = lgb.train(
            formated_params,
            lgb_train,
            num_rounds,
            valid_sets=[lgb_valid],
            verbose_eval=False,
            early_stopping_rounds=50,
        )
        val_preds = clf.predict(fold_val_x, num_iterations=clf.best_iteration)

        score = r2_score(fold_val_y, val_preds)
        return score

    def generate_lgb_fold_data(self, fold):
        """ Generates data needed to train lgb object given Kfolds fold object"""
        fold_train_x = self.x_train.iloc[fold[0], :]
        fold_val_x = self.x_train.iloc[fold[1], :]
        fold_train_y = self.y_train.iloc[fold[0]]
        fold_val_y = self.y_train.iloc[fold[1]]

        lgb_train = lgb.Dataset(
            fold_train_x, fold_train_y, free_raw_data=False, params={"verbose": -1}
        )
        lgb_valid = lgb.Dataset(
            fold_val_x, fold_val_y, free_raw_data=False, params={"verbose": -1}
        )
        return lgb_train, lgb_valid, fold_val_x, fold_val_y


def format_params(param_boundaries):
    """ Properly formats hyper-parameter boundaries for lgbm training """
    num_leaves = param_boundaries["num_leaves"]
    min_data_in_leaf = param_boundaries["min_data_in_leaf"]
    max_depth = param_boundaries["max_depth"]

    num_leaves = int(np.round(num_leaves))
    min_data_in_leaf = int(np.round(min_data_in_leaf))
    max_depth = int(np.round(max_depth))
    params = {
        "feature_fraction": param_boundaries["feature_fraction"],
        "lambda_l1": param_boundaries["lambda_l1"],
        "lambda_l2": param_boundaries["lambda_l2"],
        "learning_rate": param_boundaries["learning_rate"],
        "max_depth": max_depth,
        "min_data_in_leaf": min_data_in_leaf,
        "min_gain_to_split": param_boundaries["min_gain_to_split"],
        "min_sum_hessian_in_leaf": param_boundaries["min_sum_hessian_in_leaf"],
        "num_leaves": num_leaves,
        "bagging_fraction": 0.8,
        "bagging_freq": 6,
        "save_binary": True,
        "seed": 7,
        "feature_fraction_seed": 7,
        "bagging_seed": 7,
        "drop_seed": 7,
        "data_random_seed": 7,
        "objective": "regression",
        "boosting_type": "gbdt",
        "verbose": -1,
        "metric": {"l2"},
        "is_unbalance": True,
        "boost_from_average": True,
        "n_jobs": -1,
    }
    return params
