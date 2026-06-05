from functools import lru_cache
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

import os


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings:
    """Uygulama ayarlarini ortam degiskenlerinden okuyan merkezi yapi."""

    app_name: str = os.getenv("APP_NAME", "Akıllı Ev Enerji Tüketimi Tahmin Sistemi")
    debug: bool = os.getenv("DEBUG", "false").lower() in {"1", "true", "yes", "evet"}
    database_url: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'runtime' / 'data' / 'smart_home_energy.db'}")
    model_path: Path = Path(os.getenv("MODEL_PATH", BASE_DIR / "saved_models" / "best_model.joblib"))
    preprocessor_path: Path = Path(
        os.getenv("PREPROCESSOR_PATH", BASE_DIR / "saved_models" / "preprocessor.joblib")
    )
    model_results_json: Path = BASE_DIR / "reports" / "model_results.json"
    model_results_csv: Path = BASE_DIR / "reports" / "model_results.csv"
    feature_importance_csv: Path = BASE_DIR / "reports" / "feature_importance.csv"
    dataset_path: Path = Path(os.getenv("DATASET_PATH", BASE_DIR / "data" / "energy_consumption.csv"))
    sample_dataset_path: Path = BASE_DIR / "data" / "sample_energy_consumption.csv"

    @property
    def sqlite_database_path(self) -> Optional[Path]:
        if self.database_url.startswith("sqlite:///"):
            return Path(self.database_url.replace("sqlite:///", "", 1))
        return None


@lru_cache
def get_settings() -> Settings:
    return Settings()
