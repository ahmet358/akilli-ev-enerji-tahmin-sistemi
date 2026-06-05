from __future__ import annotations

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


NUMERICAL_FEATURES = [
    "temperature",
    "humidity",
    "hour",
    "day_of_week",
    "month",
    "active_appliances",
    "lights_usage",
    "heating_status",
    "cooling_status",
    "household_size",
]

CATEGORICAL_FEATURES = ["weather_condition"]
FEATURE_COLUMNS = NUMERICAL_FEATURES + CATEGORICAL_FEATURES
TARGET_COLUMN = "energy_consumption"


def create_one_hot_encoder() -> OneHotEncoder:
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def build_preprocessor() -> ColumnTransformer:
    numerical_pipeline = Pipeline(
        steps=[
            ("eksik_deger", SimpleImputer(strategy="median")),
            ("olcekleme", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("eksik_deger", SimpleImputer(strategy="most_frequent")),
            ("kodlama", create_one_hot_encoder()),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("sayisal", numerical_pipeline, NUMERICAL_FEATURES),
            ("kategorik", categorical_pipeline, CATEGORICAL_FEATURES),
        ],
        remainder="drop",
    )


def get_feature_names(preprocessor: ColumnTransformer) -> list[str]:
    names: list[str] = []
    names.extend(NUMERICAL_FEATURES)
    categorical_pipeline = preprocessor.named_transformers_.get("kategorik")
    if categorical_pipeline:
        encoder = categorical_pipeline.named_steps.get("kodlama")
        if encoder:
            names.extend(encoder.get_feature_names_out(CATEGORICAL_FEATURES).tolist())
    return names

