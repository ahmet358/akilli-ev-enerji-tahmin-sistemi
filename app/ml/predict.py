from __future__ import annotations

import joblib
import pandas as pd

from app.config import get_settings
from app.ml.model_registry import get_active_model_name
from app.ml.preprocessing import FEATURE_COLUMNS


class ModelNotReadyError(RuntimeError):
    pass


def predict_energy_consumption(feature_data: dict) -> tuple[float, str]:
    settings = get_settings()
    if not settings.model_path.exists() or not settings.preprocessor_path.exists():
        raise ModelNotReadyError(
            "Üretim modeli bulunamadı. Lütfen önce `python app/ml/train_model.py` komutunu çalıştırın."
        )

    preprocessor = joblib.load(settings.preprocessor_path)
    model = joblib.load(settings.model_path)
    frame = pd.DataFrame([{column: feature_data[column] for column in FEATURE_COLUMNS}])
    transformed = preprocessor.transform(frame)
    prediction = float(model.predict(transformed)[0])
    return max(prediction, 0.0), get_active_model_name()

