import json

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.config import BASE_DIR
from app.ml.model_registry import load_model_results


router = APIRouter(prefix="/model-performance", tags=["Model Performansı"])
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))


@router.get("")
def model_performance(request: Request):
    report = load_model_results()
    chart_data = [
        {
            "model": item["model_name"],
            "mae": item["MAE"],
            "mse": item["MSE"],
            "rmse": item["RMSE"],
            "r2": item["R2 Score"],
        }
        for item in report.get("results", [])
    ]
    return templates.TemplateResponse(
        "model_performance.html",
        {
            "request": request,
            "active_page": "performance",
            "report": report,
            "chart_data_json": json.dumps(chart_data, ensure_ascii=False),
        },
    )

