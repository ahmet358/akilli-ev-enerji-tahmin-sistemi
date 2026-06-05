from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app import models
from app.schemas import EnergyPredictionInput, UserCreate


def create_user(db: Session, user_data: UserCreate) -> models.User:
    user = models.User(full_name=user_data.full_name, email=user_data.email.lower())
    db.add(user)
    db.commit()
    db.refresh(user)
    create_user_action(
        db,
        user_id=user.id,
        action_type="Kullanıcı oluşturuldu",
        action_description=f"{user.full_name} için yeni kullanıcı profili oluşturuldu.",
    )
    return user


def get_user(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email.lower()).first()


def list_users(db: Session) -> list[models.User]:
    return db.query(models.User).order_by(desc(models.User.created_at)).all()


def create_prediction_record(
    db: Session,
    user_id: int,
    prediction_input: EnergyPredictionInput,
    predicted_energy_consumption: float,
    model_used: str,
) -> models.PredictionRecord:
    data = prediction_input.to_feature_dict()
    record = models.PredictionRecord(
        user_id=user_id,
        temperature=data["temperature"],
        humidity=data["humidity"],
        hour=data["hour"],
        day_of_week=data["day_of_week"],
        month=data["month"],
        active_appliances=data["active_appliances"],
        lights_usage=data["lights_usage"],
        heating_status=bool(data["heating_status"]),
        cooling_status=bool(data["cooling_status"]),
        household_size=data["household_size"],
        weather_condition=data["weather_condition"],
        predicted_energy_consumption=round(float(predicted_energy_consumption), 3),
        model_used=model_used,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    create_user_action(
        db,
        user_id=user_id,
        action_type="Tahmin sonucu veritabanına kaydedildi",
        action_description=f"{record.predicted_energy_consumption:.2f} kWh tahmin sonucu kaydedildi.",
    )
    return record


def get_prediction(db: Session, prediction_id: int) -> models.PredictionRecord | None:
    return db.query(models.PredictionRecord).filter(models.PredictionRecord.id == prediction_id).first()


def list_recent_predictions(db: Session, limit: int = 8) -> list[models.PredictionRecord]:
    return db.query(models.PredictionRecord).order_by(desc(models.PredictionRecord.created_at)).limit(limit).all()


def create_user_action(
    db: Session,
    user_id: int | None,
    action_type: str,
    action_description: str,
) -> models.UserAction:
    action = models.UserAction(
        user_id=user_id,
        action_type=action_type,
        action_description=action_description,
    )
    db.add(action)
    db.commit()
    db.refresh(action)
    return action


def list_recent_actions(db: Session, limit: int = 10) -> list[models.UserAction]:
    return db.query(models.UserAction).order_by(desc(models.UserAction.created_at)).limit(limit).all()


def dashboard_statistics(db: Session) -> dict:
    total_users = db.query(models.User).count()
    total_predictions = db.query(models.PredictionRecord).count()
    average_prediction = (
        db.query(func.avg(models.PredictionRecord.predicted_energy_consumption)).scalar() or 0.0
    )
    return {
        "total_users": total_users,
        "total_predictions": total_predictions,
        "average_prediction": round(float(average_prediction), 2),
    }


def monthly_prediction_distribution(db: Session) -> list[dict]:
    rows = (
        db.query(
            models.PredictionRecord.month,
            func.count(models.PredictionRecord.id),
            func.avg(models.PredictionRecord.predicted_energy_consumption),
        )
        .group_by(models.PredictionRecord.month)
        .order_by(models.PredictionRecord.month)
        .all()
    )
    return [
        {"month": month, "count": count, "average": round(float(average or 0), 2)}
        for month, count, average in rows
    ]

