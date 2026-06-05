from __future__ import annotations

from math import sqrt

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def calculate_regression_metrics(y_true, y_pred) -> dict:
    mse = mean_squared_error(y_true, y_pred)
    return {
        "MAE": round(float(mean_absolute_error(y_true, y_pred)), 4),
        "MSE": round(float(mse), 4),
        "RMSE": round(float(sqrt(mse)), 4),
        "R2 Score": round(float(r2_score(y_true, y_pred)), 4),
    }

