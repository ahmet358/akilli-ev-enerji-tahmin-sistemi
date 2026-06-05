from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[2]))

import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR

from app.config import get_settings
from app.ml.model_evaluation import calculate_regression_metrics
from app.ml.preprocessing import FEATURE_COLUMNS, TARGET_COLUMN, build_preprocessor, get_feature_names


def load_training_dataset() -> tuple[pd.DataFrame, str]:
    settings = get_settings()
    if settings.dataset_path.exists():
        return pd.read_csv(settings.dataset_path), str(settings.dataset_path)
    if settings.sample_dataset_path.exists():
        print(
            "Bilgi: Gerçek dataset bulunamadı. Eğitim için küçük örnek dataset kullanılacak. "
            "Üretim kalitesinde sonuçlar için data/energy_consumption.csv dosyasını ekleyin."
        )
        return pd.read_csv(settings.sample_dataset_path), str(settings.sample_dataset_path)
    raise FileNotFoundError(
        "Dataset bulunamadı. Lütfen enerji tüketimi verinizi `data/energy_consumption.csv` konumuna "
        "yerleştirin. Beklenen kolonlar data/README.md içinde açıklanmıştır."
    )


def validate_dataset(data: pd.DataFrame) -> None:
    expected_columns = set(FEATURE_COLUMNS + [TARGET_COLUMN])
    missing_columns = expected_columns.difference(data.columns)
    if missing_columns:
        missing_text = ", ".join(sorted(missing_columns))
        raise ValueError(f"Dataset eksik kolonlar içeriyor: {missing_text}")
    if data.empty:
        raise ValueError("Dataset boş. Model eğitimi için en az birkaç gözlem gereklidir.")
    if data[TARGET_COLUMN].isna().any():
        raise ValueError("Hedef değişken olan enerji tüketimi kolonunda eksik değer bulunmamalıdır.")


def candidate_models() -> dict:
    return {
        "Doğrusal Regresyon": LinearRegression(),
        "Ridge Regresyon": Ridge(alpha=1.0, random_state=42),
        "Random Forest Regressor": RandomForestRegressor(
            n_estimators=180,
            random_state=42,
            min_samples_leaf=2,
            n_jobs=-1,
        ),
        "Gradient Boosting Regressor": GradientBoostingRegressor(random_state=42),
        "Support Vector Regressor": SVR(kernel="rbf", C=20, epsilon=0.08),
    }


def select_best_model(results: list[dict]) -> dict:
    return sorted(results, key=lambda item: (item["RMSE"], -item["R2 Score"]))[0]


def save_feature_importance(model, preprocessor) -> None:
    settings = get_settings()
    settings.feature_importance_csv.parent.mkdir(parents=True, exist_ok=True)
    if not hasattr(model, "feature_importances_"):
        if settings.feature_importance_csv.exists():
            settings.feature_importance_csv.unlink()
        return

    feature_names = get_feature_names(preprocessor)
    importance_frame = pd.DataFrame(
        {
            "ozellik": feature_names,
            "onem_skoru": model.feature_importances_,
        }
    ).sort_values("onem_skoru", ascending=False)
    importance_frame.to_csv(settings.feature_importance_csv, index=False, encoding="utf-8")


def train_and_save() -> dict:
    settings = get_settings()
    data, dataset_source = load_training_dataset()
    validate_dataset(data)

    X = data[FEATURE_COLUMNS].copy()
    y = data[TARGET_COLUMN].copy()
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    preprocessor = build_preprocessor()
    X_train_prepared = preprocessor.fit_transform(X_train)
    X_test_prepared = preprocessor.transform(X_test)

    trained_models = {}
    results = []
    for model_name, model in candidate_models().items():
        model.fit(X_train_prepared, y_train)
        predictions = model.predict(X_test_prepared)
        metrics = calculate_regression_metrics(y_test, predictions)
        results.append({"model_name": model_name, **metrics})
        trained_models[model_name] = model

    best_result = select_best_model(results)
    best_model_name = best_result["model_name"]
    best_model = trained_models[best_model_name]

    settings.model_path.parent.mkdir(parents=True, exist_ok=True)
    settings.preprocessor_path.parent.mkdir(parents=True, exist_ok=True)
    settings.model_results_json.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(best_model, settings.model_path)
    joblib.dump(preprocessor, settings.preprocessor_path)
    save_feature_importance(best_model, preprocessor)

    report = {
        "best_model": best_model_name,
        "selection_rule": "En düşük RMSE ve eşitlik durumunda en yüksek R2 Score",
        "dataset_source": dataset_source,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "results": results,
    }
    settings.model_results_json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    pd.DataFrame(results).to_csv(settings.model_results_csv, index=False, encoding="utf-8")
    return report


if __name__ == "__main__":
    training_report = train_and_save()
    print("Model eğitimi tamamlandı.")
    print(f"Seçilen üretim modeli: {training_report['best_model']}")
    print(f"Rapor dosyası: {get_settings().model_results_json}")

