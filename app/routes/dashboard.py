import json

from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app import crud
from app.config import BASE_DIR
from app.database import get_db
from app.ml.model_registry import get_active_model_name, load_model_results


router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))


@router.get("")
def dashboard(request: Request, db: Session = Depends(get_db)):
    crud.create_user_action(
        db,
        user_id=None,
        action_type="Kullanıcı dashboard sayfasını görüntüledi",
        action_description="Dashboard sayfası açıldı.",
    )
    recent_predictions = crud.list_recent_predictions(db, limit=10)
    prediction_chart = [
        {
            "etiket": item.created_at.strftime("%d.%m %H:%M"),
            "deger": item.predicted_energy_consumption,
        }
        for item in reversed(recent_predictions)
    ]
    model_results = load_model_results().get("results", [])
    model_chart = [
        {"model": item["model_name"], "rmse": item["RMSE"], "r2": item["R2 Score"]}
        for item in model_results
    ]
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "active_page": "dashboard",
            "stats": crud.dashboard_statistics(db),
            "active_model": get_active_model_name(),
            "recent_predictions": recent_predictions,
            "recent_actions": crud.list_recent_actions(db, limit=10),
            "prediction_chart_json": json.dumps(prediction_chart, ensure_ascii=False),
            "model_chart_json": json.dumps(model_chart, ensure_ascii=False),
            "monthly_distribution": crud.monthly_prediction_distribution(db),
        },
    )

