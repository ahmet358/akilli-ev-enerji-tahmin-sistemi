from pydantic import ValidationError
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app import crud
from app.config import BASE_DIR
from app.database import get_db
from app.ml.predict import ModelNotReadyError, predict_energy_consumption
from app.schemas import EnergyPredictionInput


router = APIRouter(prefix="/prediction", tags=["Tahmin"])
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))


def bool_from_form(value: str | None) -> bool:
    return value in {"on", "true", "1", "evet"}


@router.get("")
def prediction_page(request: Request, user_id: int | None = None, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "prediction.html",
        {
            "request": request,
            "users": crud.list_users(db),
            "selected_user_id": user_id,
            "active_page": "prediction",
            "error": None,
        },
    )


@router.post("")
def create_prediction(
    request: Request,
    user_id: int = Form(...),
    temperature: float = Form(...),
    humidity: float = Form(...),
    hour: int = Form(...),
    day_of_week: int = Form(...),
    month: int = Form(...),
    active_appliances: int = Form(...),
    lights_usage: int = Form(...),
    heating_status: str | None = Form(None),
    cooling_status: str | None = Form(None),
    household_size: int = Form(...),
    weather_condition: str = Form(...),
    db: Session = Depends(get_db),
):
    users = crud.list_users(db)
    user = crud.get_user(db, user_id)
    if not user:
        return templates.TemplateResponse(
            "prediction.html",
            {
                "request": request,
                "users": users,
                "selected_user_id": user_id,
                "active_page": "prediction",
                "error": "Tahmin yapabilmek için geçerli bir kullanıcı seçmelisiniz.",
            },
            status_code=422,
        )

    try:
        prediction_input = EnergyPredictionInput(
            temperature=temperature,
            humidity=humidity,
            hour=hour,
            day_of_week=day_of_week,
            month=month,
            active_appliances=active_appliances,
            lights_usage=lights_usage,
            heating_status=bool_from_form(heating_status),
            cooling_status=bool_from_form(cooling_status),
            household_size=household_size,
            weather_condition=weather_condition,
        )
        predicted_value, model_name = predict_energy_consumption(prediction_input.to_feature_dict())
    except ValidationError as exc:
        return templates.TemplateResponse(
            "prediction.html",
            {
                "request": request,
                "users": users,
                "selected_user_id": user_id,
                "active_page": "prediction",
                "error": "Lütfen form alanlarını belirtilen sınırlar içinde ve geçerli değerlerle doldurun.",
            },
            status_code=422,
        )
    except ModelNotReadyError as exc:
        return templates.TemplateResponse(
            "prediction.html",
            {
                "request": request,
                "users": users,
                "selected_user_id": user_id,
                "active_page": "prediction",
                "error": str(exc),
            },
            status_code=503,
        )

    crud.create_user_action(
        db,
        user_id=user_id,
        action_type="Kullanıcı tahmin yaptı",
        action_description="Kullanıcı enerji tüketimi tahmin formunu gönderdi.",
    )
    record = crud.create_prediction_record(db, user_id, prediction_input, predicted_value, model_name)
    return RedirectResponse(url=f"/prediction/result/{record.id}", status_code=303)


@router.get("/result/{prediction_id}")
def prediction_result(prediction_id: int, request: Request, db: Session = Depends(get_db)):
    record = crud.get_prediction(db, prediction_id)
    if not record:
        raise HTTPException(status_code=404, detail="Tahmin kaydı bulunamadı.")
    crud.create_user_action(
        db,
        user_id=record.user_id,
        action_type="Kullanıcı sonuç sayfasını görüntüledi",
        action_description=f"{record.id} numaralı tahmin sonucu görüntülendi.",
    )
    return templates.TemplateResponse(
        "result.html",
        {"request": request, "record": record, "active_page": "prediction"},
    )
