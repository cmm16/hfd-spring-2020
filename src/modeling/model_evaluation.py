import numpy as np
import pandas as pd


def compute_error_metrics(X_train, X_test, y_train, y_test, models):
    """
    Creates predictions for test and train data then computes error metrics for test and train data

    Arguments:
        X_train (Data Frame): Train data frame of predictors
        X_test (Data Frame): Test data frame of predictors
        y_train (Data Frame): Train data frame of targets
        y_test (Data Frame): Test data frame of targets
        models: list of models one model per target data frame column
    """
    train_prediction_df = pd.DataFrame(y_train.index).set_index("Block_Group")
    test_prediction_df = pd.DataFrame(y_test.index).set_index("Block_Group")

    # used each model to predict X_train and X_test
    for i, col in enumerate(y_train):
        c_model = models[i]
        c_preds = []
        for s_c_model in c_model:
            c_preds.append(s_c_model.predict(X_train))
        train_prediction_df["Predicted " + col] = np.mean(c_preds, 0)
    for i, col in enumerate(y_test):
        c_model = models[i]
        c_preds = []
        for s_c_model in c_model:
            c_preds.append(s_c_model.predict(X_test))
        test_prediction_df["Predicted " + col] = np.mean(c_preds, 0)

    # create df of all predictions
    all_predictions_df = test_prediction_df.append(train_prediction_df)
    all_actuals_df = y_test.append(y_train)

    # create error metric data frame
    error_df = pd.DataFrame(zip(all_actuals_df.mean(), all_actuals_df.std()),
                            columns=["Mean", "Std"], index=all_actuals_df.columns)
    train_mae = []
    train_rsme = []
    test_mae = []
    test_rsme = []

    # compute error metrics per model
    for i, col in enumerate(y_train.columns):
        y_cur = y_train[col]
        y_pred_cur = train_prediction_df.iloc[:, i]
        train_mae.append(np.mean(np.abs(y_cur - y_pred_cur)))
        train_rsme.append(np.sqrt(np.mean(np.square(y_cur - y_pred_cur))))
    for i, col in enumerate(y_train):
        y_cur = y_test[col]
        y_pred_cur = test_prediction_df.iloc[:, i]
        test_mae.append(np.mean(np.abs(y_cur - y_pred_cur)))
        test_rsme.append(np.sqrt(np.mean(np.square(y_cur - y_pred_cur))))

    # add computed error metrics to error metric data frame
    error_df["Train MAE"] = train_mae
    error_df["Train RMSE"] = train_rsme
    error_df["Test MAE"] = test_mae
    error_df["Test RMSE"] = test_rsme
    error_df.append([error_df[col].mean() for col in error_df.columns])

    return error_df, all_predictions_df
