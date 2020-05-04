import numpy as np
import pandas as pd


def compute_error_metrics(X_train, X_test, y_train, y_test, models):
    # final_X_df = X_train.append(X_test)
    # final_df = y_df.append(Y_test)
    res_y_train_df = y_train.copy()
    for i, col in enumerate(y_train):
        c_model = models[i][0]
        res_y_train_df["Predicted " + col] = c_model.predict(X_train)
    res_y_test_df = y_test.copy()
    for i, col in enumerate(y_test):
        model = models[i]
        res_y_test_df["Predicted " + col] = model.predict(X_test)
    combined_res_y_df = res_y_test_df.append(res_y_test_df)

    error_df = pd.DataFrame(zip(combined_res_y_df.iloc[:, :6].mean(), combined_res_y_df.iloc[:, :6].std()),
                            columns=["Mean", "Std"], index=combined_res_y_df.columns[:6])
    train_mae = []
    train_rsme = []
    test_mae = []
    test_rsme = []
    train_mape = []
    for i, col in enumerate(y_train):
        train_mae.append(np.mean(np.abs(res_y_train_df.iloc[:, i] - res_y_train_df.iloc[:, i + 6])))
        train_rsme.append(np.sqrt(np.mean(np.square(res_y_train_df.iloc[:, i] - res_y_train_df.iloc[:, i + 6]))))
        train_mape.append(
            np.mean(np.abs(res_y_train_df.iloc[:, i] - res_y_train_df.iloc[:, i + 6]) / res_y_train_df.iloc[:, i]))
    for i, col in enumerate(y_train):
        test_mae.append(np.mean(np.abs(combined_res_y_df.iloc[:, i] - combined_res_y_df.iloc[:, i + 6])))
        test_rsme.append(np.sqrt(np.mean(np.square(combined_res_y_df.iloc[:, i] - combined_res_y_df.iloc[:, i + 6]))))

    error_df["Train mae"] = train_mae
    error_df["Train rmse"] = train_rsme
    error_df["Test mae"] = test_mae
    error_df["Test rmse"] = test_rsme

    return error_df, combined_res_y_df