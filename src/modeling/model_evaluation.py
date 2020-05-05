import numpy as np
import pandas as pd
from sklearn.metrics import r2_score


def compute_error_metrics(X_train, X_test, y_train, y_test, models):
    train_prediction_df = pd.DataFrame(y_train.index)
    test_prediction_df = pd.DataFrame(y_test.index)

    for i, col in enumerate(y_train):
        c_model = models[i]
        train_prediction_df["Predicted " + col] = c_model.predict(X_train)

    for i, col in enumerate(y_test):
        model = models[i]
        test_prediction_df["Predicted " + col] = model.predict(X_test)

    all_predictions_df = test_prediction_df.append(train_prediction_df)
    all_actuals_df = y_test.append(y_train)

    error_df = pd.DataFrame(zip(all_actuals_df.mean(), all_actuals_df.std()),
                            columns=["Mean", "Std"], index=all_actuals_df.columns)
    train_mae = []
    train_rsme = []
    train_r2_scores = []

    test_mae = []
    test_rsme = []
    test_r2_scores = []

    for i, col in enumerate(y_train.columns):
        y_cur = y_train[col]
        y_pred_cur = train_prediction_df.iloc[:, i]
        train_mae.append(np.mean(np.abs(y_cur - y_pred_cur)))
        train_rsme.append(np.sqrt(np.mean(np.square(y_cur - y_pred_cur))))
        train_r2_scores.append(r2_score(y_cur, y_pred_cur))
    for i, col in enumerate(y_train):
        y_cur = y_train[col]
        y_pred_cur = train_prediction_df.iloc[:, i]
        test_mae.append(np.mean(np.abs(y_cur - y_pred_cur)))
        test_rsme.append(np.sqrt(np.mean(np.square(y_cur - y_pred_cur))))
        test_r2_scores.append(r2_score(y_cur, y_pred_cur))

    error_df["Train R^2"] = train_r2_scores
    error_df["Train MAE"] = train_mae
    error_df["Train RMSE"] = train_rsme
    error_df["Test R^2"] = test_r2_scores
    error_df["Test MAE"] = test_mae
    error_df["Test RMSE"] = test_rsme
    error_df.append([error_df[col].mean() for col in error_df.columns])

    return error_df
