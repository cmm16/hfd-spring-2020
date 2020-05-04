from src.modeling.model_pipeline import LGBModelPipeline
from src.modeling.model_visualizations import visualize_model_features
import pandas as pd
import lightgbm as lgb

# correct data paths later
X_train = pd.read_csv("X_train_dem_only.csv").set_index("Block_Group")
y_train_all = pd.read_csv("Y_train.csv").set_index("Block_Group")

bounds_lgb = {
    'feature_fraction': (0.3, 1),
    'lambda_l1': (0., 70.),
    'lambda_l2': (0., 70.),
    'learning_rate': (0.001, 1),
    'max_depth': (2, 9),
    'min_data_in_leaf': (5, 50),
    'min_gain_to_split': (0, 1),
    'min_sum_hessian_in_leaf': (0.01, 1),
    'num_leaves': (10, 100)
}

for col in y_train_all.columns:
    y_train = y_train_all[col]
    model_pipeline = LGBModelPipeline(X_train, y_train, bounds_lgb)
    optimal_params = model_pipeline .optimize()
    model = model_pipeline .train(optimal_params)
    lgb.save(model, col + " model")

    visualize_model_features(col + " Feature Importance", model, X_train, 'bar')
    visualize_model_features(col + " Feature Importance", model, X_train, None)

