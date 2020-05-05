import numpy as np
import pandas as pd
from sklearn import datasets
import seaborn as sns
from sklearn.feature_selection import RFE
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import GradientBoostingRegressor
import matplotlib.pyplot as plt

import warnings
warnings.simplefilter('ignore', category=FutureWarning)

from bayes_opt import BayesianOptimization
import lightgbm as lgb


class LGBModel:
    def __init__(self, x_train, y_train, param_boundaries):
        self.param_boundaries = param_boundaries
        self.x_train = x_train
        self.y_train = y_train
        self.optimal_params = None

    def optimize(self):
        LGB_BO = BayesianOptimization(self.lgb_bayesian, self.param_boundaries, random_state=7, verbose=0)

        with warnings.catch_warnings():
            warnings.filterwarnings('ignore')
            LGB_BO.maximize(init_points=10, n_iter=10, acq='ucb')

        return LGB_BO.max['params']

    def train(self, params):
        formated_params = format_params(params)
        lgb_train = lgb.Dataset(self.x_train, self.y_train, free_raw_data=False, params={'verbose': -1})
        num_rounds = 5000
        clf = lgb.train(formated_params, lgb_train, num_rounds, verbose_eval=False)
        return clf

    def lgb_bayesian(self, num_leaves, min_data_in_leaf, learning_rate, min_sum_hessian_in_leaf, feature_fraction, lambda_l1,
                 lambda_l2, min_gain_to_split, max_depth):
        params = {
            'feature_fraction': feature_fraction,
            'lambda_l1': lambda_l1,
            'lambda_l2': lambda_l2,
            'learning_rate': learning_rate,
            'max_depth': max_depth,
            'min_data_in_leaf': min_data_in_leaf,
            'min_gain_to_split': min_gain_to_split,
            'min_sum_hessian_in_leaf': min_sum_hessian_in_leaf,
            'num_leaves': num_leaves,
            'bagging_fraction': 0.8,
            'bagging_freq': 6,
            'save_binary': True,
            'seed': 7,
            'feature_fraction_seed': 7,
            'bagging_seed': 7,
            'drop_seed': 7,
            'data_random_seed': 7,
            'objective': 'regression',
            'boosting_type': 'gbdt',
            'verbose': -1,
            'metric': {'l2', 'l1'},
            'is_unbalance': True,
            'boost_from_average': True,
            'n_jobs': -1
        }
        formated_params = format_params(params)
        KFolds = KFold(n_splits=2, shuffle=True, random_state=9).split(self.x_train, self.y_train)
        for fold in KFolds:
            lgb_train, lgb_valid, fold_val_x, fold_val_y = self.generate_lgb_fold_data(fold)

            num_rounds = 5000
            clf = lgb.train(formated_params, lgb_train, num_rounds,
                            valid_sets=[lgb_valid],
                            verbose_eval=False,
                            early_stopping_rounds=50)
            val_preds = clf.predict(fold_val_x, num_iterations=clf.best_iteration)

            score = np.mean(np.abs(fold_val_y - val_preds))
            return -1.0 * score

    def generate_lgb_fold_data(self, fold):
        fold_train_x = self.x_train.iloc[fold[0], :]
        fold_val_x = self.x_train.iloc[fold[1], :]
        fold_train_y = self.y_train.iloc[fold[0]]
        fold_val_y = self.y_train.iloc[fold[1]]

        lgb_train = lgb.Dataset(fold_train_x, fold_train_y, free_raw_data=False, params={'verbose': -1})
        lgb_valid = lgb.Dataset(fold_val_x, fold_val_y, free_raw_data=False, params={'verbose': -1})
        return lgb_train, lgb_valid, fold_val_x, fold_val_y


# run black
def format_params(param_boundaries):
        num_leaves = param_boundaries["num_leaves"]
        min_data_in_leaf = param_boundaries["min_data_in_leaf"]
        max_depth = param_boundaries["max_depth"]

        num_leaves = int(np.round(num_leaves))
        min_data_in_leaf = int(np.round(min_data_in_leaf))
        max_depth = int(np.round(max_depth))
        params = {
            'feature_fraction': param_boundaries["feature_fraction"],
            'lambda_l1': param_boundaries["lambda_l1"],
            'lambda_l2': param_boundaries["lambda_l2"],
            'learning_rate': param_boundaries["learning_rate"],
            'max_depth': max_depth,
            'min_data_in_leaf': min_data_in_leaf,
            'min_gain_to_split': param_boundaries["min_gain_to_split"],
            'min_sum_hessian_in_leaf': param_boundaries["min_sum_hessian_in_leaf"],
            'num_leaves': num_leaves,
            'bagging_fraction': 0.8,
            'bagging_freq': 6,
            'save_binary': True,
            'seed': 7,
            'feature_fraction_seed': 7,
            'bagging_seed': 7,
            'drop_seed': 7,
            'data_random_seed': 7,
            'objective': 'regression',
            'boosting_type': 'gbdt',
            'verbose': -1,
            'metric': {'l2', 'l1'},
            'is_unbalance': True,
            'boost_from_average': True,
            'n_jobs': -1
        }
        return params

