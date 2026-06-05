from __future__ import annotations

import json
from pathlib import Path

from app.config import get_settings


def load_model_results() -> dict:
    settings = get_settings()
    path = settings.model_results_json
    if not path.exists():
        return {
            "best_model": "Model henüz eğitilmedi",
            "generated_at": None,
            "results": [],
            "warning": "Model performans raporu bulunamadı. Lütfen eğitim komutunu çalıştırın.",
        }
    return json.loads(path.read_text(encoding="utf-8"))


def get_active_model_name() -> str:
    return load_model_results().get("best_model", "Model henüz eğitilmedi")


def artifacts_ready() -> bool:
    settings = get_settings()
    return Path(settings.model_path).exists() and Path(settings.preprocessor_path).exists()

